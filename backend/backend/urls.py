"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views 
from .views import getToken, get_uris, get_discover_songs  

urlpatterns = [
    # Links to songs and playlists on backend
    path('songAPI/', include('songs.urls'), name='songAPI'),
    path('playlistAPI/', include('playlists.urls'), name='playlistAPI'),
    # Admin
    path('admin/', admin.site.urls, name='admin'),
    # OTher
    path('', views.index, name='index'),  # Default view
    path("login/", views.login, name='login'),
    path("callback/", views.callback, name='callback'),
    path('logout/', views.logout, name='logout'),
    path("getAISongRecommendations/", views.getAISongRecommendations, name='getAISongRecommendations'),
    path("getRecommendations/", views.getRecommendations, name='getRecommendations'),
    path('musicAPI/search', views.search_songs, name='search_songs'),
    path('api/discover/', get_discover_songs, name='get_discover_songs'), # Disocver page 
    path('getToken/', views.getToken, name='getToken'),
    path('getUser/', views.getUser, name='getUser'),
    path('getUris/', views.get_uris, name='get_uris'),  
]

# if settings.DEBUG:
#     urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
