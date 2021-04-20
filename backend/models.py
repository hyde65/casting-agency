import os
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import datetime

# Database url variable to connect to heroku database.
# Default variable value: localhost database
DATABASE_URL = os.getenv(
    'DATABASE_URL')

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, DATABASE_URL=DATABASE_URL):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Assosiation table between Movie and Actor.
# One actor can act in many movies.
# One Movie can have many actors.
association_table = Table(
    'Movie_Actor', db.Model.metadata,
    Column('Movie_id', Integer, ForeignKey('Movie.id')),
    Column('Actor_id', Integer, ForeignKey('Actor.id'))
)


class Movie(db.Model):
    __tablename__ = 'Movie'

    def __init__(self, title=None, release_date=None):
        self.title = title
        self.release_date = release_date

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(db.DateTime())

    actors = relationship(
        'Actor',
        secondary=association_table,
        back_populates='movies'
    )

    # Helper methods
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        actors_id = [actor.id for actor in self.actors]
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%m-%d-%Y"),
            'actors': actors_id
        }


class Actor(db.Model):
    __tablename__ = 'Actor'

    def __init__(self, name=None, gender=None):
        self.name = name
        self.gender = gender

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)

    movies = relationship(
        'Movie',
        secondary=association_table,
        back_populates='actors'
    )

    # Helper Methods
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        movies_id = [movie.id for movie in self.movies]
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'movies': movies_id
        }
