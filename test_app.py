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
        
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'manuel')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')
        self.DB_NAME = os.getenv('DB_NAME', 'test-casting-agency')

        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.DB_USER, self.DB_PASSWORD,
            self.DB_HOST, self.DB_NAME
        )
        setup_db(self.app,self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()
        
        self.headers = {
            'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikk1d3FNeFk0TkdWaW1PVEtMS1Z3UyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDcxODQ3NDgwMzM4NDI4MDgyMiIsImF1ZCI6WyJhcGkiLCJodHRwczovL2Nhc3RpbmctYWdlbmN5LWJvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTA0NjgyMzAsImV4cCI6MTYxMDU1NDYzMCwiYXpwIjoiZEhjeDVZT0ZkcnFhalllYjhIdXpjMTVvMzVVdFA3NXgiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.udz6DpzgYwVX6BQTbxqyE7vrctL3W05LnMGLFEhSGY1UwqyigqGtN94UXMqh2VQ_2WnzuY-16ricybowC2vV99yspILoY_glPZffzC9EvHCv7fGESj2JaRuds4NzfhCdR9fVO-bJQAn_ZdmfQQmLk4ybSZcWNWmRin8IS4SAoSMusqTdV6Nt1QDC2_99GkRoEt3g-0PUcJYM7tmUccUrYJ0vWtPCs2f5HBglCyrfA5VXaUdzxEasRejobPo87LAWGoTVepEwnl4HtTBbUJQ5UQEybbIJsj6oS9uwqoAccIYFox3G7498gSFpT4DBuWfLfXyi-jOL9gZfnTnTBNuwSg"
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
            'title':'Harry Potter and the Prisoner of Azkaban',
            "release_date": "05-31-2004"
        }
        self.update_actor = {
            'name': 'Edward Thomas Hardy'
        }
    
    def tearDown(self):
        pass
    
    
    # TODO: Add tests for success behavior for apis.
    def test_get_movies(self):
        res = self.client.get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        res = self.client.get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_post_movie(self):
        res = self.client.post('/movies', headers=self.headers, json = self.new_movie)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
    
    def test_post_actor(self):
        res = self.client.post('/actors', headers=self.headers, json = self.new_actor)
        data =json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
    
    def test_delete_movie(self):
        id = 3 # Deleting movie "Your Name"
        res = self.client.delete('/movies/'+str(id), headers=self.headers)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'],id)
        self.assertIsNone(movie)
    

    def test_delete_actor(self):
        id = 6 # Deleting actor "Anthony Michael Hall"
        res = self.client.delete('/actors/'+str(id), headers=self.headers)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'],id)
        self.assertIsNone(movie)
    
    def test_patch_actor(self):
        # Changing name of Tom Hardy by Edward Thomas Hardy
        id = 3
        res = self.client.patch('/actors/'+str(id)+"/update",json = self.update_actor, headers= self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'].get('name'), self.update_actor.get('name')) # Checking if the name is changed
        
    def test_patch_movie(self):
        # Changing title of Harry poter 3 by Harry Potter and the Prisoner of Azkaban
        # and release date by 31-04-2004
        id = 1 
        res = self.client.patch('/movies/'+str(id)+"/update", json = self.update_movie, headers= self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'].get('title'), self.update_movie.get('title')) # Checking if the title is changed
        self.assertEqual(data['movie'].get('release_date'), self.update_movie.get('release_date')) # Checking if the release_date is changed




    # TODO: Add tests for error behavior for apis.

    


    # TODO: Add tests for RBAC for each role.


if __name__ == "__main__":
    unittest.main()

        
