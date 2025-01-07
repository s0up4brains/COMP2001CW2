# trails.py

from flask import abort, make_response
from sqlalchemy.exc import IntegrityError
from config import db
from models import Trail, Trail, Tag, TrailTags, users_schema, user_schema, trails_schema, trail_schema, TrailTagsSchema



def create(trail):
    TrailID = trail.get("TrailID")
    existing_trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    if existing_trail is None:
        new_trail = trail_schema.load(trail, session=db.session)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(406, f"Trail with TrailName {TrailID} already exists")


def read_all():
    trails = Trail.query.all()
    return trails_schema.dump(trails)

def read_one(TrailID):
    trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail with last name {TrailID} not found")


def update(TrailID, trail):
    existing_trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    if existing_trail:
        update_trail = trail_schema.load(trail, session=db.session)
        existing_trail.DescriptionID = update_trail.DescriptionID
        existing_trail.Rating = update_trail.Rating
        existing_trail.user_id = update_trail.user_id
        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 201
    else:
        abort(404, f"Trail with TraildID {TrailID} not found")


def delete(TrailID):
    existing_trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"{TrailID} successfully deleted", 200)
    else:
        abort(404, f"Trail with last name {TrailID} not found")

