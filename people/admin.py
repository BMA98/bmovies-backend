from django.contrib import admin
from .models import Star, Director, PhotographyDirector, ScreenWriter, Producer, People

# Register your models here.

admin.site.register(People)
admin.site.register(Star)
admin.site.register(Director)
admin.site.register(PhotographyDirector)
admin.site.register(ScreenWriter)
admin.site.register(Producer)