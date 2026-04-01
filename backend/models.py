# models.py - Complete Fixed Version
from datetime import datetime, timedelta
from bson import ObjectId
from typing import Optional, List, Dict, Any
from config import Config

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    doc = dict(doc)
    for key, val in doc.items():
        if isinstance(val, ObjectId):
            doc[key] = str(val)
        elif isinstance(val, datetime):
            doc[key] = val.isoformat()
    return doc

class BaseModel:
    def __init__(self, db, collection_name):
        self.db = db
        self.collection = db[collection_name]
    
    def find_by_id(self, id_str):
        try:
            doc = self.collection.find_one({'_id': ObjectId(id_str)})
            return serialize_doc(doc)
        except:
            return None
    
    def find_by_email(self, email):
        if not email:
            return None
        doc = self.collection.find_one({'email': email.lower().strip()})
        return serialize_doc(doc)
    
    def update(self, id_str, data):
        data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(id_str)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    def delete(self, id_str):
        result = self.collection.delete_one({'_id': ObjectId(id_str)})
        return result.deleted_count > 0
    
    def count(self, filter_dict=None):
        return self.collection.count_documents(filter_dict or {})

class UserModel(BaseModel):
    """Collection: users - For ADMIN only"""
    COLLECTION = 'users'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        # Create indexes
        self.collection.create_index('email', unique=True)
        self.collection.create_index('google_id', unique=True, sparse=True)
    
    def create_admin(self, email, name, google_id=None, picture=None, phone=None):
        """Create admin user if not exists"""
        existing = self.find_by_email(email)
        if existing:
            return existing
        
        doc = {
            'name': name,
            'email': email.lower().strip(),
            'google_id': google_id,
            'picture': picture or '',
            'phone': phone or '',
            'role': 'admin',
            'status': 'active',
            'is_verified': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def get_admin(self):
        return self.find_by_email(Config.ADMIN_EMAIL)

class ClientModel(BaseModel):
    """Collection: clients - All clients only"""
    COLLECTION = 'clients'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index('email', unique=True, sparse=True)
        self.collection.create_index('google_id', unique=True, sparse=True)
        self.collection.create_index('phone', unique=True, sparse=True)
    
    def create(self, data):
        doc = {
            'name': data.get('name', ''),
            'email': data.get('email', '').lower().strip() if data.get('email') else None,
            'phone': data.get('phone'),
            'google_id': data.get('google_id'),
            'picture': data.get('picture', ''),
            'role': 'client',
            'status': 'pending',  # Admin must activate
            'is_verified': True,
            'preferences': {
                'email_notifications': True,
                'whatsapp_notifications': True
            },
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def get_all(self, status=None, page=1, per_page=20):
        query = {}
        if status:
            query['status'] = status
        
        skip = (page - 1) * per_page
        docs = list(self.collection.find(query).sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents(query)
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def activate(self, client_id):
        return self.update(client_id, {'status': 'active'})
    
    def deactivate(self, client_id):
        return self.update(client_id, {'status': 'inactive'})
    
    def block(self, client_id):
        return self.update(client_id, {'status': 'blocked'})

class TrainerModel(BaseModel):
    """Collection: trainers - All trainers only"""
    COLLECTION = 'trainers'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index('email', unique=True, sparse=True)
        self.collection.create_index('google_id', unique=True, sparse=True)
        self.collection.create_index('phone', unique=True, sparse=True)
    
    def create(self, data):
        # Handle certifications - convert string to list if needed
        certs = data.get('certifications', [])
        if isinstance(certs, str):
            certs = [c.strip() for c in certs.split(',') if c.strip()]
        
        doc = {
            'name': data.get('name', ''),
            'email': data.get('email', '').lower().strip() if data.get('email') else None,
            'phone': data.get('phone'),
            'google_id': data.get('google_id'),
            'picture': data.get('picture', ''),
            'role': 'trainer',
            'status': 'pending',  # Admin must approve
            'specialization': data.get('specialization', ''),
            'experience_years': int(data.get('experience', 0)),
            'certifications': certs,
            'bio': data.get('bio', ''),
            'rating': 0.0,
            'total_reviews': 0,
            'is_verified': True,
            'preferences': {
                'email_notifications': True,
                'whatsapp_notifications': True
            },
            'approved_by': None,
            'approved_at': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def get_all(self, status=None, page=1, per_page=20):
        query = {}
        if status:
            query['status'] = status
        
        skip = (page - 1) * per_page
        docs = list(self.collection.find(query).sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents(query)
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def approve(self, trainer_id, admin_id):
        return self.update(trainer_id, {
            'status': 'active',
            'approved_by': str(admin_id),
            'approved_at': datetime.utcnow()
        })
    
    def reject(self, trainer_id, reason):
        return self.update(trainer_id, {
            'status': 'rejected',
            'rejection_reason': reason
        })
    
    def block(self, trainer_id):
        return self.update(trainer_id, {'status': 'blocked'})
    
    def update_rating(self, trainer_id):
        """Recalculate average rating from approved reviews"""
        reviews = list(self.db['reviews'].find({
            'trainer_id': str(trainer_id),
            'status': 'approved'
        }))
        
        if reviews:
            avg = sum(r['rating'] for r in reviews) / len(reviews)
            count = len(reviews)
        else:
            avg, count = 0.0, 0
        
        self.update(trainer_id, {'rating': round(avg, 1), 'total_reviews': count})
        return avg

class AssignmentModel(BaseModel):
    """Collection: assignments - Trainer-Client assignments"""
    COLLECTION = 'assignments'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index([('client_id', 1), ('status', 1)])
        self.collection.create_index([('trainer_id', 1), ('status', 1)])
    
    def assign(self, trainer_id, client_id, admin_id):
        """Assign client to trainer"""
        # Deactivate existing assignment for this client
        self.collection.update_many(
            {'client_id': str(client_id), 'status': 'active'},
            {'$set': {'status': 'inactive', 'ended_at': datetime.utcnow()}}
        )
        
        # Create new assignment
        doc = {
            'trainer_id': str(trainer_id),
            'client_id': str(client_id),
            'assigned_by': str(admin_id),
            'status': 'active',
            'sessions_completed': 0,
            'sessions_total': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def reassign(self, client_id, new_trainer_id, admin_id):
        """Reassign client to different trainer"""
        return self.assign(new_trainer_id, client_id, admin_id)
    
    def get_client_trainer(self, client_id):
        """Get current active trainer for client"""
        doc = self.collection.find_one({
            'client_id': str(client_id),
            'status': 'active'
        })
        return serialize_doc(doc)
    
    def get_trainer_clients(self, trainer_id):
        """Get all active clients for trainer"""
        docs = list(self.collection.find({
            'trainer_id': str(trainer_id),
            'status': 'active'
        }))
        return [serialize_doc(d) for d in docs]
    
    def get_all_active(self, page=1, per_page=20):
        skip = (page - 1) * per_page
        docs = list(self.collection.find({'status': 'active'}).skip(skip).limit(per_page))
        total = self.collection.count_documents({'status': 'active'})
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def remove_assignment(self, assignment_id):
        return self.update(assignment_id, {
            'status': 'removed',
            'ended_at': datetime.utcnow()
        })

class PackageModel(BaseModel):
    """Collection: packages - Offers/Packages created by admin"""
    COLLECTION = 'packages'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
    
    def create(self, data, admin_id):
        doc = {
            'title': data.get('title'),
            'description': data.get('description', ''),
            'price': float(data.get('price', 0)),
            'currency': data.get('currency', 'INR'),
            'duration_weeks': int(data.get('duration_weeks', 4)),
            'sessions_count': int(data.get('sessions_count', 8)),
            'features': data.get('features', []),
            'is_active': data.get('is_active', True),
            'is_featured': data.get('is_featured', False),
            'created_by': str(admin_id),
            'interested_clients': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def get_active(self):
        docs = list(self.collection.find({'is_active': True}).sort('created_at', -1))
        return [serialize_doc(d) for d in docs]
    
    def get_all(self, page=1, per_page=20):
        skip = (page - 1) * per_page
        docs = list(self.collection.find().sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents({})
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def find_by_id(self, package_id):
        return super().find_by_id(package_id)
    
    def express_interest(self, package_id, client_id, client_name):
        self.collection.update_one(
            {'_id': ObjectId(package_id)},
            {'$addToSet': {
                'interested_clients': {
                    'client_id': str(client_id),
                    'client_name': client_name,
                    'expressed_at': datetime.utcnow()
                }
            }}
        )
    
    def toggle_active(self, package_id):
        pkg = self.find_by_id(package_id)
        if pkg:
            return self.update(package_id, {'is_active': not pkg.get('is_active', True)})
        return False

class SessionModel(BaseModel):
    """Collection: sessions - Only admin can create/modify"""
    COLLECTION = 'sessions'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index([('client_id', 1), ('scheduled_at', -1)])
        self.collection.create_index([('trainer_id', 1), ('scheduled_at', -1)])
    
    def create(self, data, admin_id):
        # Parse scheduled_at
        scheduled_at = data['scheduled_at']
        if isinstance(scheduled_at, str):
            scheduled_at = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        
        doc = {
            'client_id': str(data['client_id']),
            'trainer_id': str(data['trainer_id']),
            'title': data['title'],
            'description': data.get('description', ''),
            'session_type': data.get('session_type', 'regular'),
            'scheduled_at': scheduled_at,
            'duration_minutes': int(data.get('duration_minutes', 60)),
            'status': 'scheduled',
            'attendance_marked': False,
            'notes': data.get('notes', ''),
            'created_by': str(admin_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def update_status(self, session_id, status, updated_by):
        allowed_status = ['scheduled', 'completed', 'cancelled', 'rescheduled']
        if status not in allowed_status:
            raise ValueError(f"Invalid status. Allowed: {allowed_status}")
        
        return self.update(session_id, {
            'status': status,
            'updated_by': str(updated_by),
            'updated_at': datetime.utcnow()
        })
    
    def mark_attendance(self, session_id):
        return self.update(session_id, {
            'attendance_marked': True,
            'attended_at': datetime.utcnow()
        })
    
    def get_client_sessions(self, client_id, status=None):
        query = {'client_id': str(client_id)}
        if status:
            query['status'] = status
        
        docs = list(self.collection.find(query).sort('scheduled_at', -1))
        return [serialize_doc(d) for d in docs]
    
    def get_trainer_sessions(self, trainer_id, status=None):
        query = {'trainer_id': str(trainer_id)}
        if status:
            query['status'] = status
        
        docs = list(self.collection.find(query).sort('scheduled_at', -1))
        return [serialize_doc(d) for d in docs]
    
    def get_upcoming_sessions(self, user_id, user_role, limit=10):
        """Get upcoming sessions for user"""
        field = 'client_id' if user_role == 'client' else 'trainer_id'
        docs = list(self.collection.find({
            field: str(user_id),
            'status': 'scheduled',
            'scheduled_at': {'$gte': datetime.utcnow()}
        }).sort('scheduled_at', 1).limit(limit))
        return [serialize_doc(d) for d in docs]

class PlanModel(BaseModel):
    """Collection: plans - Yoga plans created by trainers"""
    COLLECTION = 'plans'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
    
    def create(self, data, trainer_id):
        doc = {
            'client_id': str(data['client_id']),
            'trainer_id': str(trainer_id),
            'title': data['title'],
            'description': data.get('description', ''),
            'weeks': int(data.get('weeks', 4)),
            'sessions_per_week': int(data.get('sessions_per_week', 3)),
            'focus_areas': data.get('focus_areas', []),
            'exercises': data.get('exercises', []),
            'status': 'active',
            'progress_percentage': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def get_client_plans(self, client_id):
        docs = list(self.collection.find({
            'client_id': str(client_id),
            'status': 'active'
        }).sort('created_at', -1))
        return [serialize_doc(d) for d in docs]
    
    def get_trainer_plans(self, trainer_id):
        docs = list(self.collection.find({
            'trainer_id': str(trainer_id),
            'status': 'active'
        }).sort('created_at', -1))
        return [serialize_doc(d) for d in docs]
    
    def update_progress(self, plan_id, progress):
        return self.update(plan_id, {
            'progress_percentage': min(100, max(0, int(progress))),
            'updated_at': datetime.utcnow()
        })

class MessageModel(BaseModel):
    """Collection: messages - ONLY admin ↔ client/trainer communication"""
    COLLECTION = 'messages'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index([('participants', 1)])
        self.collection.create_index([('created_at', -1)])
    
    def send(self, sender_id, sender_role, recipient_id, recipient_role, subject, body):
        """Send message - only between admin and client/trainer"""
        # Validate no client-trainer direct messaging
        roles = {sender_role, recipient_role}
        if 'client' in roles and 'trainer' in roles:
            raise ValueError("Direct client-trainer messaging is not permitted")
        
        doc = {
            'sender_id': str(sender_id),
            'sender_role': sender_role,
            'recipient_id': str(recipient_id),
            'recipient_role': recipient_role,
            'participants': [str(sender_id), str(recipient_id)],
            'subject': subject,
            'body': body,
            'read_by': [str(sender_id)],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def get_inbox(self, user_id, page=1, per_page=20):
        """Get all conversations for user"""
        # Get unique conversation partners
        pipeline = [
            {'$match': {'participants': str(user_id)}},
            {'$sort': {'created_at': -1}},
            {'$group': {
                '_id': {
                    '$cond': [
                        {'$eq': ['$sender_id', str(user_id)]},
                        '$recipient_id',
                        '$sender_id'
                    ]
                },
                'last_message': {'$first': '$$ROOT'},
                'unread_count': {
                    '$sum': {
                        '$cond': [
                            {'$and': [
                                {'$ne': ['$sender_id', str(user_id)]},
                                {'$not': {'$in': [str(user_id), '$read_by']}}
                            ]},
                            1, 0
                        ]
                    }
                }
            }}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        # Paginate manually
        total = len(results)
        start = (page - 1) * per_page
        paginated = results[start:start + per_page]
        
        return {
            'items': paginated,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def mark_read(self, message_id, user_id):
        return self.collection.update_one(
            {'_id': ObjectId(message_id)},
            {'$addToSet': {'read_by': str(user_id)}}
        )
    
    def get_unread_count(self, user_id):
        return self.collection.count_documents({
            'participants': str(user_id),
            'sender_id': {'$ne': str(user_id)},
            'read_by': {'$nin': [str(user_id)]}
        })

class NotificationModel(BaseModel):
    """Collection: notifications - System-wide notifications"""
    COLLECTION = 'notifications'
    
    NOTIFICATION_TYPES = ['info', 'success', 'warning', 'error', 'session', 'assignment', 
                          'message', 'package', 'registration', 'review', 'system']
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index([('user_id', 1), ('created_at', -1)])
        self.collection.create_index([('read', 1)])
    
    def create(self, user_id, title, message, ntype='info', link=None, metadata=None):
        """Create notification for specific user"""
        doc = {
            'user_id': str(user_id),
            'title': title,
            'message': message,
            'type': ntype if ntype in self.NOTIFICATION_TYPES else 'info',
            'link': link,
            'metadata': metadata or {},
            'read': False,
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def broadcast(self, user_ids, title, message, ntype='info', link=None):
        """Send notification to multiple users"""
        if not user_ids:
            return 0
        
        docs = [{
            'user_id': str(uid),
            'title': title,
            'message': message,
            'type': ntype,
            'link': link,
            'metadata': {},
            'read': False,
            'created_at': datetime.utcnow()
        } for uid in user_ids]
        
        result = self.collection.insert_many(docs)
        return len(result.inserted_ids)
    
    def get_user_notifications(self, user_id, unread_only=False, page=1, per_page=50):
        query = {'user_id': str(user_id)}
        if unread_only:
            query['read'] = False
        
        skip = (page - 1) * per_page
        docs = list(self.collection.find(query).sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents(query)
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page,
            'unread_count': self.collection.count_documents({'user_id': str(user_id), 'read': False})
        }
    
    def mark_read(self, notification_id, user_id):
        return self.collection.update_one(
            {'_id': ObjectId(notification_id), 'user_id': str(user_id)},
            {'$set': {'read': True}}
        )
    
    def mark_all_read(self, user_id):
        result = self.collection.update_many(
            {'user_id': str(user_id), 'read': False},
            {'$set': {'read': True}}
        )
        return result.modified_count

class QueryModel(BaseModel):
    """Collection: queries - Support queries from clients/trainers to admin"""
    COLLECTION = 'queries'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index([('sender_id', 1), ('created_at', -1)])
        self.collection.create_index([('status', 1)])
    
    def create(self, sender_id, sender_role, subject, message):
        doc = {
            'sender_id': str(sender_id),
            'sender_role': sender_role,
            'subject': subject,
            'message': message,
            'status': 'pending',
            'response': None,
            'responded_by': None,
            'responded_at': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def respond(self, query_id, response, admin_id):
        return self.update(query_id, {
            'response': response,
            'responded_by': str(admin_id),
            'responded_at': datetime.utcnow(),
            'status': 'resolved'
        })
    
    def get_user_queries(self, user_id, page=1, per_page=20):
        skip = (page - 1) * per_page
        docs = list(self.collection.find({'sender_id': str(user_id)}).sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents({'sender_id': str(user_id)})
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def get_all(self, status=None, page=1, per_page=20):
        query = {}
        if status:
            query['status'] = status
        
        skip = (page - 1) * per_page
        docs = list(self.collection.find(query).sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents(query)
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }

class ReviewModel(BaseModel):
    """Collection: reviews - Client reviews for trainers (admin moderated)"""
    COLLECTION = 'reviews'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index([('trainer_id', 1), ('status', 1)])
        self.collection.create_index([('client_id', 1), ('trainer_id', 1)], unique=True)
    
    def create(self, client_id, trainer_id, rating, comment):
        doc = {
            'client_id': str(client_id),
            'trainer_id': str(trainer_id),
            'rating': int(rating),
            'comment': comment,
            'status': 'pending',  # Admin must approve
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        return serialize_doc(doc)
    
    def approve(self, review_id):
        return self.update(review_id, {'status': 'approved'})
    
    def reject(self, review_id, reason=None):
        update_data = {'status': 'rejected'}
        if reason:
            update_data['rejection_reason'] = reason
        return self.update(review_id, update_data)
    
    def get_trainer_reviews(self, trainer_id, page=1, per_page=20):
        skip = (page - 1) * per_page
        docs = list(self.collection.find({
            'trainer_id': str(trainer_id),
            'status': 'approved'
        }).sort('created_at', -1).skip(skip).limit(per_page))
        
        total = self.collection.count_documents({'trainer_id': str(trainer_id), 'status': 'approved'})
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def get_pending(self, page=1, per_page=20):
        skip = (page - 1) * per_page
        docs = list(self.collection.find({'status': 'pending'}).sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents({'status': 'pending'})
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def has_reviewed(self, client_id, trainer_id):
        return self.collection.count_documents({
            'client_id': str(client_id),
            'trainer_id': str(trainer_id)
        }) > 0

class ActivityLogModel(BaseModel):
    """Collection: activity_logs - Track all system activities"""
    COLLECTION = 'activity_logs'
    
    def __init__(self, db):
        super().__init__(db, self.COLLECTION)
        self.collection.create_index([('user_id', 1)])
        self.collection.create_index([('created_at', -1)])
        self.collection.create_index([('action_type', 1)])
    
    def log(self, user_id, user_role, action_type, description, metadata=None):
        doc = {
            'user_id': str(user_id),
            'user_role': user_role,
            'action_type': action_type,
            'description': description,
            'metadata': metadata or {},
            'ip_address': None,
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(doc)
        return serialize_doc(doc)
    
    def get_user_activity(self, user_id, page=1, per_page=50):
        skip = (page - 1) * per_page
        docs = list(self.collection.find({'user_id': str(user_id)}).sort('created_at', -1).skip(skip).limit(per_page))
        total = self.collection.count_documents({'user_id': str(user_id)})
        
        return {
            'items': [serialize_doc(d) for d in docs],
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }