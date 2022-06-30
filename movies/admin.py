from django.contrib import admin
from .models import Movie, Genre, Track, MovieTrack, Playlist, Collection, MovieRole


# Register your models here.

class PlaylistRecordInLine(admin.TabularInline):
    model = Playlist.movies.through
    extra = 1


class PlaylistAdmin(admin.ModelAdmin):
    inlines = (
        PlaylistRecordInLine,
    )


class CollectionRecordInLine(admin.TabularInline):
    model = Collection.playlists.through
    extra = 1


class CollectionAdmin(admin.ModelAdmin):
    inlines = (
        CollectionRecordInLine,
    )


class MovieRoleInLine(admin.TabularInline):
    model = Movie.cast.through
    extra = 1


class MovieTrackInline(admin.TabularInline):
    model = Movie.songs.through
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = (
        MovieRoleInLine,
        MovieTrackInline,
    )




admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.register(Track)
admin.register(MovieTrack)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Collection, CollectionAdmin)
