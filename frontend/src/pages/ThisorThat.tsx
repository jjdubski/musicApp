import React, { useState, useEffect } from 'react';
import SongSelector from '../components/SongSelector/SongSelector';
import SongCard from '../components/Songcard/SongCard';
import Song from '../components/Song/Song';
import './ThisorThat.css';
import SideMenu from '../components/SideMenu/SideMenu';
import { Link } from 'react-router-dom';

interface Song {
    trackID: string;
    title: string;
    artist: string;
    album: string;
    // releaseDate: string;
    image: string;
    uri: string; 
}

const ThisorThat: React.FC = () => {
    const song = {
        title: "Song Title",
        artist: "Artist Name",
        image: "https://via.placeholder.com/150", // Replace with actual image URL
        spotifyUrl: "https://open.spotify.com" // Replace with actual Spotify URL
    };
    
    const [playlistSongs, setPlaylistSongs] = useState<Song[]>([]);
    const [selectedPlaylistID, setSelectedPlaylistID] = useState<string | null>("liked_songs");
    const hasFetchedSongs = React.useRef(false);


    useEffect(() => {
        const fetchPlaylists = async () => {
            if(!selectedPlaylistID){
                return
            }
            try {
                const response = await fetch(`http://localhost:8000/playlistAPI/getPlaylistSongs/${selectedPlaylistID}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setPlaylistSongs(Array.isArray(data) ? data : []);
            }
            catch (error) {
                console.error('Error fetching Playlist songs:', error);
            }
            hasFetchedSongs.current = false; // Allow new recommendations
        }
        
        fetchPlaylists();
    }, [selectedPlaylistID]);

    const handleSelectPlaylist = (playlistID: string) => {
        setPlaylistSongs([]); // Reset songs when switching playlists
        setSelectedPlaylistID(playlistID);
    };


    return (
        <div>
            <h1>This or That</h1>
            {/* <button onClick={() => handleSelectPlaylist("liked_songs")} >playlist</button> */}
            <SongSelector 
                title={song.title} 
                artist={song.artist} 
                image={song.image} 
                spotifyUrl={song.spotifyUrl} 
                songs={playlistSongs} // Pass the song as a list for dropdown
            />
            {playlistSongs.length > 0 && (
                <SongCard 
                    trackID={playlistSongs[0].trackID}
                    title={playlistSongs[0].title}
                    artist={playlistSongs[0].artist}
                    album={playlistSongs[0].album}
                    image={playlistSongs[0].image}
                    uri={playlistSongs[0].uri}
                />
            )}
         
        </div>
    );
};

export default ThisorThat;