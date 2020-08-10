from django.test import TestCase
from model_bakery import baker

from people.models import Star, ScreenWriter, Producer, Director, PhotographyDirector


class StarTestCase(TestCase):

    def setUp(self):
        self.star = baker.make('people.Star')

    def test_creation(self):
        self.assertTrue(isinstance(self.star, Star))

    def test_string(self):
        self.assertEqual(self.star.__str__(), self.star.name)


class DirectorTestCase(TestCase):

    def setUp(self):
        self.director = baker.make('people.Director')

    def test_creation(self):
        self.assertTrue(isinstance(self.director, Director))

    def test_string(self):
        self.assertEqual(self.director.__str__(), self.director.name)


class ProducerTestCase(TestCase):

    def setUp(self):
        self.producer = baker.make('people.Producer')

    def test_creation(self):
        self.assertTrue(isinstance(self.producer, Producer))

    def test_string(self):
        self.assertEqual(self.producer.__str__(), self.producer.name)


class ScreenWriterTestCase(TestCase):

    def setUp(self):
        self.screenwriter = baker.make('people.ScreenWriter')

    def test_creation(self):
        self.assertTrue(isinstance(self.screenwriter, ScreenWriter))

    def test_string(self):
        self.assertEqual(self.screenwriter.__str__(), self.screenwriter.name)


class PhotographyDirectorTestCase(TestCase):

    def setUp(self):
        self.photography_director = baker.make('people.PhotographyDirector')

    def test_creation(self):
        self.assertTrue(isinstance(self.photography_director, PhotographyDirector))

    def test_string(self):
        self.assertEqual(self.photography_director.__str__(), self.photography_director.name)
