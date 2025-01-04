# trails.py

from flask import abort, make_response

from config import db
from models import Trail, User, trail_schema


def read_one(trail_id):
    trail = Trail.query.get(trail_id)

    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(
            404, f"Trail with ID {trail_id} not found"
        )

def update(trail_id, trail):
    existing_trail = Trail.query.get(trail_id)

    if existing_trail:
        update_trail = trail_schema.load(trail, session=db.session)
        existing_trail.content = update_trail.content
        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 201
    else:
        abort(404, f"Trail with ID {trail_id} not found")

def delete(trail_id):
    existing_trail = Trail.query.get(trail_id)

    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"{trail_id} successfully deleted", 204)
    else:
        abort(404, f"Trail with ID {trail_id} not found")

def create(trail):
    user_id = trail.get("user_id")
    user = User.query.get(user_id)

    if user:
        new_trail = trail_schema.load(trail, session=db.session)
        user.trails.append(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(
            404,
            f"User not found for ID: {user_id}"
        )