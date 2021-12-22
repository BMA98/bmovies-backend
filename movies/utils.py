import tmdbsimple as tmdb
from config import TMDB_KEY
from history.models import MovieHistory
from movies.models import Movie, Genre, Country, Language, MovieRole
from people.models import Star, Director, ScreenWriter, PhotographyDirector
from users.models import User, MovieSeen
from django.utils import timezone


def get_movie_from_tmdb(tmdb_id, year):
    tmdb.API_KEY = TMDB_KEY
    movie = tmdb.Movies(tmdb_id)
    movie_data, language, genres, countries = get_basic_info_from_tmdb(movie)
    cast, directors, screenwriters, photography_directors, producers = get_movie_credits_from_tmdb(movie)
    return movie_data, language, genres, countries, cast, directors, screenwriters, photography_directors, producers


def get_basic_info_from_tmdb(movie, year=None):
    """
    Returns the basic info, the genres and the production company of a given movie
    :param movie: the tmdb movie object
    :param year: the year in which the movie was released
    :return: dictionary of basic data, original language,  list of genres and list of production companies
    """
    movie_data = {}
    response = movie.info(language='es')
    movie_data['tmdb_id'] = response['id']
    movie_data['imdb_id'] = response['imdb_id']
    movie_data['original_title'] = response['original_title']
    movie_data['title'] = response['title']
    movie_data['year'] = year
    movie_data['release_date'] = response['release_date']
    movie_data['runtime'] = response['runtime']
    movie_data['overview'] = response['overview']
    movie_data['poster'] = response['poster_path']
    movie_data['backdrop'] = response['backdrop_path']
    return movie_data, response['original_language'], response['genres'], response['production_countries']


def get_movie_credits_from_tmdb(movie):
    """
    It returns the cast ids, and main crew roles ids for a given movie
    :param movie: the tmdb movie object
    :return: list of ids for cast, director, screenwriters, photography directors and producers
    """
    credits = movie.credits()
    cast_full = credits['cast']
    cast = []
    for people in cast_full[:12]:
        cast.append({'id': people['id'], 'role': people['character']})
    directors = []
    screenwriters = []
    photography_directors = []
    producers = []
    for person in credits['crew']:
        if person['job'] == 'Director':
            directors.append(person['id'])
        elif person['job'] == 'Screenplay' or person['job'] == 'Writer':
            screenwriters.append(person['id'])
        elif person['job'] == 'Director of Photography':
            photography_directors.append(person['id'])
        elif person['job'] == 'Producer':
            producers.append(person['id'])
    return cast, directors, screenwriters, photography_directors, producers


def get_people_from_tmdb(tmdb_id):
    tmdb.API_KEY = TMDB_KEY
    people_data = {}
    people = tmdb.People(tmdb_id)
    response = people.info(language='es-ES')
    people_data['tmdb_id'] = response['id']
    people_data['imdb_id'] = response['imdb_id']
    people_data['name'] = response['name']
    people_data['biography'] = response['biography']
    people_data['gender'] = response['gender']
    people_data['profile_path'] = response['profile_path']
    people_data['birthday'] = response['birthday']
    people_data['birthplace'] = response['place_of_birth']
    people_data['deathday'] = response['deathday']
    # Try again if no biography is available
    if people_data['biography'] == '':
        response = people.info(language='es-MX')
        people_data['biography'] = response['biography']
    return people_data


def push_movie_to_db(movie_data, language, genres, countries, cast, directors, screenwriters, photography_directors,
                     producers):
    lang, _ = Language.objects.get_or_create(iso=language)
    movie_data['language'] = lang
    movie, _ = Movie.objects.update_or_create(tmdb_id=movie_data['tmdb_id'], defaults=movie_data)
    for elem in genres:
        genre, _ = Genre.objects.get_or_create(id=elem['id'], name=elem['name'])
        movie.genres.add(genre)
    for elem in countries:
        country, _ = Country.objects.get_or_create(iso=elem['iso_3166_1'], name=elem['name'])
        movie.countries.add(country)
    for elem in cast:
        people_data = get_people_from_tmdb(elem['id'])
        people, _ = Star.objects.update_or_create(tmdb_id=elem['id'], defaults=people_data)
        MovieRole.objects.get_or_create(movie=movie, star=people, role=elem['role'])
    for elem in directors:
        people_data = get_people_from_tmdb(elem)
        people, _ = Director.objects.update_or_create(tmdb_id=elem, defaults=people_data)
        movie.directors.add(people)
    for elem in screenwriters:
        people_data = get_people_from_tmdb(elem)
        people, _ = ScreenWriter.objects.update_or_create(tmdb_id=elem, defaults=people_data)
        movie.screenwriters.add(people)
    for elem in photography_directors:
        people_data = get_people_from_tmdb(elem)
        people, _ = PhotographyDirector.objects.update_or_create(tmdb_id=elem, defaults=people_data)
        movie.photography_directors.add(people)
    return movie.tmdb_id


def add_movie_to_user(user_id, movie_id, date, hour, channel=0):
    try:
        print(f'Insertando pelicula {movie_id} en usuario {user_id}')
        user = User.objects.get(id=user_id)
        movie = Movie.objects.get(tmdb_id=movie_id)
        if date:
            datetime = timezone.datetime.strptime(date + ' ' + hour, '%Y-%m-%d %H:%M:%S')
            entry = MovieHistory.objects.create(user=user, movie=movie, timestamp=datetime.astimezone(), channel_id=channel)
            entry.save()
        else:
            seen = MovieSeen.objects.create(user=user, movie=movie)
            seen.save()
    except Exception as e:
        print(e)


def save_movie_event(tmdb_id, year, users, date, time, channel):
    try:
        movie_data, language, genres, countries, cast, directors, screenwriters, \
            photography_directors, producers = get_movie_from_tmdb(tmdb_id=tmdb_id, year=year)
        tmdb_id = push_movie_to_db(movie_data, language, genres, countries, cast, directors, screenwriters,
                                   photography_directors, producers)
        for user in users:
            add_movie_to_user(user_id=user, movie_id=tmdb_id, date=date, hour=time, channel=channel)
    except Exception as e:
        print(e)