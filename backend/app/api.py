from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Artist, Venue, Booking, Event
from datetime import datetime
import jwt
from functools import wraps
import os

api_bp = Blueprint('api', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'), algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@api_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 409
    user = User(email=data['email'], name=data.get('name', ''))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    token = jwt.encode({'user_id': user.id}, os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'), algorithm='HS256')
    return jsonify({'token': token, 'user': user.to_dict()}), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = jwt.encode({'user_id': user.id}, os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'), algorithm='HS256')
    return jsonify({'token': token, 'user': user.to_dict()})

@api_bp.route('/users/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify(current_user.to_dict())

@api_bp.route('/artists', methods=['GET'])
def get_artists():
    return jsonify([a.to_dict() for a in Artist.query.all()])

@api_bp.route('/artists', methods=['POST'])
@token_required
def create_artist(current_user):
    data = request.get_json()
    artist = Artist(user_id=current_user.id, name=data.get('name'), genre=data.get('genre'),
                    bio=data.get('bio'), hourly_rate=data.get('hourly_rate'),
                    availability=data.get('availability', {}))
    db.session.add(artist)
    db.session.commit()
    return jsonify(artist.to_dict()), 201

@api_bp.route('/artists/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    return jsonify(Artist.query.get_or_404(artist_id).to_dict())

@api_bp.route('/venues', methods=['GET'])
def get_venues():
    return jsonify([v.to_dict() for v in Venue.query.all()])

@api_bp.route('/venues', methods=['POST'])
@token_required
def create_venue(current_user):
    data = request.get_json()
    venue = Venue(user_id=current_user.id, name=data.get('name'), address=data.get('address'),
                 capacity=data.get('capacity'), description=data.get('description'))
    db.session.add(venue)
    db.session.commit()
    return jsonify(venue.to_dict()), 201

@api_bp.route('/venues/<int:venue_id>', methods=['GET'])
def get_venue(venue_id):
    return jsonify(Venue.query.get_or_404(venue_id).to_dict())

@api_bp.route('/bookings', methods=['GET'])
@token_required
def get_bookings(current_user):
    if current_user.role == 'admin':
        bookings = Booking.query.all()
    else:
        bookings = Booking.query.filter_by(client_id=current_user.id).all()
    return jsonify([b.to_dict() for b in bookings])

@api_bp.route('/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    data = request.get_json()
    artist = Artist.query.get(data.get('artist_id'))
    venue = Venue.query.get(data.get('venue_id'))
    if not artist or not venue:
        return jsonify({'error': 'Artist or venue not found'}), 404
    total_price = artist.hourly_rate * data.get('hours', 2.0)
    booking = Booking(artist_id=artist.id, venue_id=venue.id, client_id=current_user.id,
                     event_name=data.get('event_name'),
                     event_date=datetime.fromisoformat(data.get('event_date')),
                     hours=data.get('hours', 2.0), total_price=total_price,
                     status='pending', notes=data.get('notes'))
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201

@api_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@token_required
def get_booking(current_user, booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if current_user.role != 'admin' and booking.client_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(booking.to_dict())

@api_bp.route('/bookings/<int:booking_id>', methods=['PUT'])
@token_required
def update_booking(current_user, booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if current_user.role != 'admin' and booking.client_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    if 'status' in data:
        booking.status = data['status']
    if 'notes' in data:
        booking.notes = data['notes']
    if 'event_date' in data:
        booking.event_date = datetime.fromisoformat(data['event_date'])
    db.session.commit()
    return jsonify(booking.to_dict())
