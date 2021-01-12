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
            'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikk1d3FNeFk0TkdWaW1PVEtMS1Z3UyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWJvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDcxODQ3NDgwMzM4NDI4MDgyMiIsImF1ZCI6WyJhcGkiLCJodHRwczovL2Nhc3RpbmctYWdlbmN5LWJvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTA0NjczMzEsImV4cCI6MTYxMDQ3NDUzMSwiYXpwIjoiZEhjeDVZT0ZkcnFhalllYjhIdXpjMTVvMzVVdFA3NXgiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.cuntYR_QZkoopMrt3gTV5Scvcc54OQzQxCkktP7kF7-qazM_3-y9zKjQT6UBdPCwX-7TiMFFfnJOXqra575tvLKbsJcWKwGO9N3ksokdbYoYec0V4j0HTXkyvO2OqAmnYX3TK48YVNWq3eM2buThSao8TZPeLdUGLM1e9x_XTBjwO3kLqO-TTvuHAbD4lM5aaYxVH1p1PC6gjPJAe3N1wrgaiYIkl6qMGN1u9QiBrmPB4F5_uKz9p7U99T3wE2tlQsay5UCxqNeP3_dN3Nrr116PuyEPmqfm5eHciVkSDdo-vjeOGYA3-I_r8_Z8YmciYhnFTuwKt431Y9t5wTTM1A"
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

        
