import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from datetime import datetime


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # You can change the variables to your desired database
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'manuel')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')
        self.DB_NAME = os.getenv('DB_NAME', 'test-casting-agency')

        TOKEN_CASTING_ASSISTANT = os.getenv('TOKEN_CASTING_ASSISTANT')
        TOKEN_CASTING_DIRECTOR = os.getenv('TOKEN_CASTING_DIRECTOR')
        TOKEN_EXECUTIVE_DIRECTOR = os.getenv('TOKEN_EXECUTIVE_DIRECTOR')

        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.DB_USER, self.DB_PASSWORD,
            self.DB_HOST, self.DB_NAME
        )
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()

        self.header_casting_assistant = {
            'authorization': "Bearer {}".format(TOKEN_CASTING_ASSISTANT)
        }
        self.header_casting_director = {
            'authorization': "Bearer {}".format(TOKEN_CASTING_DIRECTOR)
        }
        self.header_executive_director = {
            'authorization': "Bearer {}".format(TOKEN_EXECUTIVE_DIRECTOR)
        }

        self.new_actor = {
            'name': 'Rupert Grint',
            'gender': 'Male',
            'movies': [1]
        }

        self.new_movie = {
            'title': 'Joker',
            'release_date': '01-01-2019',
            'actors': []
        }
        self.update_movie = {
            'title': 'Harry Potter and the Prisoner of Azkaban',
            "release_date": "05-31-2004"
        }
        self.update_actor = {
            'name': 'Edward Thomas Hardy'
        }

    def tearDown(self):
        pass

    # Tests for success behavior for apis.
    # RBAC tests: Executive director

    def test_get_movies(self):
        res = self.client.get(
            '/movies', headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        res = self.client.get(
            '/actors', headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_post_movie(self):
        res = self.client.post(
            '/movies', headers=self.header_executive_director,
            json=self.new_movie)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_post_actor(self):
        res = self.client.post(
            '/actors', headers=self.header_executive_director,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_delete_movie(self):
        id = 3  # Deleting movie "Your Name"
        res = self.client.delete(
            '/movies/'+str(id), headers=self.header_executive_director)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertIsNone(movie)

    def test_delete_actor(self):
        id = 6  # Deleting actor "Anthony Michael Hall"
        res = self.client.delete(
            '/actors/'+str(id), headers=self.header_executive_director)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertIsNone(movie)

    def test_patch_actor(self):
        # Changing name of Tom Hardy by Edward Thomas Hardy
        id = 3
        res = self.client.patch('/actors/'+str(id)+"/update",
                                json=self.update_actor,
                                headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'].get('name'), self.update_actor.get(
            'name'))  # Checking if the name is changed

    def test_patch_movie(self):
        # Changing title of Harry poter 3 by Harry Potter and the Prisoner
        # of Azkaban and release date by 31-04-2004
        id = 1
        res = self.client.patch('/movies/'+str(id)+"/update",
                                json=self.update_movie,
                                headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'].get('title'), self.update_movie.get(
            'title'))  # Checking if the title is changed
        # Checking if the release_date is changed
        self.assertEqual(data['movie'].get('release_date'),
                         self.update_movie.get('release_date'))

    # Tests for error behavior for apis.
    def test_400_error_post_actor(self):
        json_void = {}
        res = self.client.post('/actors', json=json_void,
                               headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_400_error_post_movie(self):
        json_void = {}
        res = self.client.post('movies', json=json_void,
                               headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_422_error_post_actor(self):
        json_send = {
            "name": "Emma Charlotte Duerre Watson",
            "gender": "Female",
            "movies": [22, 23]  # Doesn't exist this movies
        }
        res = self.client.post('/actors', json=json_send,
                               headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_422_error_post_movie(self):
        json_send = {
            "title": "Harry Potter 3",
            'release_date': "01-28-2004",
            'actors': [20, 23]  # Doesn't exist this actors
        }
        res = self.client.post('/movies', json=json_send,
                               headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_404_error_delete_movie(self):
        id = 1000
        res = self.client.delete(
            '/movies/'+str(id), headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_404_error_delete_actor(self):
        id = 1000
        res = self.client.delete(
            '/actors/'+str(id), headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_404_error_patch_movie(self):
        id = 1000
        res = self.client.patch(
            '/movies/'+str(id)+"/update",
            headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_404_error_patch_actor(self):
        id = 1000
        res = self.client.patch(
            '/movies/'+str(id)+"/update",
            headers=self.header_executive_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_400_error_patch_movie(self):
        id = 1
        json_send = {}
        res = self.client.patch('/movies/'+str(id)+"/update",
                                headers=self.header_executive_director,
                                json=json_send)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_400_error_patch_actor(self):
        id = 1
        json_send = {}
        res = self.client.patch('/actors/'+str(id)+"/update",
                                headers=self.header_executive_director,
                                json=json_send)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_422_error_patch_actor(self):
        id = 1
        json_send = {
            'name': "Daniel Rad",
            'movies': [30, 31]
        }
        res = self.client.patch('/actors/'+str(id)+"/update",
                                headers=self.header_executive_director,
                                json=json_send)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_422_error_patch_movie(self):
        id = 1
        json_send = {
            'title': "Harry Potter 3",
            'actors': [30, 31]
        }
        res = self.client.patch('/movies/'+str(id)+"/update",
                                headers=self.header_executive_director,
                                json=json_send)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    # RBAC tests: Casting Assistant
    def test_casting_assistant_get_actors(self):
        res = self.client.get('/actors', headers=self.header_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_casting_assistant_get_movies(self):
        res = self.client.get('/movies', headers=self.header_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_casting_assistant_post_actor(self):
        res = self.client.post(
            '/actors', headers=self.header_casting_assistant,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_casting_assistant_delete_actor(self):
        id = 7
        res = self.client.delete(
            '/movies/'+str(id), headers=self.header_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    # RBAC tests: Casting Director
    def test_casting_director_post_actor(self):
        res = self.client.post(
            '/actors', headers=self.header_casting_director,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_casting_director_patch_movie(self):
        id = 2
        update = {
            'title': 'Mad Max',
            'release_date': '05-14-2015'
        }
        res = self.client.patch(
            '/movies/'+str(id)+"/update", json=update,
            headers=self.header_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'].get('title'), update.get(
            'title'))  # Checking if the title is changed
        self.assertEqual(data['movie'].get('release_date'), update.get(
            'release_date'))  # Checking if the release_date is changed

    def test_casting_director_post_movie(self):
        movie = {
            'title': 'The pianist',
            'release_date': '09-06-2002',
            'actors': []
        }
        res = self.client.post(
            '/movies', headers=self.header_casting_director, json=movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_casting_director_delete_movie(self):
        id = 5  # Deleting movie "Beauty and the Beast"
        res = self.client.delete(
            '/movies/'+str(id), headers=self.header_casting_director)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=id).one_or_none()
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')
        self.assertIsNotNone(movie)


if __name__ == "__main__":
    unittest.main()
