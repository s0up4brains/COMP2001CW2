# users.py

from flask import abort, make_response

from config import db
from models import User, users_schema, user_schema


def read_all():
    users = User.query.all()
    return users_schema.dump(users)


def create(user):
    lname = user.get("lname")
    existing_user = User.query.filter(User.lname == lname).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"User with last name {lname} already exists")


def read_one(lname):
    user = User.query.filter(User.lname == lname).one_or_none()

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(404, f"User with last name {lname} not found")


def update(lname, user):
    existing_user = User.query.filter(User.lname == lname).one_or_none()

    if existing_user:
        update_user = user_schema.load(user, session=db.session)
        existing_user.fname = update_user.fname
        existing_user.lname = update_user.lname
        existing_user.email = update_user.email
        existing_user.password = update_user.password
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 201
    else:
        abort(404, f"User with last name {lname} not found")


def delete(lname):
    existing_user = User.query.filter(User.lname == lname).one_or_none()

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"User with last name {lname} not found")