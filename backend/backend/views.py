import logging
import os
import json
import spotipy
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from playlists.models import Playlist
from songs.models import Song
from spotipy import SpotifyOAuth
from utils.spotifyClient import sp
from utils.openai_client import client, prompt_for_song

logger = logging.getLogger(__name__)

# @csrf_exempt
# def recommend_songs(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode("utf-8"))

#             # Safely get values, defaulting to empty list if missing
#             top_artists = data.get("top_artists", [])
#             top_genres = data.get("top_genres", [])

#             if not top_artists:
#                 return JsonResponse({"error": "Missing 'top_artists' field"}, status=400)

#             # Call OpenAI function
#             recommendations = openai_client.generate_recommendations({
#                 "top_artists": top_artists,
#                 "top_genres": top_genres
#             })
            
#             return JsonResponse({"recommendations": recommendations})
        
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=405)


def index(request):
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d-%m-%Y")
    currentUser = None
    profile_pic = '/spotify-logo.png'
    
    if sp.auth_manager.get_cached_token():
        currentUser = sp.current_user()
    else:
        currentUser = {'id': '', 'display_name': '', 'email': '', 'image': ''}

    if currentUser.get('images') and currentUser['images'][0]['url']:
        profile_pic = currentUser['images'][0].get('url', '/spotify-logo.png')
    
    data = {
    #   'response': prompt_for_song ('give me a random color',1),
        'current_time': current_time,
        'current_date': current_date,
        'user': { 
            'id': currentUser['id'],
            'display_name': currentUser['display_name'],
            'email': currentUser['email'],
            'image': profile_pic
        }
    }
    # print(profile_pic)
    # print(len(currentUser['images']))
    return JsonResponse(data)


def process_json(output):
    output = output.strip().strip("```json").strip("```")
    try:
        output_list = json.loads(output)
        return output_list
    except:
        print(f"Error parsing JSON response: {output}")
        return {'title': 'Unknown', 'artist': 'Unknown'}
    
@csrf_exempt
def generate_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            prompt = data.get("prompt", "")
            num_runs = data.get("num_runs", 5)
            response = prompt_for_song(prompt, num_runs)
            # add parsing code here and return proper JSON object
            output = process_json(response)
            print(output)
            return JsonResponse({"response": output})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

#function to return list of songs

def login(request):
    # Redirect user to Spotify authorization URL
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)


def logout(request):
    request.session.flush()
    # log user out of Spotify
    sp.auth_manager.cache_handler.delete_cached_token()
    #cleanup database
    Song.objects.all().delete()
    Playlist.objects.all().delete()

    return redirect('http://localhost:3000/')

def callback(request):
    logger = logging.getLogger(__name__)
    try:
        code = request.GET.get("code")
        logger.info(f"Authorization code received: {code}")

        if code:
            try:
                token_info = sp.auth_manager.get_access_token(code)
                logger.info(f"Token info received: {token_info}")
                if token_info:
                    # Save token info to session
                    request.session["token_info"] = token_info
                    populatePlaylist()
                    populateSongs()
                    return redirect("http://localhost:3000/")
                    # return HttpResponse("Authentication successful")
                else:
                    logger.error("Failed to retrieve access token")
                    return HttpResponse("Failed to retrieve access token", status=500)
            except spotipy.SpotifyException as e:
                logger.error(f"Spotify API error: {str(e)}")
                return HttpResponse(f"Spotify API error: {str(e)}", status=500)
            except Exception as e:
                logger.error(f"Error in callback: {str(e)}")
                return HttpResponse(f"Failed to retrieve access token: {str(e)}", status=500)
        else:
            logger.error("No code provided")
            return HttpResponse("No code provided", status=400)
    except Exception as e:
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
                    playlistID=playlist['id'],
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

def getToken(request):
    tokenInfo = sp.auth_manager.get_cached_token()
    if tokenInfo:
        return JsonResponse(tokenInfo)
    else:
        return JsonResponse({"error": "No token found"}, status=404)

def getUser(request):
    tokenInfo = sp.auth_manager.get_cached_token()
    if tokenInfo:
        user = sp.current_user()
        # print(user)
        return JsonResponse(user)
    else:
        return JsonResponse({"error": "No token found"}, status=404)