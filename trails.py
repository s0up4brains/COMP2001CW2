# trails.py

from flask import abort, make_response
from sqlalchemy.exc import IntegrityError
from config import db
from models import Trail, Trail, Tag, TrailTags, descriptions_schema, description_schema, DescriptionSchema, Description, users_schema, user_schema, trails_schema, trail_schema, TrailTagsSchema



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

        # Only update fields that the user can modify, leave out DescriptionID and DifficultyID
        existing_trail.Rating = update_trail.Rating
        existing_trail.user_id = update_trail.user_id
        
        # Update nested description or difficulty if provided
        if 'description' in trail:
            existing_trail.description.Description = update_trail.description.Description
            existing_trail.description.RouteID = update_trail.description.RouteID
            existing_trail.description.Trail_Location = update_trail.description.Trail_Location
            existing_trail.description.Trail_Name = update_trail.description.Trail_Name
        
        if 'difficulty' in trail:
            existing_trail.difficulty.Difficulty = update_trail.difficulty.Difficulty
            existing_trail.difficulty.Duration = update_trail.difficulty.Duration
            existing_trail.difficulty.Elevation_Gain = update_trail.difficulty.Elevation_Gain
            existing_trail.difficulty.length = update_trail.difficulty.length

        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 201
    else:
        abort(404, f"Trail with TrailID {TrailID} not found")



def delete(TrailID):
    existing_trail = Trail.query.filter(Trail.TrailID == TrailID).one_or_none()

    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"{TrailID} successfully deleted", 200)
    else:
        abort(404, f"Trail with TrailID {TrailID} not found")

