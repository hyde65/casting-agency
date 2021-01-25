# CASTING-AGENCY

This backend was done to improve casting agencies, providing rest apis to store data of movies and actors, utilizing python and flask for backend and auth0 for authentication.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

You also can utilize Pyenv to install python 3.7.0 easily.
[pyenv installer](https://github.com/pyenv/pyenv-installer)

#### Virtual Enviroment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. 
Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the main directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used for postgresql.

## Database setup
This project utilized postgresql 13.1.
To install you can go to [postgresql download](https://www.postgresql.org/download/)

With Postgres running, restore a database using the casting-agency.pgsql file provided. 
From the backend folder in terminal run:
```bash
createdb casting-agency
psql casting-agency < casting-agency.pgsql
```

## Roles of the project.
For this project we have three roles and every one have diferent permissions.
- Casting Assistant
    - get:actors
    - get:movies
- Casting Director
    - get:actors
    - get:movies
    - post:actor
    - delete:actor
    - patch:actor
    - patch:movie
- Executive Producer
    - get:actors
    - get:movies
    - post:actor
    - post:movie
    - delete:actor
    - delete:movie
    - patch:actor
    - patch:movie

## Runing the server

From the source code directory first ensure you're working using your created virtual enviroment.


To run the server, execute:
```bash
# To setup the config variables, also you can modify the DATABASE_URL
source setup.sh
python manage.py runserver -r
```
## Hosted in Heroku
You also can do test in Heroku with the next url
url: https://casting-agency-bo.herokuapp.com/


## Testing
To test the code you will need:
- JWT token of the next roles:
    - Casting Assistant
    - Casting Director
    - Executive Producer
- A database created for testing purposes.

You will need to export the variables in the terminal

```BASH
export TOKEN_CASTING_ASSISTANT=<Token Executive Assistant>
export TOKEN_CASTING_DIRECTOR=<Token Casting director>
export TOKEN_EXECUTIVE_DIRECTOR=<Token Executive Director>
```

Then you can run
```BASH
bash executetest.sh
```

or you also do same with
```BASH
dropdb test-casting-agency # If you don't have a db you'll recieve an error.
createdb test-casting-agency
psql test-casting-agency < casting-agency.pgsql
python test_app.py # You can modify the variables of the database here.
```
## API Documentation

### Error Handling
Errors are returned as JSON objects in the following format.
```JSON
{
    "success": false,
    "error": 400,
    "message": "bad request"
}
```
The API will return the next error types when request fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable entity
- 500: Internal server error

### ENDPOINTS
- GET '/actors'
- GET '/movies'
- POST '/actors'
- POST'/movies'
- DELETE '/actors/\<int:id>'
- DELETE '/movies/\<int:id>'
- PATCH '/actors/\<int:id>/update'
- PATCH '/movies/\<int:id>/update'

#### GET '/actors'
- Fetches a dictionary with actors and a success value, utilizing a bearer token for authentication.
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
        - id: (int) The identificator
        - name: (string) The name of the actor
        - gender: (string)The gender of the actor
        - movies: (array) The movies where acted the actor.

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
- Fetches a dictionary with movies and a success value, utilizing a bearer token for authentication.
- Request Arguments: Header authorization bearer token.

Example:

GET 'localhost:5000/movies'
headers
```JSON
{
    "authorization": "Bearer <Token>"
}
```
- Returns: a json with the next keys:
    - success: True.
    - movies: a list of actors that have the next keys.
        - id: (int) The identificator.
        - title: (string) The title of the movie.
        - release_date:(string) The release date of the movie in the following format "mm-dd-yyyy"
        - actors: (array) The actors who acted in the movie.

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
- Create an actor through json request and bearer token for authentication. 
- Request Arguments: 
    - Header authorization bearer token.
    - JSON Request. If you add None valuesto name or gender, you will raise a 400 error
        - name: (string) The name of the actor.
        - gender: (string) The gender of the actor.
        - movies: (array) The id of the movies where acted the actor, This movies must exist, otherwise you will raise an 422 error.

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
    - created: (int) The id of the movie created.

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
    - Json request with the followin keys. If you add None values to title or release date you will raise a 400 error
        - title: (string) The title of the movie.
        - release_date: (string) The release_date of the movie, with the following format 'mm-dd-yyy'.
        - actors: (array) The actors of the movie, this actors have to exist or will raise an 422 error.

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
- Delete an actor utilizing a bearer token and the id of the actor through path parameter
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
    - deleted: (int) The id of the actor deleted.

Example
```JSON
{
    "id": 3,
    "deleted": true
}

```

#### DELETE '/movies/\<int:id>'
- Delete a movie through a bearer token and the id of the movie through path parameter
- Request Arguments:
    - Header authorization bearer token.
    - Path parameter utilizing the id.

Example:

DELETE 'localhost:5000/movies/3'

header
```JSON
{
    "authorization": "Bearer <Token>"
}
```
- Returns: a json with the next keys:
    - success: True.
    - deleted: (int) The id of the actor deleted.

Example
```JSON
{
    "deleted": 3,
    "success": true
}
```

#### PATCH '/actors/\<int:id>/update'
- Update an actor with a json request data, authorization bearer token and the id through path parameter.
- Request Arguments:
    - Header authorization bearer token.
    - Path parameter utilizing the id of the actor to be updated.
    - A json request with one or more of the following keys
        - name: (string) The name of the actor
        - gender: (string) The gender of the actor
        - movies: (array) The movies where acted the actor, This movies must exist or will raise an 422 error.

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
        - id: (int) The identificator
        - name: (string) The name of the actor
        - gender: (string) The gender of the actor
        - movies: (array) The movies where acted the actor.

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
- Update a movie with the data to be changed through a json request data, authorization bearer token and the id through the path parameter.
- Request Arguments:
    - Header authorization bearer token.
    - Path parameter utilizing the id of the movie to be updated.
    - A json request with one or more of the following keys
        - title: (string) the title of the movie.
        - release_date: (string )the release_date of the movie, with the following format 'mm-dd-yyyy'.
        - actors: (array)the actors of the movie, this actors have to exist or will raise an 422 error.

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
    - movie: the movie updated with the following keys
        - id: (int) The id of the movie
        - title: (string) The title of the movie
        - release_date: (string) The release date of the movie in the following format 'mm-dd-yyyy'
        - actors: (arrays) The actors who acted in the movie.

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
