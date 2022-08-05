# BMovies Backend

### Description

This project is developed with Django REST Framework, and intends to provide basic
functionality to a movie history service as a backend service. 

The structure of the project it is as follows:
- **movies**: provides the logic (models, serializers and viewsets) for storing all information related to a movie.
- **people**: provides the logic to handle people like stars, directors, screenwriters, etc.
- **users**: provides the logic for handling users, and their interactions as movies seen, movie ratings and movie reviews. The authentication logic is delegated (mostly) to rest-auth.

### How to Run
#### The power of Docker

In order to run this project you must install [Docker](https://docs.docker.com/engine/install/)
for your operating system and [Docker Compose](https://docs.docker.com/compose/install/).
Once you have that, you can follow the next steps:

- **Clone the project**: `git clone git@github.com:BMA98/bmovies-backend.git`
- **Change directory inside the project**: `cd bmovie-backend`
- **Create a file named `.env.dev`** with the following environment variables.
  - DB_USER=<your_preference>
  - DB_PASSWORD=<your_preference>
  - DB_NAME=<your_preference>
  - SECRET_KEY=<generate_a_secret_key>
  - DB_HOST=**db**
  - TMDB_KEY=<your_tmdb_key>
  - Notice how DB_HOST must coincide con the database service name in the Docker Compose, in our case is `db`. To generate a secret key for Django you can use [https://djecrety.ir](https://djecrety.ir/), and you can get a The Movie Database API from [here](https://developers.themoviedb.org/3/).
- **Run**: `docker-compose up`

If the project has been successfully launched, the server should be listening request in
`localhost:8000`. So if you try `localhost:8000/api/v1.0/movies` it should return an
empty list of movies.

#### If you don't like Docker

You can run the project as a classic Django project. You will need to create a PostgreSQL database,
and set the same environment variables that in the Docker step-by-step guide. These are consumed
by the `config.py` file in the root directory, so you can simply modify that.

Then you should create a virtual environment, install the requirements in the `requirements.txt` file and 
then run the project with `python manage.py makemigrations`, `python manage.py migrate` and
`python manage.py runserver`.
