# trails.py

from flask import abort, make_response
from sqlalchemy.exc import IntegrityError
from config import db
from models import Trail, User, Tag, TrailTags, trail_schema, user_schema, users_schema, TrailTagsSchema


def read_one(trail_id):
    """
    Retrieves a single trail by its ID along with its associated tags.
    """
    trail = Trail.query.get(trail_id)

    if trail:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail with ID {trail_id} not found")


def create(trail_data):
    """
    Creates a new trail and associates it with tags if provided.
    """
    user_id = trail_data.get("user_id")
    tag_ids = trail_data.get("tag_ids", [])

    user = User.query.get(user_id)

    if not user:
        abort(404, f"User not found for ID: {user_id}")

    new_trail = trail_schema.load(trail_data, session=db.session)

    try:
        # Link the new trail with tags if provided
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                trail_tag = TrailTags(TrailID=new_trail.TrailID, TagID=tag.TagID)
                db.session.add(trail_tag)

        user.trails.append(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201

    except IntegrityError:
        db.session.rollback()
        abort(400, "Failed to create trail due to data integrity issues.")


def update(trail_id, trail_data):
    """
    Updates an existing trail and its associated tags.
    """
    existing_trail = Trail.query.get(trail_id)
    if not existing_trail:
        abort(404, f"Trail with ID {trail_id} not found")

    # Update basic trail information
    updated_trail = trail_schema.load(trail_data, session=db.session, instance=existing_trail, partial=True)

    # Update tags
    if "tag_ids" in trail_data:
        tag_ids = trail_data.get("tag_ids", [])

        # Clear existing tags
        TrailTags.query.filter_by(TrailID=trail_id).delete()

        # Add new tags
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                trail_tag = TrailTags(TrailID=trail_id, TagID=tag.TagID)
                db.session.add(trail_tag)

    db.session.commit()
    return trail_schema.dump(updated_trail), 201


def delete(trail_id):
    """
    Deletes a trail and removes its associations with tags.
    """
    existing_trail = Trail.query.get(trail_id)

    if not existing_trail:
        abort(404, f"Trail with ID {trail_id} not found")

    # Delete associated trail-tags
    TrailTags.query.filter_by(TrailID=trail_id).delete()

    db.session.delete(existing_trail)
    db.session.commit()
    return make_response(f"Trail ID {trail_id} successfully deleted", 204)
