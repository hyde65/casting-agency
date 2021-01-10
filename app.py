import os
from flask import Flask, request, abort, jsonify, abort, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import exc
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.route('/')
  def index():
    
    return render_template('index.html')
  
  @app.route('/login')
  def login():
    return redirect('https://casting-agency-bo.us.auth0.com/authorize?audience=api&response_type=token&client_id=dHcx5YOFdrqajYeb8Huzc15o35UtP75x&redirect_uri=http://127.0.0.1:5000/')

  @requires_auth('get:actors')
  @app.route('/actors')
  def get_actors():
    actors = Actor.query.all()

    actors_list = [actor.format() for actor in actors]
    return jsonify({
      'success':True,
      'actors': actors_list
    })
  @requires_auth('get:movies')
  @app.route('/movies')
  def get_movies():
    movies = Movie.query.all()

    movies_list = [movie.format() for movie in movies] 
    return jsonify({
      'success':True,
      'movies':movies_list
    })
  @requires_auth('post:actor')
  @app.route('/actors', methods=['POST'])
  def create_actor():
    name = request.json.get('name')
    gender = request.json.get('gender')
    movies = request.json.get('movies') # id list

    actor = Actor(name=name,gender=gender)
    movie_list = []
    # If there aren't movie_id list just add empty list [] to actor.movie
    if movies is not None:
      for id in movies:
        movie = Movie.query.filter_by(id=id).one_or_none()
        if movie is None:
          abort(422)
        movie_list.append(movie)
    
    actor.movies = movie_list  
    actor.insert()

    return jsonify({
      'success':True,
      'actor':actor.format()
    })
  @requires_auth('post:movie')
  @app.route('/movies', methods=['POST'])
  def create_movie():
    title = request.json.get('title')
    release_date = request.json.get('release_date')
    actors = request.json.get('actors')
    
    movie = Movie(title=title,release_date=release_date)
    actor_list = []
    # Adding actors to movie if there is sent actors
    if actors is not None:
      for id in actors:
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor is None:
          abort(422)
        actor_list.append(actor)
    
    movie.actors = actor_list
    movie.insert()

    return jsonify({
      'success': True,
      'actor': movie.format()
    })
  @requires_auth('delete:movie')
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
  @requires_auth('delete:actor')
  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actor(id):
    actor = Actor.query.filter_by(id=id).one_or_none()
    if actor is None:
      abort(404)
    
    actor.delete()
    return jsonify({
      'success':True,
      'id':id
    })

  def get_actors_by_ids(actors_id_list):
    actor_list = []
    for id in actors_id_list:
      actor = Actor.query.filter_by(id = id).one_or_none()
      if actor is None:
        abort(422)
      actor_list.append(actor)
    return actor_list
  
  @requires_auth('patch:movie')
  @app.route('/movies/<int:id>/update', methods=['PATCH'])
  def update_movie(id):
    movie = Movie.query.filter_by(id=id).one_or_none()
    if movie is None:
      abort(404)
    
    json = request.json
    title = json.get('title')
    release_date = json.get('release_date')
    actors = json.get('actors')

    if title is not None:
      movie.title = title
    
    if release_date is not None:
      movie.release_date = release_date
    
    if actors is not None:
      movie.actors = get_actors_by_ids(actors) #List
    
    movie.update()
    return jsonify({
      'success': True,
      'movie': movie.format()
    })
  def get_movies_by_ids(movies_id_list):
    movie_list = []
    for id in movies_id_list:
      movie = Movie.query.filter_by(id = id).one_or_none()
      if movie is None:
        abort(422)
      
      movie_list.append(movie)
    return movie_list

  @requires_auth('patch:actor')
  @app.route('/actors/<int:id>/update', methods=['PATCH'])
  def update_actor(id):
    actor = Actor.query.filter_by(id = id).one_or_none()
    if actor is None:
      abort(404)
    
    json = request.json
    name = json.get('name')
    gender = json.get('gender')
    movies = json.get('movies')

    if name is not None:
      actor.name = name

    if gender is not None:
      actor.gender = gender
    
    if movies is not None:
      actor.movies = get_movies_by_ids(movies)
    
    actor.update()
    return jsonify({
      'success':True,
      'actor': actor.format()
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
