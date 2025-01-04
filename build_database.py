# build_database.py

from datetime import datetime
from config import app, db
from models import User, Trail


USERS_TRAILS = [
    {
        "lname": "Hopper",
        "fname": "Grace",
        "trails": [
            ("Great spot to see deer early morning!", "2024-11-26 09:10:24"),
            ("Rocky path near the quarry needs good shoes.", "2024-11-26 11:17:54"),
        ],
    },
    {
        "lname": "Berners-Lee",
        "fname": "Tim",
        "trails": [
            ("Lovely tea room at the old station building.", "2024-11-26 12:15:03"),
            ("Watch out for cyclists on narrow sections.", "2024-11-26 15:09:21"),
        ],
    },
    {
        "lname": "Lovelace",
        "fname": "Ada",
        "trails": [
            ("Old copper mining ruins are fascinating.", "2024-11-26 10:47:54"),
            ("Fast flowing river after the rain yesterday!", "2024-11-26 11:03:17"),
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in USERS_TRAILS:
        new_user = User(lname=data.get("lname"), fname=data.get("fname"))
        for content, timestamp in data.get("trails", []):
            new_user.trails.append(
                Trail(
                    content=content,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                )
            )
        db.session.add(new_user)
    db.session.commit()