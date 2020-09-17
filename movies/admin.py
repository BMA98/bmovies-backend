from django.contrib import admin
from .models import Movie, Genre, Language, ProductionCountry, MovieRole

# Register your models here.

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(ProductionCountry)
admin.site.register(MovieRole)