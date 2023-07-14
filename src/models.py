from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
            
class User(db.Model):
    __tablename__ = 'user'
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250),unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.db.String(120), unique=True, nullable=False)
    

class Characters(db.Model):
    __tablename__ = 'characters'
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birth_date = db.Column(db.String(250))
    height = db.Column(db.Integer, primary_key=False)
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    gender = db.Column(db.String(250))

class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.Integer, primary_key=False)
    diameter = db.Column(db.Integer, primary_key=False)
    climate = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    terrain = db.Column(db.String(250))


class Ships(db.Model):
    __tablename__ = 'ships'
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    model = db.Column(db.String(250))
    max_speed = db.Column(db.Integer, primary_key=False)
    passengers = db.Column(db.Integer, primary_key=False)
    starship_class = db.Column(db.String(250))

class CharacterFavorites(db.Model):
    __tablename__ = 'favorites_char'
   
    id = db.Column(db.Integer, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
   
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

class PlanetsFavorites(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

class ShipsFavorites(db.Model):
    __tablename__ = 'favorites_ships'
    id = db.Column(db.Integer, primary_key=True)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    
#     def to_dict(self):
#         return {}

# ## Draw from SQLAlchemy db.Model
# render_er(db.Model, 'diagram.png')

def __repr__(self):
        return '<User %r>' % self.username

def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

        


import os