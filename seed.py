#!/usr/bin/env python3

from datetime import date, timedelta
from random import randint, choice

from faker import Faker

from config import app, db
from models import User, WorkoutLog

fake = Faker()

CATEGORIES = ['Cardio', 'Strength', 'Yoga', 'HIIT', 'Cycling', 'Swimming']

with app.app_context():
    print('Clearing db...')
    WorkoutLog.query.delete()
    User.query.delete()

    print('Seeding users...')
    users = []
    for _ in range(5):
        user = User(username=fake.unique.user_name())
        user.password_hash = 'password123'
        users.append(user)
        db.session.add(user)
    db.session.commit()

    print('Seeding workout logs...')
    for user in users:
        for _ in range(randint(3, 6)):
            log = WorkoutLog(
                title=fake.sentence(nb_words=3).rstrip('.'),
                category=choice(CATEGORIES),
                duration_minutes=randint(15, 90),
                date=date.today() - timedelta(days=randint(0, 30)),
                notes=fake.sentence(),
                user_id=user.id,
            )
            db.session.add(log)
    db.session.commit()

    print('Done seeding! Example login -> username: any seeded username, password: password123')
