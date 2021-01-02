import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import datetime

DATABASE_URL = os.getenv('DATABASE_URL','postgresql://manuel:123456@localhost:5432/casting-agency')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app,DATABASE_URL=DATABASE_URL):
    app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app=app
    db.init_app(app)
    
    #db.create_all()

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_soukey=True)
    title = Column(String)
    release_date = Column(db.DateTime())

    

class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)



