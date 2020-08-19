from django.test import TestCase
from model_bakery import baker
from iso_language_codes import language


from movies.models import Movie, Genre, Language


class MovieTestCase(TestCase):

   def setUp(self):
      self.movie_1 = baker.make('movies.Movie')
      self.movie_2 = baker.make('movies.Movie')

   def test_creation(self):
      self.assertTrue(isinstance(self.movie_1, Movie))
      self.assertNotEqual(self.movie_1, self.movie_2)
      self.assertEqual(len(Movie.objects.all()), 2)

   def test_string(self):
      self.assertEqual(self.movie_1.__str__(), self.movie_1.original_title)
      self.assertEqual(self.movie_2.__str__(), self.movie_2.original_title)

   def test_query_order(self):
      first = Movie.objects.all()[0]
      second = Movie.objects.all()[1]
      self.assertEqual(first, self.movie_2)
      self.assertEqual(second, self.movie_1)


class GenreTestCase(TestCase):

   def setUp(self):
      self.genre = baker.make('movies.Genre')

   def test_creation(self):
      self.assertTrue(isinstance(self.genre, Genre))

   def test_string(self):
      self.assertEqual(self.genre.__str__(), self.genre.genre)


class LanguageTestCase(TestCase):

   def setUp(self):
      self.language = Language(language_id=0, language_iso='es')

   def test_creation(self):
      self.assertTrue(isinstance(self.language, Language))

   def test_string(self):
      self.assertEqual(self.language.__str__(), language(self.language.language_iso)['Name'])
