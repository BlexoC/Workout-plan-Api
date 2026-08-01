from datetime import datetime

from flask import request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from config import app, db
from models import User, WorkoutLog


def parse_date(value):
    """Convert an ISO date string (YYYY-MM-DD) to a date object, or return
    the value unchanged if it's already a date / None."""
    if not value or not isinstance(value, str):
        return value
    return datetime.strptime(value, '%Y-%m-%d').date()


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {'error': 'Username and password are required'}, 422

    if User.query.filter_by(username=username).first():
        return {'error': 'Username is already taken'}, 422

    try:
        user = User(username=username)
        user.password_hash = password
        db.session.add(user)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {'error': str(e)}, 422

    access_token = create_access_token(identity=str(user.id))
    return {'user': user.to_dict(), 'access_token': access_token}, 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.authenticate(password):
        return {'error': 'Invalid username or password'}, 401

    access_token = create_access_token(identity=str(user.id))
    return {'user': user.to_dict(), 'access_token': access_token}, 200


@app.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return {'error': 'User not found'}, 404
    return user.to_dict(), 200



@app.route('/workout_logs', methods=['GET', 'POST'])
@jwt_required()
def workout_logs():
    user_id = int(get_jwt_identity())

    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)

        pagination = (
            WorkoutLog.query.filter_by(user_id=user_id)
            .order_by(WorkoutLog.date.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            'workout_logs': [log.to_dict() for log in pagination.items],
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
        }, 200

    # POST
    data = request.get_json() or {}
    try:
        log = WorkoutLog(
            title=data.get('title'),
            category=data.get('category'),
            duration_minutes=data.get('duration_minutes'),
            date=parse_date(data.get('date')) or datetime.today().date(),
            notes=data.get('notes'),
            user_id=user_id,
        )
        db.session.add(log)
        db.session.commit()
    except (ValueError, TypeError) as e:
        db.session.rollback()
        return {'error': str(e)}, 422

    return log.to_dict(), 201


@app.route('/workout_logs/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def workout_log_by_id(id):
    user_id = int(get_jwt_identity())
    
    log = WorkoutLog.query.filter_by(id=id, user_id=user_id).first()

    if not log:
        return {'error': 'Workout log not found'}, 404

    if request.method == 'GET':
        return log.to_dict(), 200

    if request.method == 'PATCH':
        data = request.get_json() or {}
        try:
            for attr in ['title', 'category', 'duration_minutes', 'notes']:
                if attr in data:
                    setattr(log, attr, data[attr])
            if 'date' in data:
                log.date = parse_date(data['date'])
            db.session.commit()
        except (ValueError, TypeError) as e:
            db.session.rollback()
            return {'error': str(e)}, 422
        return log.to_dict(), 200

    
    db.session.delete(log)
    db.session.commit()
    return {}, 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)
