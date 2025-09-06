from app import db, User, Post, Follow
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def seed_users(n=50):
    for _ in range(n):
        user = User(
            Name=fake.name(),
            Email=fake.unique.email(),
            Age=random.randint(18, 65),
            Gender=random.choice(['Male', 'Female', 'Other']),
            Location=fake.city()
        )
        db.session.add(user)
    db.session.commit()

def seed_follows():
    users = User.query.all()
    for user in users:
        followees = random.sample(users, k=random.randint(1, 10))
        for f in followees:
            if f.UserID != user.UserID:
                follow = Follow(FollowerID=user.UserID, FollowingID=f.UserID, Timestamp=datetime.utcnow())
                db.session.add(follow)
    db.session.commit()

def seed_posts():
    users = User.query.all()
    for _ in range(200):
        user = random.choice(users)
        post = Post(
            UserID=user.UserID,
            Content=fake.sentence(nb_words=20),
            Timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            SentimentScore=random.uniform(-1, 1)
        )
        db.session.add(post)
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    seed_users()
    seed_follows()
    seed_posts()
    print("Database seeded!")