import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.route('/')
  def index():
    return 'Hello world'

  @app.route('/actors')
  def get_actors():
    actors = Actor.query.all()

    actors_list = [actor.format() for actor in actors]
    return jsonify({
      'success':True,
      'actors': actors_list
    })
  @app.route('/movies')
  def get_movies():
    movies = Movie.query.all()

    movies_list = [movie.format() for movie in movies] 
    return jsonify({
      'success':True,
      'movies':movies_list
    })
  return app

app = create_app()

if __name__ == '__main__':
  app.run()
