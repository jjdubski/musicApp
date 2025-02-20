import logging
from django.http import HttpResponse, JsonResponse
from datetime import datetime

from django.shortcuts import redirect

from playlists.models import Playlist
from songs.models import Song
import spotipy
import os
from spotipy import SpotifyOAuth

from utils.spotifyClient import sp
def index(request):
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d-%m-%Y")
    currentUser = None
    if "spotify_token" not in request.session:
        currentUser = sp.current_user()

    data = {
        'current_time': current_time,
        'current_date': current_date,
        'user': {
            'id': currentUser['id'],
            'display_name': currentUser['display_name'],
            'email': currentUser['email']
        }
    }

    return JsonResponse(data)

def login(request):
    # Redirect user to Spotify authorization URL
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)


def logout(request):
    request.session.flush()
    return redirect('http://localhost:3000/login')

def callback(request):
    try:
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No authorization code provided"}, status=400)
            
        tokenInfo = sp.auth_manager.get_access_token(code)
        request.session["spotify_token"] = tokenInfo["access_token"]
        
        songs_success = populateSongs()
        playlists_success = populatePlaylist()
        
        if not (songs_success and playlists_success):
            logger = logging.getLogger(__name__)
            logger.error("Failed to populate songs or playlists")
            
        return redirect('http://localhost:3000/')
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error in callback: {str(e)}")
        return JsonResponse({"error": "Authentication failed"}, status=500)

def populateSongs():
    try:
        results = sp.current_user_top_tracks()
        songs = results['items']
        
        for song in songs:
            if not Song.objects.filter(trackID=song['id']).exists():
                release_date = datetime.strptime(song['album']['release_date'], '%Y-%m-%d').date()
                Song.objects.create(
                    trackID=song['id'],
                    title=song['name'],
                    artist=song['artists'][0]['name'],
                    album=song['album']['name'],
                    release_date=release_date,
                    genre=", ".join(song.get('genres', [])),
                    coverArt=song['album']['images'][0]['url'] if song['album']['images'] else None
                )
        return True
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error populating songs: {str(e)}")
        return False
    
def populatePlaylist():
    try:
        results = sp.current_user_playlists()
        playlists = results['items']
        
        for playlist in playlists:
            # Check if playlist already exists
            if not Playlist.objects.filter(name=playlist['name']).exists():
                Playlist.objects.create(
                    name=playlist['name'],
                    description=playlist.get('description', ''),  # Use get() with default value
                    coverArt=playlist['images'][0]['url'] if playlist['images'] else None
                )
                logger = logging.getLogger(__name__)
                logger.info(playlist['images'][0]['url'])
                
        return True
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error populating Playlist: {str(e)}")
        return False
    
                
        
    
    

# def getSong(request):
#     #ensure user is logged-in
#     if "spotify_token" not in request.session:
#         return JsonResponse({"error": "User must be logged in to Spotify"}, status = 401)
    
#     results = sp.current_user_top_tracks(limit = 10)
#     songs = results['items']
    
#     songList = []
    
#     for song in songs:
#         songList.append({
#             'name': song['name'],
#             'artist': song['artists'][0]['name'],
#             'album': song['album']['name'],
#             'previewURL': song['preview_url']
#         })
        
#     return JsonResponse[songList]