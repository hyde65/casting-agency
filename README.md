# CASTING-AGENCY

This backend was done to improve casting agencies, providing apis rest to save data of the movies and actors, utilizing python for backend.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

You also can utilize Pyenv to install 3.7.0 easily.
[pyenv installer](https://github.com/pyenv/pyenv-installer)

#### Virtual Enviroment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the main directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

## Database setup
This project utilized postgresql 13.1.
To install you can go to [postgresql download](https://www.postgresql.org/download/)

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql casting-agency < casting-agency.pgsql
```

## Runing the server

From the source code directory first ensure you're working using your created virtual enviroment.


To run the server, execute:
```bash
python manage runserver -r
```

## API REFERENCE
Error Handling
Errors are returned as JSON objects in the following format.

{
    "success": False,
    "error": 400,
    "message": "bad request"
}

The API will return three error types when request fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable entity
- 500: Internal server error

### ENDPOINTS
GET '/actors'
GET '/movies'
POST '/actors'
POST'/movies'
DELETE '/actors/\<int:id>'
DELETE '/movies/<int:id>'
PATCH '/actors/<int:id>/update'
PATCH '/movies/<int:id>/update'

#### GET '/actors'
- Fetches a dictionary with actors and a success value, utilizing a bearer token.
- Request Arguments: Header authorization bearer token.

Example:
GET 'localhost:5000/actors'
headers
```JSON
{
    "authorization":"Bearer <Token>"
}
```

- Returns: a json with the next keys:
    - success: True.
    - actors: a list of actors that have the next keys.
        - id: The identificator
        - name: The name of the actor
        - gender: The gender of the actor
        - movies: The movies where acted the actor.

Example: 

```json
{
    "actors": [
        {
            "gender": "Male",
            "id": 1,
            "movies": [
                1
            ],
            "name": "Daniel Radcliffe"
        },
        {
            "gender": "Female",
            "id": 2,
            "movies": [
                1,2
            ],
            "name": "Emma Watson"
        }
    ],
    "success": true
}
```

#### GET '/movies'
- Fetches a dictionary with movies and a success value, utilizing a bearer token.
- Request Arguments: Header authorization bearer token.

Example:
GET 'localhost:5000/movies'
headers
```JSON
{
    "authorization":"Bearer <Token>"
}
```
- Returns: a json with the next keys:
    - success: True.
    - movies: a list of actors that have the next keys.
        - id: /<int>The identificator
        - title: The title of the movie
        - release_date: The release date of the movie
        - actors: The actors who acted in the movie.

Example: 

```json
{
    "movies": [
        
        {
            "actors": [
                2
            ],
            "id": 2,
            "release_date": "01-01-2017",
            "title": "Beauty and the Beast"
        },
        {
            "actors": [
                1,
                2
            ],
            "id": 1,
            "release_date": "05-31-2004",
            "title": "Harry Potter and the Prisoner of Azkaban"
        }
    ],
    "success": true
}

```
#### POST '/actors'
- Create an actor through json request. 
- Request Arguments: 
    - Header authorization bearer token.
    - JSON Request
        - name: The name of the actor
        - gender: The gender of the actor
        - movies: The id of the movies where acted the actor, This movies must exist, otherwise you will raise an 422 error.
Example:
POST 'localhost:5000/movies'
headers
```JSON
{
    "authorization":"Bearer <Token>"
}
Request json
```JSON
{
    "name": "My name",
    "gender": "Male",
    "movies":[1,2]
}
```
- Returns: a json with the next keys:
    - success: True.
    - created: The id of the movie created.

Example: 

```json
{
    "created": 3,
    "success": true
}
```

#### POST'/movies'
- Create a movie through a json request, and a bearer token.
- Request Arguments: 
    - Header authorization bearer token.
    - Json request with the followin keys
        - title: the title of the movie.
        - release_date: the release_date of the movie.
        - actors: the actors of the movie, this actors have to exist or will raise an 422 error.
Example
POST 'localhost:5000/movies'

headers
```JSON
{
    "authorization":"Bearer <Token>"
}
```

- Returns: a json with the next keys
    - success: True
    - created: The id of the created movie.

Example
```JSON
{
    "created": 3,
    "success": true
}
```

#### DELETE '/actors/\<int:id>'
- Delete an actor utilizing a bearer token and path parameter
- Request Arguments:
    - Header authorization bearer token.
    - Path parameter utilizing the id.

Example:
DELETE '/actors/3'

header
```JSON
{
    "authorization":"Bearer <Token>"
}
```
- Returns: a json with the next keys:
    - success: True.
    - deleted: The id of the actor deleted.

```JSON
{
    "id": 3,
    "deleted": true
}

```

#### DELETE '/movies/<int:id>'
- Delete a movie through a bearer token and path parameter
- Request Arguments:
    - Header authorization bearer token.
    - Path parameter utilizing the id.

Example:
DELETE 'localhost:5000/movies/3'

header
```JSON
{
    "authorization":"Bearer <Token>"
}
```
- Returns: a json with the next keys:
    - success: True.
    - deleted: The id of the actor deleted.

```JSON
{
    "deleted": 3,
    "success": true
}
```

#### PATCH '/actors/<int:id>/update'
- Update an actor with a json request data, authorization bearer token and path parameter.
- Request Arguments:
    - Header authorization bearer token.
    - Path parameter utilizing the id of the actor to be updated.
    - A json request with the following keys
        - name: The name of the actor
        - gender: The gender of the actor
        - movies: The movies where acted the actor, This movies must exist or will raise an 422 error.
Example
PATCH 'localhost:5000/actors/1/update'

Header
```JSON
{
    "authorization":"Bearer <Token>"
}
```

Request Json
```JSON
{
    "name":"Daniel Jacob Radcliffe"
}
```
- Returns: a json with the next keys:
    - success: True.
    - actor: The actor updated with the next keys.
        - id: The identificator
        - name: The name of the actor
        - gender: The gender of the actor
        - movies: The movies where acted the actor.
Example 
```JSON
{
    "actor": {
        "movies": [2],
        "gender": "Male",
        "name": "Daniel Jacob Radcliffe"
    },
    "success": true
}
```

#### PATCH '/movies/<int:id>/update'
- Update a movie with the data to be changed through a json request data, authorization bearer token and path parameter.
- Request Arguments:
    - Header authorization bearer token.
    - Path parameter utilizing the id of the movie to be updated..
    - A json request with the following keys
        - title: the title of the movie.
        - release_date: the release_date of the movie.
        - actors: the actors of the movie, this actors have to exist or will raise an 422 error.
Example
PATCH 'localhost:5000/movies/1/update'

Header
```JSON
{
    "authorization":"Bearer <Token>"
}
```
JSON Request
```JSON
{
    "title": "Harry Potter 3",
    "actors": [
                1
            ],
    "release_date": "01-01-2004"
}
```
- Return a json with the following keys
    - success: True
    - movie with the following keys
        - id: The id of the movie
        - title: The title of the movie
        - release_date: The release date of the movie
        - actors: The actors who acted in the movie.
Example
```JSON
{
    "movie": {
        "actors": [
            1
        ],
        "id": 1,
        "release_date": "01-01-2004",
        "title": "Harry Potter 3"
    },
    "success": true
}
```