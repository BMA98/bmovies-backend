from django.contrib import admin
from .models import Star, Director, PhotographyDirector, ScreenWriter, People

# Register your models here.

admin.site.register(People)
admin.site.register(Star)
admin.site.register(Director)
admin.site.register(PhotographyDirector)
admin.site.register(ScreenWriter)
