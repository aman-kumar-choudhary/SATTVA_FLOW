from datetime import datetime, timedelta
from bson import ObjectId
import bcrypt
import secrets
from config import Config


class MongoModel:
    @staticmethod
    def serialize(doc):
        if doc is None:
            return None
        doc['_id'] = str(doc['_id'])
        return doc


class User:
    COLLECTION = 'users'
    ROLES    = ['admin', 'trainer', 'client']
    STATUSES = ['pending', 'active', 'blocked', 'rejected']

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, data):
        user = {
            'name':        data.get('name'),
            'email':       data.get('email'),
            'phone':       data.get('phone'),
            'google_id':   data.get('google_id'),
            'picture':     data.get('picture', ''),
            'role':        data.get('role', 'client'),
            # Admin → active immediately; everyone else → pending approval
            'status':      'active' if data.get('role') == 'admin' else 'pending',
            'is_verified': True,   # Google-authenticated users are always verified
            'created_at':  datetime.utcnow(),
            'updated_at':  datetime.utcnow(),
            'profile':     data.get('profile', {}),
            'settings':    data.get('settings', {})
        }

        if data.get('role') == 'trainer':
            user['trainer_details'] = {
                'specialization': data.get('specialization', ''),
                'experience':     data.get('experience', 0),
                'certifications': data.get('certifications', []),
                'bio':            data.get('bio', ''),
                'rating':         0,
                'total_ratings':  0,
                'approved_by':    None,
                'approved_at':    None
            }

        result = self.collection.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return user

    def find_by_email(self, email):
        user = self.collection.find_one({'email': email})
        return MongoModel.serialize(user)

    def find_by_google_id(self, google_id):
        user = self.collection.find_one({'google_id': google_id})
        return MongoModel.serialize(user)

    def find_by_phone(self, phone):
        user = self.collection.find_one({'phone': phone})
        return MongoModel.serialize(user)

    def find_by_id(self, user_id):
        user = self.collection.find_one({'_id': ObjectId(user_id)})
        return MongoModel.serialize(user)

    def update(self, user_id, data):
        data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        return result.modified_count > 0

    def get_all_trainers(self, status=None):
        query = {'role': 'trainer'}
        if status:
            query['status'] = status
        trainers = list(self.collection.find(query))
        return [MongoModel.serialize(t) for t in trainers]

    def get_all_clients(self, status=None):
        query = {'role': 'client'}
        if status:
            query['status'] = status
        clients = list(self.collection.find(query))
        return [MongoModel.serialize(c) for c in clients]


class OTP:
    """Kept for backward-compatibility; no longer used by auth routes."""
    COLLECTION = 'otps'

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, phone_or_email, otp, type='whatsapp'):
        self.collection.delete_many({'identifier': phone_or_email})
        otp_data = {
            'identifier': phone_or_email,
            'otp': otp,
            'type': type,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(seconds=Config.OTP_EXPIRY),
            'used': False
        }
        result = self.collection.insert_one(otp_data)
        return str(result.inserted_id)

    def verify(self, phone_or_email, otp):
        otp_record = self.collection.find_one({
            'identifier': phone_or_email,
            'otp': otp,
            'used': False,
            'expires_at': {'$gt': datetime.utcnow()}
        })
        if otp_record:
            self.collection.update_one(
                {'_id': otp_record['_id']},
                {'$set': {'used': True}}
            )
            return True
        return False


class Assignment:
    COLLECTION = 'assignments'

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, trainer_id, client_id):
        assignment = {
            'trainer_id': ObjectId(trainer_id),
            'client_id':  ObjectId(client_id),
            'created_at': datetime.utcnow(),
            'status':     'active',
            'sessions_completed': 0,
            'total_sessions':     0
        }
        result = self.collection.insert_one(assignment)
        return str(result.inserted_id)

    def get_client_trainer(self, client_id):
        assignment = self.collection.find_one({'client_id': ObjectId(client_id), 'status': 'active'})
        if assignment:
            assignment['_id']        = str(assignment['_id'])
            assignment['trainer_id'] = str(assignment['trainer_id'])
            assignment['client_id']  = str(assignment['client_id'])
        return assignment

    def get_trainer_clients(self, trainer_id):
        assignments = list(self.collection.find({'trainer_id': ObjectId(trainer_id), 'status': 'active'}))
        return [MongoModel.serialize(a) for a in assignments]

    def get_all_assignments(self):
        assignments = list(self.collection.find({'status': 'active'}))
        return [MongoModel.serialize(a) for a in assignments]


class Session:
    COLLECTION = 'sessions'

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, data):
        session = {
            'client_id':   ObjectId(data['client_id']),
            'trainer_id':  ObjectId(data['trainer_id']),
            'title':       data['title'],
            'description': data.get('description', ''),
            'type':        data.get('type', 'regular'),
            'scheduled_at': datetime.fromisoformat(data['scheduled_at']) if data.get('scheduled_at') else None,
            'duration':    data.get('duration', 60),
            'status':      'scheduled',
            'attended':    False,
            'notes':       data.get('notes', ''),
            'created_at':  datetime.utcnow(),
            'updated_at':  datetime.utcnow()
        }
        result = self.collection.insert_one(session)
        return str(result.inserted_id)

    def get_client_sessions(self, client_id):
        sessions = list(self.collection.find({'client_id': ObjectId(client_id)}).sort('scheduled_at', -1))
        return [MongoModel.serialize(s) for s in sessions]

    def get_trainer_sessions(self, trainer_id):
        sessions = list(self.collection.find({'trainer_id': ObjectId(trainer_id)}).sort('scheduled_at', -1))
        return [MongoModel.serialize(s) for s in sessions]

    def update_status(self, session_id, status):
        return self.collection.update_one(
            {'_id': ObjectId(session_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )


class Plan:
    COLLECTION = 'plans'

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, data):
        plan = {
            'client_id':       ObjectId(data['client_id']),
            'trainer_id':      ObjectId(data['trainer_id']),
            'title':           data['title'],
            'description':     data.get('description', ''),
            'weeks':           data.get('weeks', 4),
            'sessions_per_week': data.get('sessions_per_week', 3),
            'focus_areas':     data.get('focus_areas', []),
            'exercises':       data.get('exercises', []),
            'status':          'active',
            'progress':        0,
            'created_at':      datetime.utcnow(),
            'updated_at':      datetime.utcnow()
        }
        result = self.collection.insert_one(plan)
        return str(result.inserted_id)

    def get_client_plans(self, client_id):
        plans = list(self.collection.find({'client_id': ObjectId(client_id), 'status': 'active'}))
        return [MongoModel.serialize(p) for p in plans]

    def update_progress(self, plan_id, progress):
        return self.collection.update_one(
            {'_id': ObjectId(plan_id)},
            {'$set': {'progress': progress, 'updated_at': datetime.utcnow()}}
        )


class Query:
    COLLECTION = 'queries'

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, data):
        query = {
            'sender_id':    ObjectId(data['sender_id']),
            'sender_role':  data['sender_role'],
            'receiver_id':  ObjectId(data['receiver_id']) if data.get('receiver_id') else None,
            'receiver_role': data.get('receiver_role', 'admin'),
            'subject':      data['subject'],
            'message':      data['message'],
            'status':       'pending',
            'response':     None,
            'responded_at': None,
            'created_at':   datetime.utcnow(),
            'updated_at':   datetime.utcnow()
        }
        result = self.collection.insert_one(query)
        return str(result.inserted_id)

    def respond(self, query_id, response, responder_id):
        return self.collection.update_one(
            {'_id': ObjectId(query_id)},
            {'$set': {
                'response':     response,
                'responder_id': ObjectId(responder_id),
                'responded_at': datetime.utcnow(),
                'status':       'resolved',
                'updated_at':   datetime.utcnow()
            }}
        )

    def get_user_queries(self, user_id):
        queries = list(self.collection.find({
            '$or': [
                {'sender_id':   ObjectId(user_id)},
                {'receiver_id': ObjectId(user_id)}
            ]
        }).sort('created_at', -1))
        return [MongoModel.serialize(q) for q in queries]

    def get_all_queries(self):
        queries = list(self.collection.find().sort('created_at', -1))
        return [MongoModel.serialize(q) for q in queries]


class Review:
    COLLECTION = 'reviews'

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, data):
        review = {
            'client_id':  ObjectId(data['client_id']),
            'trainer_id': ObjectId(data['trainer_id']),
            'rating':     data['rating'],
            'comment':    data.get('comment', ''),
            'status':     'pending',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(review)
        return str(result.inserted_id)

    def approve(self, review_id):
        result = self.collection.update_one(
            {'_id': ObjectId(review_id)},
            {'$set': {'status': 'approved', 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    def reject(self, review_id):
        result = self.collection.update_one(
            {'_id': ObjectId(review_id)},
            {'$set': {'status': 'rejected', 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    def get_trainer_reviews(self, trainer_id):
        reviews = list(self.collection.find({'trainer_id': ObjectId(trainer_id), 'status': 'approved'}))
        return [MongoModel.serialize(r) for r in reviews]

    def get_pending_reviews(self):
        reviews = list(self.collection.find({'status': 'pending'}))
        return [MongoModel.serialize(r) for r in reviews]

    def get_all_approved(self):
        reviews = list(self.collection.find({'status': 'approved'}).sort('created_at', -1).limit(10))
        return [MongoModel.serialize(r) for r in reviews]


class Notification:
    COLLECTION = 'notifications'

    def __init__(self, db):
        self.db = db
        self.collection = db[self.COLLECTION]

    def create(self, user_id, title, message, type='info', metadata=None):
        notification = {
            'user_id':    ObjectId(user_id),
            'title':      title,
            'message':    message,
            'type':       type,
            'metadata':   metadata or {},
            'read':       False,
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(notification)
        return str(result.inserted_id)

    def get_user_notifications(self, user_id, unread_only=False):
        query = {'user_id': ObjectId(user_id)}
        if unread_only:
            query['read'] = False
        notifications = list(self.collection.find(query).sort('created_at', -1))
        return [MongoModel.serialize(n) for n in notifications]

    def mark_as_read(self, notification_id):
        return self.collection.update_one(
            {'_id': ObjectId(notification_id)},
            {'$set': {'read': True}}
        )

    def mark_all_read(self, user_id):
        return self.collection.update_many(
            {'user_id': ObjectId(user_id), 'read': False},
            {'$set': {'read': True}}
        )