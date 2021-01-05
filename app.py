import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import exc
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
  
  @app.route('/actors', methods=['POST'])
  def create_actor():
    name = request.json.get('name')
    gender = request.json.get('gender')
    movie_id = request.json.get('movie_id')

    actor = Actor(name=name,gender=gender)

    if movie_id is not None:
      movie = Movie.query.filter_by(id=movie_id).one_or_none()
      movie_list = []
      movie_list.append(movie)
      actor.movies = movie_list
      
    actor.insert()

    return jsonify({
      'success':True,
      'actor':actor.format()
    })
  
  @app.route('/movies', methods=['POST'])
  def create_movie():
    title = request.json.get('title')
    release_date = request.json.get('release_date')
    actor_id = request.json.get('actor_id')
    
    movie = Movie(title=title,release_date=release_date)

    # Adding actors to movie if there is an actor_id
    if actor_id is not None:
      actor = Actor.query.filter_by(id=actor_id).one_or_none()
      actor_list = []
      actor_list.append(actor)
      movie.actors = actor_list
    
    movie.insert()

    return jsonify({
      'success': True,
      'actor': movie.format()
    })
  @app.route('/movies/<int:id>', methods=['DELETE'])
  def delete_movie(id):
    movie = Movie.query.filter_by(id=id).one_or_none()
    if movie is None:
      abort(404)

    movie.delete()
    return jsonify({
      'success':True,
      'id':id
    })
  @app.route('/actors/<int:id>',methods=['DELETE'])
  def delete_actor(id):
    actor = Actor.query.filter_by(id=id).one_or_none()
    if actor is None:
      abort(404)
    
    actor.delete()
    return jsonify({
      'success':True,
      'id':id
    })
  
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad request'
      }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found'
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed'
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'internal server error'
      }), 500
  return app

app = create_app()

if __name__ == '__main__':
  app.run()
