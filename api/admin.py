from django.contrib import admin
from .models import Artist, Album, Track, Genre

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'get_duration_display']
    filter_horizontal = ['artists', 'genres']
    prepopulated_fields = {'slug': ('title',)}