import tmdbsimple as tmdb

import movies.models
from config import TMDB_KEY
from movies.models import Genre, Country, MovieRole, Movie
from people.models import People

tmdb.API_KEY = TMDB_KEY


def fetch_movie(tmdb_id: int = None, title: str = None, year: int = None) -> tmdb.Movies:
    """
    Fetches The Movie Database for a movie object given a tmdb_id param or a title and a year
    @param tmdb_id: unique id for a movie in The Movie Database
    @param title: movie title to search
    @param year: movie release year
    @return: a tmdb_simple movie object
    """
    if tmdb_id:
        return tmdb.Movies(tmdb_id)
    elif title and year:
        searcher = tmdb.Search()
        try:
            if year:
                tmdb_id = searcher.movie(query=title, year=year)['results'][0]['id']
            else:
                tmdb_id = searcher.movie(query=title)['results'][0]['id']
            return tmdb.Movies(tmdb_id)
        except IndexError:
            print(f'No movie {title} ({year}) has been found')
    else:
        raise Exception(f'Function needs tmdb_id OR title and year')


def parse_movie(movie: tmdb.Movies) -> dict:
    """
    Given a tmdb_simple Movie object, it returns a dictionary with the relevant data in latin spanish or iberian spanish
    @param movie: the tmdb_simple Movie object
    @return: a dictionary with movie data
    """
    data = movie.info(language='es-MX')
    overview = data.pop('overview')
    if not overview or overview == '':
        overview = movie.info(language='es-ES')['overview']
    data['tmdb_id'] = data.pop('id')
    data['overview'] = overview
    data['year'] = data['release_date'].split('-')[0]
    data['poster'] = data.pop('poster_path')
    data['backdrop'] = data.pop('backdrop_path')
    data['language'] = data.pop('original_language')
    data['countries'] = data.pop('production_countries')
    keys = ['tmdb_id', 'imdb_id', 'original_title', 'title', 'year', 'release_date',
            'runtime', 'overview', 'poster', 'backdrop', 'language', 'countries', 'genres']
    return {key: data[key] for key in keys}


def parse_credits(movie: tmdb.Movies) -> dict:
    """
    Given a tmdb_simple Movie object, it returns a dictionary with cast and key crew roles
    @param movie: a tmdb_simle Movie object
    @return: a dictionary with credits data
    """
    credits_themoviedb = movie.credits()
    cast = [{'id': people['id'], 'role': people['character']} for people in credits_themoviedb['cast'][:12]]
    credits_parsed = {
        'cast': cast,
        'directors': [],
        'screenwriters': [],
        'photography_directors': []
    }
    for people in credits_themoviedb['crew']:
        if people['job'] == 'Director':
            credits_parsed['directors'].append(people['id'])
        elif people['job'] == 'Screenplay' or people['job'] == 'Writer':
            credits_parsed['screenwriters'].append(people['id'])
        elif people['job'] == 'Director of Photography':
            credits_parsed['photography_directors'].append(people['id'])
    return credits_parsed


def fetch_people(tmdb_id: int):
    """
    Given a unique id of a people in The Movie Database, fetches the data and returns a dictionary with relevant data
    @param tmdb_id: unique id
    @return: dictionary with people data
    """
    people = tmdb.People(tmdb_id)
    data = people.info(language='es-MX')
    biography = data.pop('biography')
    if not biography or biography == '':
        biography = people.info(language='es-ES')['biography']
    data['tmdb_id'] = data.pop('id')
    data['biography'] = biography
    data['birthplace'] = data.pop('place_of_birth')
    keys = ['tmdb_id', 'imdb_id', 'name', 'biography', 'gender', 'profile_path', 'birthday', 'birthplace', 'deathday']
    return {key: data[key] for key in keys}


def add_genres_to_movie(movie: movies.models.Movie, genres: dict) -> None:
    for record in genres:
        try:
            genre, _ = Genre.objects.get_or_create(id=record['id'], defaults={'name': record['name']})
            movie.genres.add(genre)
        except Exception as e:
            print(e)
            pass


def add_countries_to_movie(movie: movies.models.Movie, countries: list[dict]) -> None:
    for record in countries:
        try:
            genre, _ = Country.objects.get_or_create(iso=record['iso_3166_1'], defaults={'name': record['name']})
            movie.countries.add(genre)
        except Exception as e:
            print(e)
            pass


def update_or_create_person(tmdb_id: int) -> People:
    data = fetch_people(tmdb_id)
    people, _ = People.objects.update_or_create(tmdb_id=data.pop('tmdb_id'), defaults=data)
    return people


def add_cast_to_movie(movie: Movie, cast: list[dict]) -> None:
    for record in cast:
        try:
            people = update_or_create_person(record['id'])
            role, _ = MovieRole.objects.get_or_create(movie=movie, star=people, role=record['role'])
            print(f'Inserting cast member {people} in movie {movie}')
        except Exception as e:
            print(e)
            pass


def add_crew_to_movie(movie: Movie, crew: list[int], role: str = 'director') -> None:
    for record in crew:
        people = update_or_create_person(record)
        if role == 'director':
            movie.directors.add(people)
        elif role == 'screenwriter':
            movie.screenwriters.add(people)
        elif role == 'photography_director':
            movie.photography_directors.add(people)


def update_or_create_movie(
        tmdb_id: int = None,
        title: str = None,
        year: int = None,
        status: int = 0,
        trailer: str = None
) -> Movie:

    movie = fetch_movie(tmdb_id, title, year)
    movie_data = parse_movie(movie)
    movie_data['status'] = status
    print(f'My status is {status}')
    movie_data['trailer'] = trailer
    movie_credits = parse_credits(movie)

    genres = movie_data.pop('genres')
    countries = movie_data.pop('countries')

    movie, _ = Movie.objects.update_or_create(tmdb_id=movie_data.pop('tmdb_id'), defaults=movie_data)

    # Add genres
    add_genres_to_movie(movie, genres)
    # Add countries
    add_countries_to_movie(movie, countries)

    # Add cast members
    add_cast_to_movie(movie, movie_credits['cast'])

    ## Add crew member
    add_crew_to_movie(movie, movie_credits['directors'], 'director')
    add_crew_to_movie(movie, movie_credits['screenwriters'], 'screenwriter')
    add_crew_to_movie(movie, movie_credits['photography_directors'], 'photography_director')

    return movie
