from django.urls import path
from . import views

urlpatterns = [
    path('artists/', views.artist_list),
    path('artists/create/', views.artist_create),
    path('artists/<int:pk>/', views.artist_detail),
    path('artists/<int:pk>/albums/', views.artist_albums),
    path('artists/<int:pk>/tracks/', views.artist_tracks),

    path('albums/', views.album_list),
    path('albums/<int:pk>/', views.album_detail),
    path('albums/<int:pk>/tracks/', views.album_tracks),

    path('tracks/', views.track_list),
    path('tracks/<int:pk>/', views.track_detail),

    path('genres/', views.genre_list),
    path('genres/<int:pk>/tracks/', views.genre_tracks),
]