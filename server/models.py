from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # add relationship
    appearances = db.relationship('Appearance', back_populates ='episode', cascade='all, delete-orphan')
    
    
    
    # add serialization rules
    serialize_rules = ('-appearances.episode')
    

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # add relationship
    appearances = db.relationship('Appearance', back_populates ='guest', cascade='all, delete-orphan')
    
    
    # add serialization rules
    serialize_rules =('-appearances.guest')
    

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    # add relationships
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey ('guests.id'))
    
    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')
    
    # add serialization rules
    serialize_rules = ('-episode.appearances', '-guest.appearances')
    # add validation
    @validates('rating')
    def check_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5 (inclusive).")
        return rating

        
        
    
     
# add any models you may need.
