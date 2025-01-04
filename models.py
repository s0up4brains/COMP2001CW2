# models.py

import pytz
from datetime import datetime
from marshmallow_sqlalchemy import fields

from config import db, ma


class Trail(db.Model):
    __tablename__ = "trail"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_fk = True

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )
    trails = db.relationship(
        Trail,
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Trail.timestamp)"
    )

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sql_session = db.session
        include_relationships = True

    trails = fields.Nested(TrailSchema, many=True)

trail_schema = TrailSchema()

user_schema = UserSchema()
users_schema = UserSchema(many=True)