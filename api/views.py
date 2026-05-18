from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Artist, Album, Track, Genre

# ====================== ВИКОНАВЦІ ======================

@api_view(['GET'])
def artist_list(request):
    """GET /api/artists/ - Список усіх виконавців"""
    artists = Artist.objects.all()
    data = [{
        'id': a.id,
        'name': a.name,
        'slug': a.slug,
        'country': a.country,
        'image': a.image.url if a.image else None,
    } for a in artists]
    return Response(data)


@api_view(['GET', 'POST'])
def artist_detail(request, pk):
    """GET /api/artists/{id}/  
       POST /api/artists/{id}/ (оновлення)"""
    artist = get_object_or_404(Artist, pk=pk)

    if request.method == 'GET':
        data = {
            'id': artist.id,
            'name': artist.name,
            'slug': artist.slug,
            'bio': artist.bio,
            'country': artist.country,
            'image': artist.image.url if artist.image else None,
            'created_at': artist.created_at,
        }
        return Response(data)

    # POST/PUT/PATCH — тільки для адміністратора
    if request.method == 'POST':
        if not request.user.is_staff:
            return Response({"detail": "Доступ заборонено"}, status=status.HTTP_403_FORBIDDEN)
        
        artist.name = request.data.get('name', artist.name)
        artist.bio = request.data.get('bio', artist.bio)
        artist.country = request.data.get('country', artist.country)
        artist.save()
        return Response({"detail": "Виконавця оновлено"})


@api_view(['GET'])
def artist_albums(request, pk):
    """GET /api/artists/{id}/albums/"""
    artist = get_object_or_404(Artist, pk=pk)
    albums = artist.albums.all()
    data = [{
        'id': album.id,
        'title': album.title,
        'release_date': album.release_date,
    } for album in albums]
    return Response(data)


@api_view(['GET'])
def artist_tracks(request, pk):
    """GET /api/artists/{id}/tracks/"""
    artist = get_object_or_404(Artist, pk=pk)
    tracks = artist.tracks.all()
    data = [{
        'id': t.id,
        'title': t.title,
        'duration': t.get_duration_display(),
    } for t in tracks]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def artist_create(request):
    """POST /api/artists/ - створення нового виконавця"""
    serializer_data = {
        'name': request.data.get('name'),
        'bio': request.data.get('bio', ''),
        'country': request.data.get('country', ''),
    }
    artist = Artist.objects.create(**serializer_data)
    return Response({
        'id': artist.id,
        'name': artist.name,
        'message': 'Виконавець успішно створений'
    }, status=status.HTTP_201_CREATED)


# ====================== АЛЬБОМИ ======================

@api_view(['GET'])
def album_list(request):
    """GET /api/albums/"""
    albums = Album.objects.select_related('artist').all()
    data = [{
        'id': a.id,
        'title': a.title,
        'artist': a.artist.name,
        'release_date': a.release_date,
    } for a in albums]
    return Response(data)


@api_view(['GET'])
def album_detail(request, pk):
    """GET /api/albums/{id}/"""
    album = get_object_or_404(Album, pk=pk)
    data = {
        'id': album.id,
        'title': album.title,
        'artist': album.artist.name,
        'release_date': album.release_date,
        'cover': album.cover.url if album.cover else None,
    }
    return Response(data)


@api_view(['GET'])
def album_tracks(request, pk):
    """GET /api/albums/{id}/tracks/"""
    album = get_object_or_404(Album, pk=pk)
    tracks = album.tracks.all()
    data = [{
        'id': t.id,
        'title': t.title,
        'track_number': t.track_number,
        'duration': t.get_duration_display(),
    } for t in tracks]
    return Response(data)


# ====================== ТРЕКИ ======================

@api_view(['GET'])
def track_list(request):
    """GET /api/tracks/"""
    tracks = Track.objects.select_related('album').prefetch_related('artists').all()
    data = []
    for t in tracks:
        data.append({
            'id': t.id,
            'title': t.title,
            'artists': [artist.name for artist in t.artists.all()],
            'album': t.album.title if t.album else None,
            'duration': t.get_duration_display(),
        })
    return Response(data)


@api_view(['GET'])
def track_detail(request, pk):
    """GET /api/tracks/{id}/"""
    track = get_object_or_404(Track, pk=pk)
    data = {
        'id': track.id,
        'title': track.title,
        'artists': [a.name for a in track.artists.all()],
        'album': track.album.title if track.album else None,
        'duration': track.get_duration_display(),
        'is_explicit': track.is_explicit,
        'lyrics': track.lyrics,
    }
    return Response(data)


# ====================== ЖАНРИ ======================

@api_view(['GET'])
def genre_list(request):
    """GET /api/genres/"""
    genres = Genre.objects.all()
    data = [{'id': g.id, 'name': g.name, 'slug': g.slug} for g in genres]
    return Response(data)


@api_view(['GET'])
def genre_tracks(request, pk):
    """GET /api/genres/{id}/tracks/"""
    genre = get_object_or_404(Genre, pk=pk)
    tracks = genre.tracks.all()
    data = [{
        'id': t.id,
        'title': t.title,
        'artists': [a.name for a in t.artists.all()],
    } for t in tracks]
    return Response(data)
