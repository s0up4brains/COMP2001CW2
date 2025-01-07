# models.py
import pytz
from datetime import datetime
from marshmallow_sqlalchemy import fields

from sqlalchemy import Table, Column, Integer, ForeignKey

from config import db, ma

#     #join table trail->tags
# Trail_Tags = db.Table(
#   'Trail_Tags',
#   db.metadata,
#   db.Column('TrailID', db.Integer, db.ForeignKey('TrailID')),
#   db.Column('TagID', db.Integer, db.ForeignKey('TagID'))
# )

#route
class Route(db.Model):
    __tablename__ = "Route"
    __table_args__ = {'schema': 'CW2'}
    RouteID = db.Column(db.Integer, primary_key=True)
    Route_Type = db.Column(db.String, nullable=False)

class RouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Route
        load_instance = True
        sqla_session = db.session
        include_fk = True
        

class Difficulty(db.Model):
    __tablename__ = "Difficulty"
    __table_args__ = {'schema': 'CW2'}
    DifficultyID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Difficulty = db.Column(db.String, nullable=False)
    length = db.Column(db.Numeric, nullable=False)
    Elevation_Gain = db.Column(db.Numeric, nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    

class DifficultySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        
        model = Difficulty
        load_instance = True
        sqla_session = db.session
        include_fk = True        



# description
class Description(db.Model):
    __tablename__ = "Description"
    __table_args__ = {'schema': 'CW2'}
    DescriptionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String, nullable=False)
    Trail_Name = db.Column(db.String, nullable=False)
    Trail_Location = db.Column(db.String, nullable=False)
    RouteID = db.Column(db.Integer, nullable=False)
    DifficultyID = db.Column(db.Integer, db.ForeignKey('CW2.Difficulty.DifficultyID'), nullable=False)

    # Relationship to Difficulty
    difficulty = db.relationship(
        "Difficulty",
        backref="descriptions"  # Allows access to related descriptions from a Difficulty object
    )


class DescriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Description
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    # Nested schema for Difficulty
    difficulty = fields.Nested("DifficultySchema")


# tags
class Tag(db.Model):
    __tablename__ = "Tags"
    __table_args__ = {'schema': 'CW2'}
    TagID = db.Column(db.Integer, primary_key=True)
    Tag_Name = db.Column(db.String(50))
    Tag_Type = db.Column(db.String(50))

    
class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True
        sqla_session = db.session
        include_fk = True


# user
class User(db.Model):
    __tablename__ = "User"
    __table_args__ = {'schema': 'CW2'}
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(32))
    email = db.Column(db.String(50))
    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_fk = True

# trail_log
class TrailLog(db.Model):
    __tablename__ = "Trail_Log"
    __table_args__ = {'schema': 'CW2'}
    LogID = db.Column(db.Integer, primary_key=True)
    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trail.TrailID'))
    Added_By = db.Column(db.String(50), nullable=False)
    Time_Added = db.Column(db.String(50), nullable=False)

class TrailLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailLog
        load_instance = True
        sqla_session = db.session
        include_fk = True


# trail_tags
class TrailTags(db.Model):
    __tablename__ = "Trail_Tags"
    __table_args__ = {'schema': 'CW2'}
    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trail.TrailID'), primary_key=True)
    TagID = db.Column(db.Integer, db.ForeignKey('CW2.Tags.TagID'), primary_key=True)

class TrailTagsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailTags
        load_instance = True
        sqla_session = db.session
        include_fk = True

# trail
class Trail(db.Model):
    __tablename__ = "Trail"
    __table_args__ = {'schema': 'CW2'}
    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('CW2.User.id'))
    Rating = db.Column(db.Numeric)
    DescriptionID = db.Column(db.Integer, db.ForeignKey('CW2.Description.DescriptionID'))
    
    # Relationship to Description
    description = db.relationship(
        "Description",
        backref="trails",  # Allows access to related trails from a Description object
    )


class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_fk = True
        
    # Nested schema for Description
    description = fields.Nested(DescriptionSchema)


trail_schema = TrailSchema()

description_schema = DescriptionSchema()
descriptions_schema = DescriptionSchema(many=True)

trails_schema = TrailSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)



