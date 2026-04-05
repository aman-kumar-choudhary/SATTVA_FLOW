# app.py
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from functools import wraps
import logging

from config import Config
from models import (
    UserModel, ClientModel, TrainerModel, AssignmentModel,
    SessionModel, PlanModel, PackageModel, MessageModel,
    QueryModel, ReviewModel, NotificationModel, ActivityLogModel,
    SubscriptionModel
)
from notification_service import NotificationService
from auth import token_required, admin_required, trainer_required, client_required, generate_jwt
from utils import verify_google_token

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=[Config.FRONTEND_URL], supports_credentials=True)

# Database connection
mongo_client = MongoClient(Config.MONGODB_URI)
db = mongo_client[Config.DATABASE_NAME]

# Initialize models
user_model = UserModel(db)
client_model = ClientModel(db)
trainer_model = TrainerModel(db)
assignment_model = AssignmentModel(db)
session_model = SessionModel(db)
plan_model = PlanModel(db)
package_model = PackageModel(db)
message_model = MessageModel(db)
query_model = QueryModel(db)
review_model = ReviewModel(db)
notification_model = NotificationModel(db)
activity_log_model = ActivityLogModel(db)
subscription_model = SubscriptionModel(db)

# Ensure admin exists on startup
def ensure_admin():
    admin = user_model.create_admin(
        email=Config.ADMIN_EMAIL,
        name=Config.ADMIN_NAME,
        phone=Config.ADMIN_PHONE
    )
    logger.info(f"Admin ensured: {admin['email'] if admin else 'Failed'}")
    return admin

ADMIN = ensure_admin()

# Helper functions
def get_admin():
    return user_model.get_admin()

def log_activity(user_id, user_role, action_type, description, metadata=None):
    """Log user activity"""
    activity_log_model.log(user_id, user_role, action_type, description, metadata)

def create_notification(user_id, title, message, ntype='info', link=None):
    """Create in-app notification"""
    return notification_model.create(user_id, title, message, ntype, link)

def send_notification_with_channels(user, title, message, ntype='info', link=None):
    """Send notification via all channels"""
    # Create in-app notification
    create_notification(user['_id'], title, message, ntype, link)
    
    # Send email/WhatsApp
    NotificationService.send_notification(user, title, message, ntype, link)

def notify_admin(title, message, ntype='info', link=None):
    """Notify admin"""
    admin = get_admin()
    if admin:
        send_notification_with_channels(admin, title, message, ntype, link)

def notify_user_by_id(user_id, title, message, ntype='info', link=None):
    """Notify user by ID"""
    # Try to find user in clients first, then trainers
    user = client_model.find_by_id(user_id)
    if not user:
        user = trainer_model.find_by_id(user_id)
    if not user:
        user = user_model.find_by_id(user_id)
    
    if user:
        send_notification_with_channels(user, title, message, ntype, link)

def get_user_by_id(user_id):
    """Get user from appropriate collection"""
    user = client_model.find_by_id(user_id)
    if user:
        return user, 'client'
    
    user = trainer_model.find_by_id(user_id)
    if user:
        return user, 'trainer'
    
    user = user_model.find_by_id(user_id)
    if user:
        return user, 'admin'
    
    return None, None

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    """Google Sign-In authentication"""
    data = request.get_json() or {}
    id_token = data.get('token')
    
    if not id_token:
        return jsonify({'error': 'ID token required'}), 400
    
    google_data = verify_google_token(id_token)
    if not google_data:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    email = google_data['email']
    google_id = google_data['google_id']
    
    # Check admin
    if email == Config.ADMIN_EMAIL:
        admin = user_model.find_by_email(email)
        if not admin:
            admin = user_model.create_admin(email, Config.ADMIN_NAME, google_id, google_data.get('picture'))
        token = generate_jwt(admin['_id'], 'admin')
        return jsonify({'token': token, 'user': admin}), 200
    
    # Check existing client
    client = client_model.find_by_email(email)
    if client:
        token = generate_jwt(client['_id'], 'client')
        return jsonify({'token': token, 'user': client}), 200
    
    # Check existing trainer
    trainer = trainer_model.find_by_email(email)
    if trainer:
        token = generate_jwt(trainer['_id'], 'trainer')
        return jsonify({'token': token, 'user': trainer}), 200
    
    # New user - need profile completion
    return jsonify({
        'needs_profile': True,
        'google_data': google_data
    }), 200

@app.route('/api/auth/google/complete', methods=['POST'])
def google_complete():
    """Complete registration after Google auth"""
    data = request.get_json() or {}
    google_id = data.get('google_id')
    email = data.get('email')
    role = data.get('role', 'client')
    
    if not google_id or not email:
        return jsonify({'error': 'google_id and email required'}), 400
    
    if role == 'admin':
        return jsonify({'error': 'Cannot register as admin'}), 403
    
    if role == 'client':
        # Check if already exists
        existing = client_model.find_by_email(email)
        if existing:
            token = generate_jwt(existing['_id'], 'client')
            return jsonify({'token': token, 'user': existing}), 200
        
        # Create client
        client = client_model.create(data)
        
        # Notify admin
        notify_admin(
            f"New Client Registration",
            f"New client {client['name']} ({client['email']}) has registered. Please activate their account.",
            'registration',
            f"/admin/clients?status=pending"
        )
        
        # Send welcome email
        send_notification_with_channels(
            client,
            "Welcome to SattvaFlow!",
            "Your account has been created. Admin will activate your account soon.",
            'success',
            "/client/dashboard"
        )
        
        token = generate_jwt(client['_id'], 'client')
        return jsonify({'token': token, 'user': client}), 201
    
    elif role == 'trainer':
        existing = trainer_model.find_by_email(email)
        if existing:
            token = generate_jwt(existing['_id'], 'trainer')
            return jsonify({'token': token, 'user': existing}), 200
        
        trainer = trainer_model.create(data)
        
        # Notify admin
        notify_admin(
            f"New Trainer Registration - Pending Approval",
            f"Trainer {trainer['name']} ({trainer['email']}) has registered. Specialization: {trainer.get('specialization', 'N/A')}",
            'registration',
            f"/admin/trainers?status=pending"
        )
        
        # Send welcome email
        send_notification_with_channels(
            trainer,
            "Trainer Application Received",
            "Your application is under review. You'll be notified once approved.",
            'info',
            "/trainer/dashboard"
        )
        
        token = generate_jwt(trainer['_id'], 'trainer')
        return jsonify({'token': token, 'user': trainer}), 201
    
    return jsonify({'error': 'Invalid role'}), 400

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current user details"""
    user, role = get_user_by_id(request.user['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user), 200

@app.route('/api/auth/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    user_id = request.user['user_id']
    role = request.user['role']
    data = request.get_json() or {}

    # Allowed fields by role
    allowed_base = {'name', 'phone'}
    allowed_client = allowed_base | {
        'city', 'age', 'date_of_birth', 'gender',
        'health_conditions', 'yoga_experience', 'health_goals',
        'expectations', 'emergency_contact'
    }
    allowed_trainer = allowed_base | {
        'specialization', 'experience', 'certifications', 'bio', 'city'
    }

    if role == 'admin':
        filtered = {k: v for k, v in data.items() if k in allowed_base}
        user_model.update(user_id, filtered)
    elif role == 'client':
        filtered = {k: v for k, v in data.items() if k in allowed_client}
        client_model.update(user_id, filtered)
    elif role == 'trainer':
        filtered = {k: v for k, v in data.items() if k in allowed_trainer}
        trainer_model.update(user_id, filtered)

    log_activity(user_id, role, 'profile_update', 'Updated profile')

    # Return updated user
    user, _ = get_user_by_id(user_id)
    return jsonify({'message': 'Profile updated successfully', 'user': user}), 200

# ==================== ADMIN ROUTES ====================

@app.route('/api/admin/stats', methods=['GET'])
@token_required
@admin_required
def admin_stats():
    """Get dashboard statistics"""
    stats = {
        'trainers': {
            'total': trainer_model.count(),
            'pending': trainer_model.count({'status': 'pending'}),
            'active': trainer_model.count({'status': 'active'}),
            'blocked': trainer_model.count({'status': 'blocked'})
        },
        'clients': {
            'total': client_model.count(),
            'pending': client_model.count({'status': 'pending'}),
            'active': client_model.count({'status': 'active'}),
            'blocked': client_model.count({'status': 'blocked'})
        },
        'sessions': {
            'total': session_model.count(),
            'scheduled': session_model.count({'status': 'scheduled'}),
            'completed': session_model.count({'status': 'completed'}),
            'cancelled': session_model.count({'status': 'cancelled'})
        },
        'assignments': assignment_model.count({'status': 'active'}),
        'packages': package_model.count({'is_active': True}),
        'pending_queries': query_model.count({'status': 'pending'}),
        'pending_reviews': review_model.count({'status': 'pending'}),
        'unread_messages': message_model.get_unread_count(get_admin()['_id'])
    }
    
    return jsonify(stats), 200

@app.route('/api/admin/trainers', methods=['GET'])
@token_required
@admin_required
def admin_get_trainers():
    """Get all trainers with pagination"""
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    result = trainer_model.get_all(status, page, per_page)
    return jsonify(result), 200

@app.route('/api/admin/trainers/<trainer_id>', methods=['GET'])
@token_required
@admin_required
def admin_get_trainer(trainer_id):
    """Get trainer details with reviews and clients"""
    trainer = trainer_model.find_by_id(trainer_id)
    if not trainer:
        return jsonify({'error': 'Trainer not found'}), 404
    
    # Get reviews
    reviews = review_model.get_trainer_reviews(trainer_id)
    trainer['reviews'] = reviews
    
    # Get assigned clients
    assignments = assignment_model.get_trainer_clients(trainer_id)
    clients = []
    for assignment in assignments:
        client = client_model.find_by_id(assignment['client_id'])
        if client:
            client['assignment_id'] = assignment['_id']
            client['sessions_completed'] = assignment.get('sessions_completed', 0)
            clients.append(client)
    trainer['assigned_clients'] = clients
    
    return jsonify(trainer), 200

@app.route('/api/admin/trainers/<trainer_id>/approve', methods=['PUT'])
@token_required
@admin_required
def admin_approve_trainer(trainer_id):
    """Approve trainer application"""
    trainer = trainer_model.find_by_id(trainer_id)
    if not trainer:
        return jsonify({'error': 'Trainer not found'}), 404
    
    admin_id = request.user['user_id']
    trainer_model.approve(trainer_id, admin_id)
    
    # Notify trainer
    send_notification_with_channels(
        trainer,
        "Trainer Application Approved!",
        f"Congratulations! Your trainer application has been approved. You can now log in and start working with clients.",
        'success',
        "/trainer/dashboard"
    )
    
    log_activity(admin_id, 'admin', 'approve_trainer', f"Approved trainer {trainer['name']}")
    
    return jsonify({'message': 'Trainer approved successfully'}), 200

@app.route('/api/admin/trainers/<trainer_id>/reject', methods=['PUT'])
@token_required
@admin_required
def admin_reject_trainer(trainer_id):
    """Reject trainer application"""
    trainer = trainer_model.find_by_id(trainer_id)
    if not trainer:
        return jsonify({'error': 'Trainer not found'}), 404
    
    reason = request.get_json().get('reason', 'Not specified')
    trainer_model.reject(trainer_id, reason)
    
    # Notify trainer
    send_notification_with_channels(
        trainer,
        "Trainer Application Update",
        f"Your trainer application was not approved. Reason: {reason}",
        'error',
        "/signup"
    )
    
    log_activity(request.user['user_id'], 'admin', 'reject_trainer', f"Rejected trainer {trainer['name']}")
    
    return jsonify({'message': 'Trainer rejected'}), 200

@app.route('/api/admin/trainers/<trainer_id>/block', methods=['PUT'])
@token_required
@admin_required
def admin_block_trainer(trainer_id):
    """Block trainer"""
    trainer = trainer_model.find_by_id(trainer_id)
    if not trainer:
        return jsonify({'error': 'Trainer not found'}), 404
    
    trainer_model.block(trainer_id)
    
    send_notification_with_channels(
        trainer,
        "Account Blocked",
        "Your trainer account has been blocked. Please contact admin for details.",
        'error',
        "/login"
    )
    
    return jsonify({'message': 'Trainer blocked'}), 200

@app.route('/api/admin/clients', methods=['GET'])
@token_required
@admin_required
def admin_get_clients():
    """Get all clients with pagination"""
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    result = client_model.get_all(status, page, per_page)
    
    # Add assigned trainer info
    for client in result['items']:
        assignment = assignment_model.get_client_trainer(client['_id'])
        if assignment:
            trainer = trainer_model.find_by_id(assignment['trainer_id'])
            if trainer:
                client['assigned_trainer'] = {
                    '_id': trainer['_id'],
                    'name': trainer['name'],
                    'specialization': trainer.get('specialization', '')
                }
    
    return jsonify(result), 200

@app.route('/api/admin/clients/<client_id>/activate', methods=['PUT'])
@token_required
@admin_required
def admin_activate_client(client_id):
    """Activate client account"""
    client = client_model.find_by_id(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    client_model.activate(client_id)
    
    send_notification_with_channels(
        client,
        "Account Activated!",
        "Your SattvaFlow account has been activated. Welcome aboard!",
        'success',
        "/client/dashboard"
    )
    
    log_activity(request.user['user_id'], 'admin', 'activate_client', f"Activated client {client['name']}")
    
    return jsonify({'message': 'Client activated'}), 200


@app.route('/api/admin/clients/<client_id>/detail', methods=['GET'])
@token_required
@admin_required
def admin_client_detail(client_id):
    """Get complete client detail: info, trainer, sessions, queries, subscription, progress"""
    client = client_model.find_by_id(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
 
    # Trainer
    assignment = assignment_model.get_client_trainer(client_id)
    trainer = None
    if assignment:
        trainer = trainer_model.find_by_id(assignment['trainer_id'])
 
    # Sessions (all, sorted by scheduled_at desc)
    sessions = session_model.get_client_sessions(client_id)
 
    # Queries
    queries_data = query_model.get_all_for_user(client_id)

    # Subscription / package progress
    subscription = subscription_model.get_active(client_id)
    progress = subscription_model.compute_progress(subscription)

    return jsonify({
        'client': client,
        'trainer': trainer,
        'sessions': sessions,
        'queries': queries_data,
        'subscription': subscription,
        'progress': progress,
    }), 200
 
@app.route('/api/admin/clients/<client_id>/assign-trainer', methods=['POST'])
@token_required
@admin_required
def admin_assign_trainer_shorthand(client_id):
    """Assign or reassign a trainer to a client from the client detail panel."""
    data = request.get_json() or {}
    trainer_id = data.get('trainer_id')
    if not trainer_id:
        return jsonify({'error': 'trainer_id required'}), 400

    client = client_model.find_by_id(client_id)
    trainer = trainer_model.find_by_id(trainer_id)
    if not client or not trainer:
        return jsonify({'error': 'Client or trainer not found'}), 404
    if trainer.get('status') != 'active':
        return jsonify({'error': 'Trainer is not active'}), 400

    # assign() already deactivates any previous assignment first
    assignment = assignment_model.assign(trainer_id, client_id, request.user['user_id'])

    send_notification_with_channels(
        trainer,
        "New Client Assigned",
        f"You have been assigned client: {client['name']}.",
        'assignment',
        f"/trainer/clients/{client_id}"
    )
    send_notification_with_channels(
        client,
        "Trainer Assigned",
        f"Your trainer is now {trainer['name']} ({trainer.get('specialization', '')}).",
        'assignment',
        "/client/trainer"
    )
    log_activity(
        request.user['user_id'], 'admin', 'assign_trainer',
        f"Assigned {client['name']} → {trainer['name']}"
    )
    return jsonify({'message': 'Trainer assigned', 'assignment': assignment}), 200


@app.route('/api/admin/clients/<client_id>/unblock', methods=['PUT'])
@token_required
@admin_required
def admin_unblock_client(client_id):
    """Unblock client account"""
    client = client_model.find_by_id(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
 
    client_model.activate(client_id)
 
    send_notification_with_channels(
        client,
        "Account Unblocked",
        "Your SattvaFlow account has been unblocked. You can now log in.",
        'success',
        "/client/dashboard"
    )
    log_activity(request.user['user_id'], 'admin', 'unblock_client', f"Unblocked client {client['name']}")
    return jsonify({'message': 'Client unblocked'}), 200

@app.route('/api/admin/clients/<client_id>', methods=['DELETE'])
@token_required
@admin_required
def admin_delete_client(client_id):
    """Permanently remove client and all their data"""
    client = client_model.find_by_id(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
 
    # Remove assignments
    assignment_model.collection.delete_many({'client_id': client_id})
    # Remove sessions
    session_model.collection.delete_many({'client_id': client_id})
    # Remove subscriptions
    subscription_model.collection.delete_many({'client_id': client_id})
    # Remove queries
    query_model.collection.delete_many({'sender_id': client_id})
    # Remove reviews
    review_model.collection.delete_many({'client_id': client_id})
    # Remove notifications
    notification_model.collection.delete_many({'user_id': client_id})
    # Remove client
    client_model.delete(client_id)
 
    log_activity(request.user['user_id'], 'admin', 'delete_client', f"Deleted client {client['name']}")
    return jsonify({'message': 'Client removed permanently'}), 200
@app.route('/api/admin/trainers/<trainer_id>', methods=['DELETE'])
@token_required
@admin_required
def admin_delete_trainer(trainer_id):
    """Permanently remove trainer"""
    trainer = trainer_model.find_by_id(trainer_id)
    if not trainer:
        return jsonify({'error': 'Trainer not found'}), 404
 
    # Reassign clients (remove assignments)
    assignment_model.collection.update_many(
        {'trainer_id': trainer_id, 'status': 'active'},
        {'$set': {'status': 'removed', 'ended_at': datetime.utcnow()}}
    )
    # Remove sessions
    session_model.collection.delete_many({'trainer_id': trainer_id})
    # Remove reviews
    review_model.collection.delete_many({'trainer_id': trainer_id})
    # Remove trainer
    trainer_model.delete(trainer_id)
 
    log_activity(request.user['user_id'], 'admin', 'delete_trainer', f"Deleted trainer {trainer['name']}")
    return jsonify({'message': 'Trainer removed permanently'}), 200
 
 
# ─── PATCH 7: DELETE SESSION ───
 

 
 
# ─── PATCH 8: ASSIGN PACKAGE TO CLIENT ───
 
@app.route('/api/admin/clients/<client_id>/assign-package', methods=['POST'])
@token_required
@admin_required
def admin_assign_package(client_id):
    """Assign a package to a client (creates subscription)"""
    data = request.get_json() or {}
    package_id = data.get('package_id')
 
    if not package_id:
        return jsonify({'error': 'package_id required'}), 400
 
    client = client_model.find_by_id(client_id)
    package = package_model.find_by_id(package_id)
 
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    if not package:
        return jsonify({'error': 'Package not found'}), 404
 
    # Deactivate existing subscription
    subscription_model.deactivate_existing(client_id)
 
    # Create new subscription
    sub = subscription_model.create(client_id, package_id, package, request.user['user_id'])
 
    # Notify client
    send_notification_with_channels(
        client,
        f"Package Assigned: {package['title']}",
        f"You have been enrolled in the '{package['title']}' package — {package['sessions_count']} sessions over {package['duration_weeks']} weeks.",
        'success',
        "/client/dashboard"
    )
 
    log_activity(request.user['user_id'], 'admin', 'assign_package', f"Assigned package '{package['title']}' to {client['name']}")
    return jsonify({'message': 'Package assigned', 'subscription': sub}), 201
 
 
# ─── PATCH 9: LIST ALL SUBSCRIPTIONS ───
 
@app.route('/api/admin/subscriptions', methods=['GET'])
@token_required
@admin_required
def admin_get_subscriptions():
    """Get all active subscriptions with client and package details"""
    subs = subscription_model.get_all_active()
 
    for sub in subs:
        client = client_model.find_by_id(sub['client_id'])
        sub['client_name'] = client['name'] if client else '—'
 
    return jsonify({'items': subs}), 200
 
 
# ─── PATCH 10: SESSION GET WITH STATUS FILTER ───
# Update existing admin_get_sessions to support status filter:
# Add:  if status: query['status'] = status
# In the find() call.
 
@app.route('/api/admin/sessions/filtered', methods=['GET'])
@token_required
@admin_required
def admin_get_sessions_filtered():
    """Get sessions with optional status filter"""
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    client_id = request.args.get('client_id')
 
    query = {}
    if status:
        query['status'] = status
    if client_id:
        query['client_id'] = client_id
 
    skip = (page - 1) * per_page
    raw_sessions = list(session_model.collection.find(query).sort('scheduled_at', -1).skip(skip).limit(per_page))
    total = session_model.collection.count_documents(query)
 
    from models import serialize_doc
    result = []
    for s in raw_sessions:
        s = serialize_doc(s)
        s['client'] = client_model.find_by_id(s['client_id'])
        s['trainer'] = trainer_model.find_by_id(s['trainer_id'])
        result.append(s)
 
    return jsonify({
        'items': result,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    }), 200
 
 
# ─── PATCH 11: FIXED ATTENDANCE MARKING ───
# Replace the existing trainer mark_attendance route with this:
 
@app.route('/api/trainer/sessions/<session_id>/attendance', methods=['PUT'])
@token_required
@trainer_required
def trainer_mark_attendance(session_id):
    """Mark session attendance - updates session status AND increments subscription count"""
    trainer_id = request.user['user_id']
 
    session = session_model.find_by_id(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
 
    if session['trainer_id'] != str(trainer_id):
        return jsonify({'error': 'Not your session'}), 403
 
    if session.get('attendance_marked'):
        return jsonify({'error': 'Attendance already marked'}), 400
 
    if session['status'] != 'scheduled':
        return jsonify({'error': 'Session is not in scheduled state'}), 400
 
    # Mark attendance on the session
    session_model.mark_attendance(session_id)
    # Update session status to completed
    session_model.update_status(session_id, 'completed', trainer_id)
 
    # Update subscription completed count
    subscription = subscription_model.get_active(session['client_id'])
    if subscription:
        subscription_model.increment_completed(session['client_id'])
 
    # Notify client
    client = client_model.find_by_id(session['client_id'])
    if client:
        # Get updated subscription for progress
        updated_sub = subscription_model.get_active(session['client_id'])
        pending = updated_sub['pending_sessions'] if updated_sub else '?'
        completed = updated_sub['completed_sessions'] if updated_sub else '?'
        total = updated_sub['total_sessions'] if updated_sub else '?'
 
        send_notification_with_channels(
            client,
            f"Session Completed: {session['title']}",
            f"Your session '{session['title']}' has been marked complete. Progress: {completed}/{total} sessions done, {pending} remaining.",
            'success',
            "/client/sessions"
        )
 
    # Notify admin
    notify_admin(
        f"Session Attended: {session['title']}",
        f"Trainer marked attendance for session with client {client['name'] if client else ''}.",
        'session'
    )
 
    log_activity(trainer_id, 'trainer', 'mark_attendance', f"Marked attendance for session '{session['title']}'")
 
    return jsonify({'message': 'Attendance marked, session completed'}), 200
 
 
# ─── PATCH 12: PACKAGES WITH FILTER (update existing admin_get_packages) ───
 
@app.route('/api/admin/packages/all', methods=['GET'])
@token_required
@admin_required
def admin_get_all_packages():
    """Get all packages (active + inactive) for admin"""
    data = package_model.get_all()
    # Add enrollment counts
    for pkg in data.get('items', data if isinstance(data, list) else []):
        pkg['enrolled_count'] = subscription_model.count({'package_id': pkg['_id'], 'status': 'active'})
    return jsonify(data), 200
 
 
@app.route('/api/admin/packages/<package_id>', methods=['DELETE'])
@token_required
@admin_required
def admin_delete_package(package_id):
    """Delete a package (only if no active subscriptions)"""
    count = subscription_model.count({'package_id': package_id, 'status': 'active'})
    if count > 0:
        return jsonify({'error': f'Cannot delete: {count} active subscriptions exist'}), 400
 
    package_model.delete(package_id)
    return jsonify({'message': 'Package deleted'}), 200
 
 
# ─── PATCH 13: CLIENT STATS FOR TRAINER DASHBOARD ───
 
@app.route('/api/trainer/clients/<client_id>/progress', methods=['GET'])
@token_required
@trainer_required
def trainer_client_progress(client_id):
    """Get client's session progress for trainer view"""
    trainer_id = request.user['user_id']
 
    # Verify this trainer is assigned to this client
    assignment = assignment_model.get_client_trainer(client_id)
    if not assignment or assignment['trainer_id'] != str(trainer_id):
        return jsonify({'error': 'Not your client'}), 403
 
    subscription = subscription_model.get_active(client_id)
    sessions = session_model.get_client_sessions(client_id)
 
    return jsonify({
        'subscription': subscription,
        'sessions': sessions
    }), 200
 
 
# ─── PATCH 14: CLIENT SELF-VIEW PROGRESS ───
 
@app.route('/api/client/progress', methods=['GET'])
@token_required
@client_required
def client_get_progress():
    """Client's own session/package progress"""
    client_id = request.user['user_id']
 
    subscription = subscription_model.get_active(client_id)
    sessions = session_model.get_client_sessions(client_id)
    upcoming = session_model.get_upcoming_sessions(client_id, 'client', 5)
 
    return jsonify({
        'subscription': subscription,
        'sessions': sessions,
        'upcoming': upcoming,
        'total_completed': len([s for s in sessions if s.get('attendance_marked')]),
        'total_scheduled': len([s for s in sessions if s['status'] == 'scheduled'])
    }), 200



@app.route('/api/admin/trainers/<trainer_id>/unblock', methods=['PUT'])
@token_required
@admin_required
def admin_unblock_trainer(trainer_id):
    """Unblock trainer account"""
    trainer = trainer_model.find_by_id(trainer_id)
    if not trainer:
        return jsonify({'error': 'Trainer not found'}), 404
 
    trainer_model.approve(trainer_id, request.user['user_id'])
 
    send_notification_with_channels(
        trainer,
        "Account Unblocked",
        "Your SattvaFlow trainer account has been unblocked.",
        'success',
        "/trainer/dashboard"
    )
    return jsonify({'message': 'Trainer unblocked'}), 200
 

@app.route('/api/admin/clients/<client_id>/block', methods=['PUT'])
@token_required
@admin_required
def admin_block_client(client_id):
    """Block client"""
    client = client_model.find_by_id(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    client_model.block(client_id)
    
    send_notification_with_channels(
        client,
        "Account Blocked",
        "Your account has been blocked. Please contact admin.",
        'error',
        "/login"
    )
    
    return jsonify({'message': 'Client blocked'}), 200

@app.route('/api/admin/assignments', methods=['GET'])
@token_required
@admin_required
def admin_get_assignments():
    """Get all active assignments"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    result = assignment_model.get_all_active(page, per_page)
    
    # Add trainer and client details
    for assignment in result['items']:
        trainer = trainer_model.find_by_id(assignment['trainer_id'])
        client = client_model.find_by_id(assignment['client_id'])
        assignment['trainer'] = trainer
        assignment['client'] = client
    
    return jsonify(result), 200

@app.route('/api/admin/assignments', methods=['POST'])
@token_required
@admin_required
def admin_create_assignment():
    """Assign client to trainer"""
    data = request.get_json() or {}
    trainer_id = data.get('trainer_id')
    client_id = data.get('client_id')
    
    if not trainer_id or not client_id:
        return jsonify({'error': 'trainer_id and client_id required'}), 400
    
    trainer = trainer_model.find_by_id(trainer_id)
    client = client_model.find_by_id(client_id)
    
    if not trainer or not client:
        return jsonify({'error': 'Trainer or client not found'}), 404
    
    if trainer.get('status') != 'active':
        return jsonify({'error': 'Trainer is not active'}), 400
    
    if client.get('status') != 'active':
        return jsonify({'error': 'Client is not active'}), 400
    
    # Check if already assigned
    existing = assignment_model.get_client_trainer(client_id)
    if existing:
        return jsonify({'error': 'Client already has an assigned trainer. Use reassign.'}), 400
    
    assignment = assignment_model.assign(trainer_id, client_id, request.user['user_id'])
    
    # Notify trainer
    send_notification_with_channels(
        trainer,
        "New Client Assigned",
        f"You have been assigned a new client: {client['name']}. Please create a personalized yoga plan for them.",
        'assignment',
        f"/trainer/clients/{client_id}"
    )
    
    # Notify client
    send_notification_with_channels(
        client,
        "Trainer Assigned",
        f"Your trainer is {trainer['name']} (Specialization: {trainer.get('specialization', 'General')}). They will create your yoga plan soon.",
        'assignment',
        "/client/trainer"
    )
    
    log_activity(request.user['user_id'], 'admin', 'create_assignment', f"Assigned {client['name']} to {trainer['name']}")
    
    return jsonify({'message': 'Assignment created', 'assignment': assignment}), 201

@app.route('/api/admin/assignments/reassign', methods=['PUT'])
@token_required
@admin_required
def admin_reassign():
    """Reassign client to different trainer"""
    data = request.get_json() or {}
    client_id = data.get('client_id')
    new_trainer_id = data.get('new_trainer_id')
    
    if not client_id or not new_trainer_id:
        return jsonify({'error': 'client_id and new_trainer_id required'}), 400
    
    # Get old assignment
    old_assignment = assignment_model.get_client_trainer(client_id)
    if not old_assignment:
        return jsonify({'error': 'Client has no active assignment'}), 404
    
    old_trainer = trainer_model.find_by_id(old_assignment['trainer_id'])
    new_trainer = trainer_model.find_by_id(new_trainer_id)
    client = client_model.find_by_id(client_id)
    
    if not new_trainer or new_trainer.get('status') != 'active':
        return jsonify({'error': 'New trainer not found or inactive'}), 400
    
    # Create new assignment
    new_assignment = assignment_model.assign(new_trainer_id, client_id, request.user['user_id'])
    
    # Notify old trainer
    if old_trainer:
        send_notification_with_channels(
            old_trainer,
            "Client Reassigned",
            f"Client {client['name']} has been reassigned to another trainer.",
            'assignment',
            "/trainer/clients"
        )
    
    # Notify new trainer
    send_notification_with_channels(
        new_trainer,
        "New Client Assigned",
        f"Client {client['name']} has been reassigned to you.",
        'assignment',
        f"/trainer/clients/{client_id}"
    )
    
    # Notify client
    send_notification_with_channels(
        client,
        "Trainer Changed",
        f"Your trainer has been changed to {new_trainer['name']}.",
        'assignment',
        "/client/trainer"
    )
    
    log_activity(request.user['user_id'], 'admin', 'reassign_client', f"Reassigned {client['name']} from {old_trainer['name'] if old_trainer else 'Unknown'} to {new_trainer['name']}")
    
    return jsonify({'message': 'Client reassigned successfully', 'assignment': new_assignment}), 200

@app.route('/api/admin/sessions', methods=['GET'])
@token_required
@admin_required
def admin_get_sessions():
    """Get all sessions with optional status filter"""
    from models import serialize_doc
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    status = request.args.get('status')  # FIX: support status filter

    query = {}
    if status:
        query['status'] = status

    skip = (page - 1) * per_page
    # FIX: call serialize_doc on each raw MongoDB document so ObjectId/_id/datetime are JSON-safe
    raw_sessions = list(session_model.collection.find(query).sort('scheduled_at', -1).skip(skip).limit(per_page))
    total = session_model.collection.count_documents(query)

    result = []
    for s in raw_sessions:
        s = serialize_doc(s)  # FIX: serialize before adding nested objects
        s['client'] = client_model.find_by_id(s.get('client_id'))
        s['trainer'] = trainer_model.find_by_id(s.get('trainer_id'))
        result.append(s)

    return jsonify({
        'items': result,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    }), 200

@app.route('/api/admin/sessions', methods=['POST'])
@token_required
@admin_required
def admin_create_session():
    """Create a session (admin only)"""
    data = request.get_json() or {}
    
    required = ['client_id', 'trainer_id', 'title', 'scheduled_at']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    client = client_model.find_by_id(data['client_id'])
    trainer = trainer_model.find_by_id(data['trainer_id'])
    
    if not client or not trainer:
        return jsonify({'error': 'Client or trainer not found'}), 404
    
    session = session_model.create(data, request.user['user_id'])
    
    # Notify client
    send_notification_with_channels(
        client,
        f"New Session: {data['title']}",
        f"A new session has been scheduled for you on {data['scheduled_at']}",
        'session',
        "/client/sessions"
    )
    
    # Notify trainer
    send_notification_with_channels(
        trainer,
        f"New Session: {data['title']}",
        f"A new session has been scheduled with client {client['name']} on {data['scheduled_at']}",
        'session',
        "/trainer/sessions"
    )
    
    log_activity(request.user['user_id'], 'admin', 'create_session', f"Created session '{data['title']}' for {client['name']}")
    
    return jsonify({'message': 'Session created', 'session': session}), 201

@app.route('/api/admin/sessions/<session_id>', methods=['PUT'])
@token_required
@admin_required
def admin_update_session(session_id):
    """Update session details"""
    data = request.get_json() or {}
    session_model.update(session_id, data)
    
    session = session_model.find_by_id(session_id)
    if session:
        client = client_model.find_by_id(session['client_id'])
        trainer = trainer_model.find_by_id(session['trainer_id'])
        
        if client:
            send_notification_with_channels(
                client,
                "Session Updated",
                f"Your session '{session['title']}' has been updated.",
                'session',
                "/client/sessions"
            )
        
        if trainer:
            send_notification_with_channels(
                trainer,
                "Session Updated",
                f"Session '{session['title']}' with {client['name'] if client else 'client'} has been updated.",
                'session',
                "/trainer/sessions"
            )
    
    return jsonify({'message': 'Session updated'}), 200

@app.route('/api/admin/sessions/<session_id>', methods=['DELETE'])
@token_required
@admin_required
def admin_delete_session(session_id):
    """Delete/cancel session — notifies client & trainer, decrements subscription if completed"""
    session = session_model.find_by_id(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    client = client_model.find_by_id(session['client_id'])
    trainer = trainer_model.find_by_id(session['trainer_id'])

    # Decrement subscription count if session was already completed
    if session.get('status') == 'completed' and session.get('attendance_marked'):
        subscription_model.decrement_completed(session['client_id'])

    # Notify client
    if client:
        send_notification_with_channels(
            client,
            "Session Cancelled",
            f"Your session '{session['title']}' has been cancelled.",
            'error',
            "/client/sessions"
        )

    # Notify trainer
    if trainer:
        send_notification_with_channels(
            trainer,
            "Session Cancelled",
            f"Session '{session['title']}' with {client['name'] if client else 'client'} has been cancelled.",
            'error',
            "/trainer/sessions"
        )

    session_model.delete(session_id)
    return jsonify({'message': 'Session deleted'}), 200

@app.route('/api/admin/packages', methods=['GET'])
@token_required
@admin_required
def admin_get_packages():
    """Get all packages"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    
    if active_only:
        packages = package_model.get_active()
        return jsonify(packages), 200
    
    result = package_model.get_all(page, per_page)
    return jsonify(result), 200

@app.route('/api/admin/packages', methods=['POST'])
@token_required
@admin_required
def admin_create_package():
    """Create a new package/offer"""
    data = request.get_json() or {}

    if not data.get('title'):
        return jsonify({'error': 'Package title required'}), 400

    duration_weeks = int(data.get('duration_weeks', 0))
    sessions_per_week = int(data.get('sessions_per_week', 0))
    sessions_count = int(data.get('sessions_count', 0))

    if duration_weeks < 1:
        return jsonify({'error': 'duration_weeks must be ≥ 1'}), 400
    if sessions_per_week < 1 and sessions_count < 1:
        return jsonify({'error': 'Provide sessions_per_week or sessions_count'}), 400

    package = package_model.create(data, request.user['user_id'])
    
    # Notify all active clients and trainers about new package
    all_clients = client_model.get_all('active')
    all_trainers = trainer_model.get_all('active')
    
    all_user_ids = []
    for client in all_clients['items']:
        all_user_ids.append(client['_id'])
    for trainer in all_trainers['items']:
        all_user_ids.append(trainer['_id'])
    
    notification_model.broadcast(
        all_user_ids,
        f"New Package Available: {package['title']}",
        f"Check out our new package: {package['description'][:100]}",
        'package',
        "/packages"
    )
    
    log_activity(request.user['user_id'], 'admin', 'create_package', f"Created package '{package['title']}'")
    
    return jsonify({'message': 'Package created', 'package': package}), 201

@app.route('/api/admin/packages/<package_id>', methods=['PUT'])
@token_required
@admin_required
def admin_update_package(package_id):
    """Update package — recomputes sessions_count when sessions_per_week/duration_weeks change"""
    data = request.get_json() or {}

    # Recompute derived fields if both driving fields are present
    spw = data.get('sessions_per_week')
    dw  = data.get('duration_weeks')
    if spw is not None and dw is not None:
        data['sessions_count'] = int(spw) * int(dw)
    elif spw is not None:
        pkg = package_model.find_by_id(package_id)
        if pkg:
            data['sessions_count'] = int(spw) * int(pkg.get('duration_weeks', 1))

    package_model.update(package_id, data)
    return jsonify({'message': 'Package updated'}), 200

@app.route('/api/admin/packages/<package_id>/toggle', methods=['PUT'])
@token_required
@admin_required
def admin_toggle_package(package_id):
    """Toggle package active status"""
    package_model.toggle_active(package_id)
    
    return jsonify({'message': 'Package status toggled'}), 200


@app.route('/api/admin/queries', methods=['GET'])
@token_required
@admin_required
def admin_get_queries():
    """Get all queries"""
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    result = query_model.get_all(status, page, per_page)
    
    # Add sender details
    for query in result['items']:
        sender, role = get_user_by_id(query['sender_id'])
        query['sender'] = sender
    
    return jsonify(result), 200

@app.route('/api/admin/queries/<query_id>/respond', methods=['POST', 'PUT'])
@token_required
@admin_required
def admin_respond_query(query_id):
    """Respond to a query"""
    data = request.get_json() or {}
    response = data.get('response', '').strip()
    
    if not response:
        return jsonify({'error': 'Response required'}), 400
    
    query = query_model.find_by_id(query_id)
    if not query:
        return jsonify({'error': 'Query not found'}), 404
    
    query_model.respond(query_id, response, request.user['user_id'])
    
    # Notify sender
    sender, role = get_user_by_id(query['sender_id'])
    if sender:
        send_notification_with_channels(
            sender,
            f"Response to your query: {query['subject']}",
            response[:200],
            'query',
            "/queries"
        )
    
    log_activity(request.user['user_id'], 'admin', 'respond_query', f"Responded to query '{query['subject']}'")
    
    return jsonify({'message': 'Response sent'}), 200

@app.route('/api/admin/reviews', methods=['GET'])
@token_required
@admin_required
def admin_get_reviews():
    """Get pending reviews"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    result = review_model.get_pending(page, per_page)
    
    # Add client and trainer details
    for review in result['items']:
        review['client'] = client_model.find_by_id(review['client_id'])
        review['trainer'] = trainer_model.find_by_id(review['trainer_id'])
    
    return jsonify(result), 200

@app.route('/api/admin/reviews/<review_id>/approve', methods=['PUT'])
@token_required
@admin_required
def admin_approve_review(review_id):
    """Approve a review"""
    review = review_model.find_by_id(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    review_model.approve(review_id)
    
    # Update trainer rating
    trainer_model.update_rating(review['trainer_id'])
    
    # Notify trainer
    trainer = trainer_model.find_by_id(review['trainer_id'])
    if trainer:
        send_notification_with_channels(
            trainer,
            "New Review Approved",
            f"A client has given you a {review['rating']}-star review!",
            'review',
            f"/trainer/reviews"
        )
    
    log_activity(request.user['user_id'], 'admin', 'approve_review', f"Approved review for trainer {review['trainer_id']}")
    
    return jsonify({'message': 'Review approved'}), 200

@app.route('/api/admin/reviews/<review_id>/reject', methods=['PUT'])
@token_required
@admin_required
def admin_reject_review(review_id):
    """Reject a review"""
    review_model.reject(review_id)
    
    return jsonify({'message': 'Review rejected'}), 200

@app.route('/api/admin/messages', methods=['GET'])
@token_required
@admin_required
def admin_get_messages():
    """Get admin's message conversations"""
    admin_id = get_admin()['_id']
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    result = message_model.get_inbox(admin_id, page, per_page)
    
    # Add user details for each conversation
    for conv in result['items']:
        other_user_id = conv['_id']
        user, role = get_user_by_id(other_user_id)
        if user:
            conv['other_user'] = user
            conv['other_user_role'] = role
    
    return jsonify(result), 200

@app.route('/api/admin/messages/send', methods=['POST'])
@token_required
@admin_required
def admin_send_message():
    """Send message to client or trainer"""
    data = request.get_json() or {}
    recipient_id = data.get('recipient_id')
    recipient_role = data.get('recipient_role')
    subject = data.get('subject', '').strip()
    body = data.get('body', '').strip()
    
    if not all([recipient_id, recipient_role, subject, body]):
        return jsonify({'error': 'recipient_id, recipient_role, subject, body required'}), 400
    
    admin = get_admin()
    
    message = message_model.send(
        admin['_id'], 'admin',
        recipient_id, recipient_role,
        subject, body
    )
    
    # Notify recipient
    recipient, _ = get_user_by_id(recipient_id)
    if recipient:
        send_notification_with_channels(
            recipient,
            f"New message from Admin: {subject}",
            body[:200],
            'message',
            "/messages"
        )
    
    log_activity(admin['_id'], 'admin', 'send_message', f"Sent message to {recipient_role}: {subject}")
    
    return jsonify({'message': 'Message sent', 'data': message}), 201

@app.route('/api/admin/messages/<message_id>/reply', methods=['POST'])
@token_required
@admin_required
def admin_reply_message(message_id):
    """Reply to a message"""
    data = request.get_json() or {}
    body = data.get('body', '').strip()
    
    if not body:
        return jsonify({'error': 'Body required'}), 400
    
    parent = message_model.find_by_id(message_id)
    if not parent:
        return jsonify({'error': 'Message not found'}), 404
    
    admin = get_admin()
    
    # Determine recipient
    other_id = parent['sender_id'] if parent['sender_id'] != admin['_id'] else parent['recipient_id']
    other_role = parent['sender_role'] if parent['sender_id'] == other_id else parent['recipient_role']
    
    reply = message_model.send(
        admin['_id'], 'admin',
        other_id, other_role,
        f"Re: {parent['subject']}",
        body
    )
    
    # Notify recipient
    recipient, _ = get_user_by_id(other_id)
    if recipient:
        send_notification_with_channels(
            recipient,
            f"Admin replied to your message",
            body[:200],
            'message',
            "/messages"
        )
    
    return jsonify({'message': 'Reply sent', 'data': reply}), 201

@app.route('/api/admin/broadcast', methods=['POST'])
@token_required
@admin_required
def admin_broadcast():
    """Broadcast notification to all users"""
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    message = data.get('message', '').strip()
    target_role = data.get('target_role', 'all')  # all, client, trainer
    
    if not title or not message:
        return jsonify({'error': 'Title and message required'}), 400
    
    user_ids = []
    
    if target_role in ('all', 'client'):
        clients = client_model.get_all('active')
        user_ids.extend([c['_id'] for c in clients['items']])
    
    if target_role in ('all', 'trainer'):
        trainers = trainer_model.get_all('active')
        user_ids.extend([t['_id'] for t in trainers['items']])
    
    count = notification_model.broadcast(user_ids, title, message, 'system')
    
    log_activity(request.user['user_id'], 'admin', 'broadcast', f"Broadcast to {count} users: {title}")
    
    return jsonify({'message': f'Broadcast sent to {count} users'}), 200

@app.route('/api/admin/activity', methods=['GET'])
@token_required
@admin_required
def admin_get_activity():
    """Get system activity logs"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    user_id = request.args.get('user_id')
    
    if user_id:
        result = activity_log_model.get_user_activity(user_id, page, per_page)
    else:
        skip = (page - 1) * per_page
        logs = list(activity_log_model.collection.find().sort('created_at', -1).skip(skip).limit(per_page))
        total = activity_log_model.count()
        result = {
            'items': logs,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    return jsonify(result), 200

# ==================== TRAINER ROUTES ====================

@app.route('/api/trainer/clients', methods=['GET'])
@token_required
@trainer_required
def trainer_get_clients():
    """Get trainer's assigned clients"""
    trainer_id = request.user['user_id']
    
    assignments = assignment_model.get_trainer_clients(trainer_id)
    
    clients = []
    for assignment in assignments:
        client = client_model.find_by_id(assignment['client_id'])
        if client:
            client['assignment_id'] = assignment['_id']
            client['sessions_completed'] = assignment.get('sessions_completed', 0)
            
            # Get client's plans
            client['plans'] = plan_model.get_client_plans(client['_id'])
            
            # Get upcoming sessions
            client['upcoming_sessions'] = session_model.get_upcoming_sessions(client['_id'], 'client', 5)
            
            clients.append(client)
    
    return jsonify(clients), 200

@app.route('/api/trainer/clients/<client_id>/plans', methods=['GET'])
@token_required
@trainer_required
def trainer_get_client_plans(client_id):
    """Get plans for a specific client"""
    trainer_id = request.user['user_id']
    
    # Verify client is assigned to this trainer
    assignment = assignment_model.get_client_trainer(client_id)
    if not assignment or assignment['trainer_id'] != trainer_id:
        return jsonify({'error': 'Client not assigned to you'}), 403
    
    plans = plan_model.get_client_plans(client_id)
    
    return jsonify(plans), 200

@app.route('/api/trainer/plans', methods=['GET', 'POST'])
@token_required
@trainer_required
def trainer_plans():
    trainer_id = request.user['user_id']
    
    if request.method == 'GET':
        client_id = request.args.get('client_id')
        if client_id:
            # Verify client is assigned to this trainer
            assignment = assignment_model.get_client_trainer(client_id)
            if not assignment or assignment['trainer_id'] != trainer_id:
                return jsonify({'error': 'Client not assigned to you'}), 403
            plans = plan_model.get_client_plans(client_id)
        else:
            plans = plan_model.get_trainer_plans(trainer_id)
        
        return jsonify(plans), 200
    
    # POST - Create plan
    data = request.get_json() or {}
    client_id = data.get('client_id')
    
    if not client_id or not data.get('title'):
        return jsonify({'error': 'client_id and title required'}), 400
    
    # Verify client is assigned to this trainer
    assignment = assignment_model.get_client_trainer(client_id)
    if not assignment or assignment['trainer_id'] != trainer_id:
        return jsonify({'error': 'Client not assigned to you'}), 403
    
    plan = plan_model.create(data, trainer_id)
    
    # Notify client
    client = client_model.find_by_id(client_id)
    if client:
        send_notification_with_channels(
            client,
            f"New Yoga Plan: {data['title']}",
            f"Your trainer has created a new personalized yoga plan for you.",
            'info',
            "/client/plans"
        )
    
    # Notify admin
    notify_admin(
        f"New Plan Created",
        f"Trainer created plan '{data['title']}' for client {client['name'] if client else 'Unknown'}",
        'info',
        f"/admin/plans"
    )
    
    return jsonify({'message': 'Plan created', 'plan': plan}), 201

@app.route('/api/trainer/plans/<plan_id>/progress', methods=['PUT'])
@token_required
@trainer_required
def trainer_update_plan_progress(plan_id):
    """Update plan progress"""
    data = request.get_json() or {}
    progress = data.get('progress')
    
    if progress is None:
        return jsonify({'error': 'progress required'}), 400
    
    plan = plan_model.find_by_id(plan_id)
    if not plan:
        return jsonify({'error': 'Plan not found'}), 404
    
    # Verify trainer owns this plan
    if plan['trainer_id'] != request.user['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    plan_model.update_progress(plan_id, progress)
    
    # Notify client
    client = client_model.find_by_id(plan['client_id'])
    if client:
        send_notification_with_channels(
            client,
            "Plan Progress Updated",
            f"Your plan '{plan['title']}' is now {progress}% complete!",
            'info',
            "/client/plans"
        )
    
    return jsonify({'message': 'Progress updated'}), 200

@app.route('/api/trainer/sessions', methods=['GET'])
@token_required
@trainer_required
def trainer_get_sessions():
    """Get trainer's sessions"""
    trainer_id = request.user['user_id']
    status = request.args.get('status')
    
    sessions = session_model.get_trainer_sessions(trainer_id, status)
    
    # Add client details
    for session in sessions:
        session['client'] = client_model.find_by_id(session['client_id'])
    
    return jsonify(sessions), 200



@app.route('/api/trainer/reviews', methods=['GET'])
@token_required
@trainer_required
def trainer_get_reviews():
    """Get trainer's reviews"""
    trainer_id = request.user['user_id']
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
    
    result = review_model.get_trainer_reviews(trainer_id, page, per_page)
    
    # Add client details
    for review in result['items']:
        review['client'] = client_model.find_by_id(review['client_id'])
    
    return jsonify(result), 200

@app.route('/api/trainer/queries', methods=['GET', 'POST'])
@token_required
@trainer_required
def trainer_queries():
    trainer_id = request.user['user_id']
    
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
        result = query_model.get_user_queries(trainer_id, page, per_page)
        return jsonify(result), 200
    
    # POST - Create query
    data = request.get_json() or {}
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()
    
    if not subject or not message:
        return jsonify({'error': 'Subject and message required'}), 400
    
    query = query_model.create(trainer_id, 'trainer', subject, message)
    
    # Notify admin
    notify_admin(
        f"New Query from Trainer",
        f"Subject: {subject}",
        'query',
        f"/admin/queries"
    )
    
    return jsonify({'message': 'Query sent', 'query': query}), 201

@app.route('/api/trainer/messages', methods=['GET', 'POST'])
@token_required
@trainer_required
def trainer_messages():
    trainer_id = request.user['user_id']
    admin = get_admin()
    
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
        
        result = message_model.get_inbox(trainer_id, page, per_page)
        
        # Mark messages as read
        for conv in result['items']:
            if conv.get('last_message'):
                message_model.mark_read(conv['last_message']['_id'], trainer_id)
        
        return jsonify(result), 200
    
    # POST - Send message to admin
    data = request.get_json() or {}
    subject = data.get('subject', '').strip()
    body = data.get('body', '').strip()
    
    if not subject or not body:
        return jsonify({'error': 'Subject and body required'}), 400
    
    message = message_model.send(
        trainer_id, 'trainer',
        admin['_id'], 'admin',
        subject, body
    )
    
    # Notify admin
    notify_admin(
        f"New message from Trainer",
        f"Subject: {subject}",
        'message',
        f"/admin/messages"
    )
    
    return jsonify({'message': 'Message sent', 'data': message}), 201

@app.route('/api/trainer/packages', methods=['GET'])
@token_required
@trainer_required
def trainer_get_packages():
    """Get active packages for trainers to view"""
    packages = package_model.get_active()
    return jsonify(packages), 200

# ==================== CLIENT ROUTES ====================

@app.route('/api/client/trainer', methods=['GET'])
@token_required
@client_required
def client_get_trainer():
    """Get client's assigned trainer"""
    client_id = request.user['user_id']
    
    assignment = assignment_model.get_client_trainer(client_id)
    if not assignment:
        return jsonify({'trainer': None, 'message': 'No trainer assigned yet'}), 200
    
    trainer = trainer_model.find_by_id(assignment['trainer_id'])
    if trainer:
        trainer['assignment_id'] = assignment['_id']
        trainer['sessions_completed'] = assignment.get('sessions_completed', 0)
        
        # Get trainer's reviews
        reviews = review_model.get_trainer_reviews(trainer['_id'])
        trainer['reviews'] = reviews['items']
        trainer['avg_rating'] = trainer.get('rating', 0)
        trainer['total_reviews'] = trainer.get('total_reviews', 0)
    
    return jsonify(trainer), 200

@app.route('/api/client/sessions', methods=['GET'])
@token_required
@client_required
def client_get_sessions():
    """Get client's sessions"""
    client_id = request.user['user_id']
    status = request.args.get('status')
    
    sessions = session_model.get_client_sessions(client_id, status)
    
    # Add trainer details
    for session in sessions:
        session['trainer'] = trainer_model.find_by_id(session['trainer_id'])
    
    return jsonify(sessions), 200

@app.route('/api/client/plans', methods=['GET'])
@token_required
@client_required
def client_get_plans():
    """Get client's yoga plans"""
    client_id = request.user['user_id']
    
    plans = plan_model.get_client_plans(client_id)
    
    # Add trainer details
    for plan in plans:
        plan['trainer'] = trainer_model.find_by_id(plan['trainer_id'])
    
    return jsonify(plans), 200

@app.route('/api/client/packages', methods=['GET'])
@token_required
@client_required
def client_get_packages():
    """Get active packages for clients"""
    packages = package_model.get_active()
    return jsonify(packages), 200

@app.route('/api/client/packages/<package_id>/interest', methods=['POST'])
@token_required
@client_required
def client_express_interest(package_id):
    """Express interest in a package"""
    client_id = request.user['user_id']
    client = client_model.find_by_id(client_id)
    package = package_model.find_by_id(package_id)
    
    if not package:
        return jsonify({'error': 'Package not found'}), 404
    
    package_model.express_interest(package_id, client_id, client['name'])
    
    # Notify admin
    notify_admin(
        f"Package Interest: {package['title']}",
        f"Client {client['name']} is interested in package '{package['title']}'.",
        'package',
        f"/admin/packages"
    )
    
    return jsonify({'message': 'Interest recorded. Admin will contact you soon.'}), 200

@app.route('/api/client/queries', methods=['GET', 'POST'])
@token_required
@client_required
def client_queries():
    client_id = request.user['user_id']
    
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
        result = query_model.get_user_queries(client_id, page, per_page)
        return jsonify(result), 200
    
    # POST - Create query
    data = request.get_json() or {}
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()
    
    if not subject or not message:
        return jsonify({'error': 'Subject and message required'}), 400
    
    query = query_model.create(client_id, 'client', subject, message)
    
    # Notify admin
    notify_admin(
        f"New Query from Client",
        f"Subject: {subject}",
        'query',
        f"/admin/queries"
    )
    
    return jsonify({'message': 'Query sent', 'query': query}), 201

@app.route('/api/client/messages', methods=['GET', 'POST'])
@token_required
@client_required
def client_messages():
    client_id = request.user['user_id']
    admin = get_admin()
    
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
        
        result = message_model.get_inbox(client_id, page, per_page)
        
        # Mark messages as read
        for conv in result['items']:
            if conv.get('last_message'):
                message_model.mark_read(conv['last_message']['_id'], client_id)
        
        return jsonify(result), 200
    
    # POST - Send message to admin
    data = request.get_json() or {}
    subject = data.get('subject', '').strip()
    body = data.get('body', '').strip()
    
    if not subject or not body:
        return jsonify({'error': 'Subject and body required'}), 400
    
    message = message_model.send(
        client_id, 'client',
        admin['_id'], 'admin',
        subject, body
    )
    
    # Notify admin
    notify_admin(
        f"New message from Client",
        f"Subject: {subject}",
        'message',
        f"/admin/messages"
    )
    
    return jsonify({'message': 'Message sent', 'data': message}), 201

@app.route('/api/client/reviews', methods=['GET', 'POST'])
@token_required
@client_required
def client_reviews():
    client_id = request.user['user_id']
    
    if request.method == 'GET':
        reviews = review_model.get_client_reviews(client_id)
        return jsonify(reviews), 200
    
    # POST - Create review
    data = request.get_json() or {}
    rating = data.get('rating')
    comment = data.get('comment', '').strip()
    
    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    # Get assigned trainer
    assignment = assignment_model.get_client_trainer(client_id)
    if not assignment:
        return jsonify({'error': 'No trainer assigned. Cannot submit review.'}), 400
    
    trainer_id = assignment['trainer_id']
    
    # Check if already reviewed
    if review_model.has_reviewed(client_id, trainer_id):
        return jsonify({'error': 'You have already reviewed this trainer'}), 400
    
    review = review_model.create(client_id, trainer_id, rating, comment)
    
    # Notify admin
    notify_admin(
        f"New Review Pending Approval",
        f"Client has submitted a {rating}-star review for trainer.",
        'review',
        f"/admin/reviews"
    )
    
    return jsonify({'message': 'Review submitted. Pending admin approval.', 'review': review}), 201

# ==================== NOTIFICATION ROUTES ====================

@app.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications():
    """Get user notifications"""
    user_id = request.user['user_id']
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    result = notification_model.get_user_notifications(user_id, unread_only, page, per_page)
    
    return jsonify(result), 200

@app.route('/api/notifications/<notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    user_id = request.user['user_id']
    notification_model.mark_read(notification_id, user_id)
    
    return jsonify({'message': 'Marked as read'}), 200

@app.route('/api/notifications/read-all', methods=['PUT'])
@token_required
def mark_all_notifications_read():
    """Mark all notifications as read"""
    user_id = request.user['user_id']
    count = notification_model.mark_all_read(user_id)
    
    return jsonify({'message': f'{count} notifications marked as read'}), 200

@app.route('/api/notifications/unread-count', methods=['GET'])
@token_required
def get_unread_count():
    """Get unread notification count"""
    user_id = request.user['user_id']
    count = notification_model.collection.count_documents({'user_id': user_id, 'read': False})
    
    return jsonify({'unread_count': count}), 200

# ==================== PUBLIC ROUTES ====================

@app.route('/api/public/packages', methods=['GET'])
def public_packages():
    """Get active packages for public view"""
    packages = package_model.get_active()
    return jsonify(packages), 200

@app.route('/api/public/trainers', methods=['GET'])
def public_trainers():
    """Get featured trainers for public view"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 8))
    
    result = trainer_model.get_all('active', page, per_page)
    
    # Simplify for public view
    for trainer in result['items']:
        trainer.pop('phone', None)
        trainer.pop('email', None)
        trainer.pop('google_id', None)
    
    return jsonify(result), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        mongo_client.admin.command('ping')
        db_status = 'connected'
    except Exception as e:
        db_status = f'disconnected: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5000, host='0.0.0.0')