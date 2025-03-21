from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'playlists', views.PlaylistViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('getPlaylists/', views.AddPlaylists, name='AddPlaylists'),
    path('getPlaylistSongs/<str:playlist_id>/', views.getPlaylistSongs, name='getPlaylistSongs'),
    path('addSongToPlaylist', views.addSongToPlaylist, name = "addSongToPlaylist"),
    path('thisorthat', views.thisOrThat, name = "thisOrThat"),
    path('generateSong/', views.generateSong, name = "generateSong"),
    path('removeSong/', views.removeSong, name = "removeSong"),
]