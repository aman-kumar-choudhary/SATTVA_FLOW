from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from config import Config
from auth import token_required, admin_required, trainer_required, client_required, generate_jwt, decode_jwt
from models import User, OTP, Assignment, Session, Plan, Query, Review, Notification, MongoModel
from utils import verify_google_token, send_notification, validate_phone, validate_email
import requests as http_requests

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=[Config.FRONTEND_URL], supports_credentials=True)

# Database connection
client = MongoClient(Config.MONGODB_URI)
db = client.get_default_database()

# Initialize models
user_model         = User(db)
assignment_model   = Assignment(db)
session_model      = Session(db)
plan_model         = Plan(db)
query_model        = Query(db)
review_model       = Review(db)
notification_model = Notification(db)


# ==================== HELPERS ====================

def _build_user_payload(user):
    """Compact user dict returned in every auth response."""
    return {
        'id':      user['_id'],
        'name':    user['name'],
        'email':   user.get('email'),
        'picture': user.get('picture', ''),
        'phone':   user.get('phone'),
        'role':    user['role'],
        'status':  user.get('status', 'pending')
    }


def _exchange_code_for_google_data(code, redirect_uri):
    """
    Exchange an OAuth authorization code for Google user info.
    Returns a dict with google_id, email, name, picture — or None on failure.
    """
    try:
        # Step 1: exchange code for tokens
        token_resp = http_requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code':          code,
                'client_id':     Config.GOOGLE_CLIENT_ID,
                'client_secret': Config.GOOGLE_CLIENT_SECRET,
                'redirect_uri':  redirect_uri,
                'grant_type':    'authorization_code',
            },
            timeout=10
        )
        token_data = token_resp.json()
        if 'error' in token_data:
            print(f"Token exchange error: {token_data}")
            return None

        access_token = token_data.get('access_token')
        id_token     = token_data.get('id_token')

        if not access_token:
            return None

        # Step 2: fetch user info using access token
        userinfo_resp = http_requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=10
        )
        info = userinfo_resp.json()

        if not info.get('verified_email', False):
            print("Google: email not verified")
            return None

        return {
            'google_id': info['id'],
            'email':     info['email'],
            'name':      info.get('name', ''),
            'picture':   info.get('picture', ''),
        }

    except Exception as e:
        print(f"Google code exchange error: {e}")
        return None


@app.after_request
def fix_cors_headers(response):
    response.headers["Cross-Origin-Opener-Policy"]   = "same-origin-allow-popups"
    response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"
    response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return response


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    """
    Accepts either:
      - { token: '<google_id_token>' }  — legacy / One Tap flow
      - { code: '<oauth_code>', redirect_uri: '...' }  — redirect flow

    Returns one of:
      - { token, user }           → existing user, log them in
      - { needs_profile, google_data }  → new user, must complete signup first
      - 4xx on error
    """
    data = request.get_json() or {}

    # ── Resolve google_data from either token or code ────────────────────────
    google_data = None

    if data.get('token'):
        # ID-token path (One Tap / popup)
        google_data = verify_google_token(data['token'])
    elif data.get('code'):
        # Authorization-code path (redirect flow)
        redirect_uri = data.get('redirect_uri', '')
        google_data  = _exchange_code_for_google_data(data['code'], redirect_uri)

    if not google_data:
        return jsonify({'error': 'Invalid or expired Google credentials'}), 401

    email     = google_data['email']
    google_id = google_data['google_id']

    # ── Admin fast-path ──────────────────────────────────────────────────────
    if email == Config.ADMIN_EMAIL:
        user = user_model.find_by_email(email)
        if not user:
            user = user_model.create({
                'name':        google_data['name'] or 'Admin',
                'email':       email,
                'google_id':   google_id,
                'picture':     google_data.get('picture', ''),
                'role':        'admin',
                'status':      'active',
                'is_verified': True
            })
        else:
            if not user.get('google_id'):
                user_model.update(user['_id'], {
                    'google_id': google_id,
                    'picture':   google_data.get('picture', ''),
                })
                user['google_id'] = google_id

        jwt_token = generate_jwt(user['_id'], user['role'])
        return jsonify({'token': jwt_token, 'user': _build_user_payload(user)}), 200

    # ── Look up existing user ────────────────────────────────────────────────
    user = user_model.find_by_google_id(google_id) or user_model.find_by_email(email)

    if user:
        # Patch google_id if missing
        if not user.get('google_id'):
            user_model.update(user['_id'], {
                'google_id': google_id,
                'picture':   google_data.get('picture', ''),
            })
        jwt_token = generate_jwt(user['_id'], user['role'])
        return jsonify({'token': jwt_token, 'user': _build_user_payload(user)}), 200

    # ── New user — must complete signup ──────────────────────────────────────
    return jsonify({
        'needs_profile': True,
        'google_data': {
            'email':     email,
            'name':      google_data['name'],
            'picture':   google_data.get('picture', ''),
            'google_id': google_id
        }
    }), 200


@app.route('/api/auth/google/complete', methods=['POST'])
def google_complete():
    """
    Step 2 — save profile after first Google login (signup completion).
    """
    data      = request.get_json() or {}
    google_id = data.get('google_id')
    email     = data.get('email')
    role      = data.get('role', 'client')

    if not google_id or not email:
        return jsonify({'error': 'google_id and email are required'}), 400

    # Block admin email from using signup flow
    if email == Config.ADMIN_EMAIL:
        return jsonify({'error': 'Admin account must log in directly.'}), 403

    if role not in User.ROLES or role == 'admin':
        return jsonify({'error': 'Invalid role. Choose client or trainer.'}), 400

    # Guard against duplicates
    existing = user_model.find_by_google_id(google_id) or user_model.find_by_email(email)
    if existing:
        jwt_token = generate_jwt(existing['_id'], existing['role'])
        return jsonify({'token': jwt_token, 'user': _build_user_payload(existing)}), 200

    user_data = {
        'name':        data.get('name', ''),
        'email':       email,
        'google_id':   google_id,
        'picture':     data.get('picture', ''),
        'phone':       data.get('phone') or None,
        'role':        role,
        'status':      'active' if role == 'client' else 'pending',
        'is_verified': True,
    }

    if role == 'trainer':
        certs_raw = data.get('certifications', '')
        user_data['specialization'] = data.get('specialization', '')
        user_data['experience']     = int(data.get('experience', 0))
        user_data['certifications'] = [c.strip() for c in certs_raw.split(',')] if isinstance(certs_raw, str) else certs_raw
        user_data['bio']            = data.get('bio', '')

    user = user_model.create(user_data)

    # Notify admin about new trainer signup
    if role == 'trainer':
        admin = user_model.find_by_email(Config.ADMIN_EMAIL)
        if admin:
            notification_model.create(
                admin['_id'],
                'New Trainer Registration',
                f'{user["name"]} has applied as a trainer. Please review and approve.'
            )

    jwt_token = generate_jwt(user['_id'], user['role'])
    return jsonify({'token': jwt_token, 'user': _build_user_payload(user)}), 201


@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user():
    user_id = request.user.get('user_id')
    user    = user_model.find_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id':              user['_id'],
        'name':            user['name'],
        'email':           user.get('email'),
        'picture':         user.get('picture', ''),
        'phone':           user.get('phone'),
        'role':            user['role'],
        'status':          user.get('status'),
        'profile':         user.get('profile', {}),
        'trainer_details': user.get('trainer_details') if user['role'] == 'trainer' else None
    }), 200


@app.route('/api/auth/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update the current user's profile details."""
    user_id = request.user.get('user_id')
    data    = request.get_json() or {}

    allowed = ['name', 'phone', 'profile']
    update  = {k: v for k, v in data.items() if k in allowed}

    # Trainer-specific fields
    if request.user.get('role') == 'trainer':
        trainer_fields = ['specialization', 'experience', 'certifications', 'bio']
        trainer_update = {f'trainer_details.{k}': v for k, v in data.items() if k in trainer_fields}
        update.update(trainer_update)

    if not update:
        return jsonify({'error': 'No valid fields to update'}), 400

    user_model.update(user_id, update)
    user = user_model.find_by_id(user_id)
    return jsonify({'message': 'Profile updated', 'user': _build_user_payload(user)}), 200


# ==================== ADMIN ROUTES ====================

@app.route('/api/admin/trainers', methods=['GET'])
@token_required
@admin_required
def get_trainers():
    status   = request.args.get('status')
    trainers = user_model.get_all_trainers(status)
    return jsonify(trainers), 200


@app.route('/api/admin/trainers/<trainer_id>/approve', methods=['PUT'])
@token_required
@admin_required
def approve_trainer(trainer_id):
    trainer = user_model.find_by_id(trainer_id)
    if not trainer or trainer['role'] != 'trainer':
        return jsonify({'error': 'Trainer not found'}), 404

    user_model.update(trainer_id, {
        'status': 'active',
        'trainer_details.approved_by': request.user.get('user_id'),
        'trainer_details.approved_at': datetime.utcnow()
    })

    send_notification(trainer, 'Trainer Application Approved',
                      'Congratulations! Your trainer application has been approved.')
    notification_model.create(trainer_id, 'Trainer Application Approved',
                              'Congratulations! Your application has been approved.')

    return jsonify({'message': 'Trainer approved successfully'}), 200


@app.route('/api/admin/trainers/<trainer_id>/reject', methods=['PUT'])
@token_required
@admin_required
def reject_trainer(trainer_id):
    trainer = user_model.find_by_id(trainer_id)
    if not trainer or trainer['role'] != 'trainer':
        return jsonify({'error': 'Trainer not found'}), 404

    reason = (request.get_json() or {}).get('reason', '')
    user_model.update(trainer_id, {'status': 'rejected'})

    send_notification(trainer, 'Trainer Application Rejected',
                      f'Your trainer application has been rejected. Reason: {reason}')
    notification_model.create(trainer_id, 'Trainer Application Rejected',
                              f'Your application was rejected. Reason: {reason}')

    return jsonify({'message': 'Trainer rejected'}), 200


@app.route('/api/admin/clients', methods=['GET'])
@token_required
@admin_required
def get_clients():
    status  = request.args.get('status')
    clients = user_model.get_all_clients(status)
    return jsonify(clients), 200


@app.route('/api/admin/assignments', methods=['POST'])
@token_required
@admin_required
def create_assignment():
    data       = request.get_json() or {}
    trainer_id = data.get('trainer_id')
    client_id  = data.get('client_id')

    if not trainer_id or not client_id:
        return jsonify({'error': 'Trainer ID and Client ID are required'}), 400

    existing = assignment_model.get_client_trainer(client_id)
    if existing:
        return jsonify({'error': 'Client already has an assigned trainer'}), 400

    assignment_id = assignment_model.create(trainer_id, client_id)

    trainer = user_model.find_by_id(trainer_id)
    cl      = user_model.find_by_id(client_id)

    send_notification(trainer, 'New Client Assigned',
                      f'You have been assigned to {cl["name"]} as their yoga trainer.')
    notification_model.create(trainer_id, 'New Client Assigned',
                              f'You have been assigned to {cl["name"]}')

    send_notification(cl, 'Trainer Assigned',
                      f'You have been assigned to {trainer["name"]} as your yoga trainer.')
    notification_model.create(client_id, 'Trainer Assigned',
                              f'You have been assigned to {trainer["name"]}')

    return jsonify({'message': 'Client assigned successfully', 'assignment_id': assignment_id}), 201


@app.route('/api/admin/assignments', methods=['GET'])
@token_required
@admin_required
def get_assignments():
    assignments = assignment_model.get_all_assignments()

    for assignment in assignments:
        trainer = user_model.find_by_id(assignment['trainer_id'])
        cl      = user_model.find_by_id(assignment['client_id'])
        assignment['trainer'] = trainer
        assignment['client']  = cl

    return jsonify(assignments), 200


@app.route('/api/admin/queries', methods=['GET'])
@token_required
@admin_required
def get_all_queries():
    status  = request.args.get('status')
    queries = query_model.get_all_queries()

    for q in queries:
        sender      = user_model.find_by_id(q['sender_id'])
        q['sender'] = sender

    if status:
        queries = [q for q in queries if q['status'] == status]

    return jsonify(queries), 200


@app.route('/api/admin/queries/<query_id>/respond', methods=['POST'])
@token_required
@admin_required
def respond_to_query(query_id):
    data     = request.get_json() or {}
    response = data.get('response')

    if not response:
        return jsonify({'error': 'Response is required'}), 400

    query_model.respond(query_id, response, request.user.get('user_id'))

    q = query_model.collection.find_one({'_id': ObjectId(query_id)})
    if q:
        sender = user_model.find_by_id(q['sender_id'])
        if sender:
            send_notification(sender, 'Query Response',
                              f'Your query has been answered: {response}')
            notification_model.create(sender['_id'], 'Query Response',
                                      f'Your query has been answered: {response[:100]}...')

    return jsonify({'message': 'Response sent successfully'}), 200


@app.route('/api/admin/reviews', methods=['GET'])
@token_required
@admin_required
def get_reviews():
    status  = request.args.get('status', 'pending')
    reviews = review_model.get_pending_reviews() if status == 'pending' else review_model.get_all_approved()

    for review in reviews:
        review['client']  = user_model.find_by_id(review['client_id'])
        review['trainer'] = user_model.find_by_id(review['trainer_id'])

    return jsonify(reviews), 200


@app.route('/api/admin/reviews/<review_id>/approve', methods=['PUT'])
@token_required
@admin_required
def approve_review(review_id):
    if review_model.approve(review_id):
        return jsonify({'message': 'Review approved'}), 200
    return jsonify({'error': 'Review not found'}), 404


@app.route('/api/admin/reviews/<review_id>/reject', methods=['DELETE'])
@token_required
@admin_required
def reject_review(review_id):
    result = review_model.collection.delete_one({'_id': ObjectId(review_id)})
    if result.deleted_count:
        return jsonify({'message': 'Review rejected'}), 200
    return jsonify({'error': 'Review not found'}), 404


@app.route('/api/admin/stats', methods=['GET'])
@token_required
@admin_required
def get_stats():
    return jsonify({
        'total_trainers':  user_model.collection.count_documents({'role': 'trainer'}),
        'active_trainers': user_model.collection.count_documents({'role': 'trainer', 'status': 'active'}),
        'total_clients':   user_model.collection.count_documents({'role': 'client'}),
        'active_clients':  user_model.collection.count_documents({'role': 'client', 'status': 'active'}),
        'total_sessions':  session_model.collection.count_documents({}),
        'pending_queries': query_model.collection.count_documents({'status': 'pending'}),
        'pending_reviews': review_model.collection.count_documents({'status': 'pending'})
    }), 200


# ==================== TRAINER ROUTES ====================

@app.route('/api/trainer/clients', methods=['GET'])
@token_required
@trainer_required
def get_trainer_clients():
    trainer_id  = request.user.get('user_id')
    assignments = assignment_model.get_trainer_clients(trainer_id)

    clients = []
    for assignment in assignments:
        c = user_model.find_by_id(assignment['client_id'])
        if c:
            c['assignment_id']      = assignment['_id']
            c['sessions_completed'] = assignment.get('sessions_completed', 0)
            clients.append(c)

    return jsonify(clients), 200


@app.route('/api/trainer/sessions', methods=['GET', 'POST'])
@token_required
@trainer_required
def trainer_sessions():
    trainer_id = request.user.get('user_id')

    if request.method == 'GET':
        return jsonify(session_model.get_trainer_sessions(trainer_id)), 200

    data             = request.get_json() or {}
    data['trainer_id'] = trainer_id

    assignment = assignment_model.get_client_trainer(data['client_id'])
    if not assignment or assignment['trainer_id'] != trainer_id:
        return jsonify({'error': 'Client not assigned to you'}), 403

    session_id = session_model.create(data)

    c = user_model.find_by_id(data['client_id'])
    if c:
        send_notification(c, 'New Session Scheduled',
                          f'New session "{data["title"]}" has been scheduled for you.')
        notification_model.create(c['_id'], 'New Session Scheduled',
                                  f'New session "{data["title"]}" has been scheduled.')

    return jsonify({'message': 'Session created', 'session_id': session_id}), 201


@app.route('/api/trainer/plans', methods=['GET', 'POST'])
@token_required
@trainer_required
def trainer_plans():
    trainer_id = request.user.get('user_id')

    if request.method == 'GET':
        client_id = request.args.get('client_id')
        if client_id:
            plans = plan_model.get_client_plans(client_id)
        else:
            assignments = assignment_model.get_trainer_clients(trainer_id)
            plans = []
            for a in assignments:
                plans.extend(plan_model.get_client_plans(a['client_id']))
        return jsonify(plans), 200

    data             = request.get_json() or {}
    data['trainer_id'] = trainer_id

    assignment = assignment_model.get_client_trainer(data['client_id'])
    if not assignment or assignment['trainer_id'] != trainer_id:
        return jsonify({'error': 'Client not assigned to you'}), 403

    plan_id = plan_model.create(data)

    c = user_model.find_by_id(data['client_id'])
    if c:
        send_notification(c, 'New Yoga Plan',
                          f'Your trainer has created a new plan: {data["title"]}')
        notification_model.create(c['_id'], 'New Yoga Plan',
                                  f'New plan created: {data["title"]}')

    return jsonify({'message': 'Plan created', 'plan_id': plan_id}), 201


@app.route('/api/trainer/plans/<plan_id>/progress', methods=['PUT'])
@token_required
@trainer_required
def update_plan_progress(plan_id):
    data     = request.get_json() or {}
    progress = data.get('progress')

    if progress is None:
        return jsonify({'error': 'Progress is required'}), 400

    plan_model.update_progress(plan_id, progress)
    return jsonify({'message': 'Progress updated'}), 200


@app.route('/api/trainer/reviews', methods=['GET'])
@token_required
@trainer_required
def get_trainer_reviews():
    trainer_id = request.user.get('user_id')
    reviews    = review_model.get_trainer_reviews(trainer_id)

    for review in reviews:
        review['client'] = user_model.find_by_id(review['client_id'])

    return jsonify(reviews), 200


# ==================== CLIENT ROUTES ====================

@app.route('/api/client/trainer', methods=['GET'])
@token_required
@client_required
def get_my_trainer():
    client_id  = request.user.get('user_id')
    assignment = assignment_model.get_client_trainer(client_id)

    if not assignment:
        return jsonify({'error': 'No trainer assigned yet'}), 404

    trainer = user_model.find_by_id(assignment['trainer_id'])
    if trainer:
        trainer['assignment_id']      = assignment['_id']
        trainer['sessions_completed'] = assignment.get('sessions_completed', 0)

    return jsonify(trainer), 200


@app.route('/api/client/sessions', methods=['GET'])
@token_required
@client_required
def get_my_sessions():
    client_id = request.user.get('user_id')
    return jsonify(session_model.get_client_sessions(client_id)), 200


@app.route('/api/client/plans', methods=['GET'])
@token_required
@client_required
def get_my_plans():
    client_id = request.user.get('user_id')
    return jsonify(plan_model.get_client_plans(client_id)), 200


@app.route('/api/client/queries', methods=['GET', 'POST'])
@token_required
@client_required
def client_queries():
    client_id = request.user.get('user_id')

    if request.method == 'GET':
        return jsonify(query_model.get_user_queries(client_id)), 200

    data                  = request.get_json() or {}
    data['sender_id']     = client_id
    data['sender_role']   = 'client'
    data['receiver_id']   = None
    data['receiver_role'] = 'admin'

    query_id = query_model.create(data)

    admin = user_model.find_by_email(Config.ADMIN_EMAIL)
    if admin:
        notification_model.create(admin['_id'], 'New Query from Client',
                                  f'New query: {data.get("subject")}')

    return jsonify({'message': 'Query sent', 'query_id': query_id}), 201


@app.route('/api/client/reviews', methods=['GET', 'POST'])
@token_required
@client_required
def client_reviews():
    client_id = request.user.get('user_id')

    if request.method == 'GET':
        reviews = list(review_model.collection.find({'client_id': ObjectId(client_id)}))
        return jsonify([MongoModel.serialize(r) for r in reviews]), 200

    data              = request.get_json() or {}
    data['client_id'] = client_id

    assignment = assignment_model.get_client_trainer(client_id)
    if not assignment:
        return jsonify({'error': 'No trainer assigned'}), 400

    data['trainer_id'] = assignment['trainer_id']

    existing = review_model.collection.find_one({
        'client_id':  ObjectId(client_id),
        'trainer_id': ObjectId(assignment['trainer_id'])
    })
    if existing:
        return jsonify({'error': 'You have already reviewed this trainer'}), 400

    review_id = review_model.create(data)
    return jsonify({'message': 'Review submitted', 'review_id': review_id}), 201


# ==================== NOTIFICATION ROUTES ====================

@app.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications():
    user_id     = request.user.get('user_id')
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    return jsonify(notification_model.get_user_notifications(user_id, unread_only)), 200


@app.route('/api/notifications/<notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_read(notification_id):
    notification_model.mark_as_read(notification_id)
    return jsonify({'message': 'Notification marked as read'}), 200


@app.route('/api/notifications/read-all', methods=['PUT'])
@token_required
def mark_all_read():
    user_id = request.user.get('user_id')
    notification_model.mark_all_read(user_id)
    return jsonify({'message': 'All notifications marked as read'}), 200


# ==================== PUBLIC ROUTES ====================

@app.route('/api/public/trainers', methods=['GET'])
def get_featured_trainers():
    trainers = user_model.get_all_trainers('active')

    featured = []
    for t in trainers[:6]:
        reviews = review_model.get_trainer_reviews(t['_id'])
        avg     = round(sum(r['rating'] for r in reviews) / len(reviews), 1) if reviews else 0
        featured.append({
            'id':             t['_id'],
            'name':           t['name'],
            'picture':        t.get('picture', ''),
            'specialization': t.get('trainer_details', {}).get('specialization', ''),
            'experience':     t.get('trainer_details', {}).get('experience', 0),
            'bio':            t.get('trainer_details', {}).get('bio', ''),
            'avg_rating':     avg,
            'review_count':   len(reviews)
        })

    return jsonify(featured), 200


@app.route('/api/public/reviews', methods=['GET'])
def get_public_reviews():
    reviews = review_model.get_all_approved()

    for review in reviews:
        c = user_model.find_by_id(review['client_id'])
        t = user_model.find_by_id(review['trainer_id'])
        review['client_name']  = c['name'] if c else 'Anonymous'
        review['trainer_name'] = t['name'] if t else ''

    return jsonify(reviews), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)