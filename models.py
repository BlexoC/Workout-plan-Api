from datetime import date as date_type

from sqlalchemy.orm import validates

from config import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column('password_hash', db.String, nullable=False)

    workout_logs = db.relationship(
        'WorkoutLog', backref='user', cascade='all, delete-orphan'
    )

    @property
    def password_hash(self):
        raise AttributeError('password_hash is not a readable attribute')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise ValueError('Username cannot be empty')
        return username

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'


class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=date_type.today)
    notes = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError('Title cannot be empty')
        return title

    @validates('category')
    def validate_category(self, key, category):
        if not category or not category.strip():
            raise ValueError('Category cannot be empty')
        return category

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes is None or int(duration_minutes) <= 0:
            raise ValueError('Duration must be a positive number of minutes')
        return duration_minutes

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'duration_minutes': self.duration_minutes,
            'date': self.date.isoformat() if self.date else None,
            'notes': self.notes,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f'<WorkoutLog {self.id}: {self.title}>'
