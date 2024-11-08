from flask import Blueprint, request, jsonify
from models import db, Room, Guest, Booking, User
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{'id': room.id, 'number': room.number, 'status': room.status} for room in rooms])

@main.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    room = Room.query.filter_by(id=data['room_id']).first()
    if room.status != 'Clean':
        return jsonify({"error": "Room not available"}), 400
    new_booking = Booking(
        guest_id=data['guest_id'],
        room_id=data['room_id'],
        check_in=datetime.strptime(data['check_in'], '%Y-%m-%d'),
        check_out=datetime.strptime(data['check_out'], '%Y-%m-%d')
    )
    db.session.add(new_booking)
    room.status = "Occupied"
    db.session.commit()
    return jsonify({"message": "Booking created successfully"}), 201

@main.route('/check_out/<int:booking_id>', methods=['POST'])
def check_out(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        room = Room.query.get(booking.room_id)
        room.status = 'Dirty'
        booking.status = 'Completed'
        db.session.commit()
        return jsonify({"message": "Checked out successfully"}), 200
    return jsonify({"error": "Booking not found"}), 404
