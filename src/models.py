import os
import sys
from sqlalchemy import DateTime, ForeignKey, Integer, String, Float, Column
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Fans(db.Model):
    __tablename__ = 'fans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    date_of_subscription = db.Column(db.Date, unique=False, nullable=False)
    def __repr__(self):
        return '<Fans %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_subscription": self.date_of_subscription

        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    rotation_period = db.Column(Float, unique=False, nullable=False)
    orbital_period = db.Column(Float, unique=False, nullable=False)
    diameter = db.Column(Integer, unique=False, nullable=False)
    climate = db.Column(db.String(120), unique=False, nullable=False)
    gravity = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {    
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity
        }
    
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(Integer, unique=False, nullable=False)
    mass = db.Column(Float, unique=False, nullable=False)
    hair_color = db.Column(db.String(120), unique=False, nullable=False)
    skin_color = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color
        }
    

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    fan_id = db.Column(db.Integer, db.ForeignKey('fans.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def to_dict(self):
        return {
            "id": self.id,
            "fan_id": self.fan_id,
            "people_id": self.people_id,
            "planets_id": self.planets_id
        }
    
