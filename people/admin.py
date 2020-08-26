from django.contrib import admin
from .models import Star, Director, PhotographyDirector, ScreenWriter, Producer

# Register your models here.

admin.site.register(Star)
admin.site.register(Director)
admin.site.register(PhotographyDirector)
admin.site.register(ScreenWriter)
admin.site.register(Producer)