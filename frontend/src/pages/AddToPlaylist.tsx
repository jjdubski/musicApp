import React, { useState, useEffect } from 'react';
//import './AddToPlaylist.css';
import User from '../components/User/User'; // Ensure this path is correct
import SpotifyButton from '../components/SpotifyButton/SpotifyButton';
import AddSong from '../components/AddSong/AddSong';
import PlaylistList from '../components/PlaylistList/PlaylistList';
import RecomendedSongList from '../components/RecomendedSongList/RecomendedSongList';

interface Playlist {
    id: string;
    name: string;
    coverArt: string;
}

const AddToPlaylist: React.FC = () => {
    const [currentUser, setCurrentUser] = useState({
        email: '',
        username: '',
        image: '/spotify-logo.png'
    });
    const [isLoading, setIsLoading] = useState(true);
    const [selectedPlaylist, setSelectedPlaylist] = useState<Playlist | null>(null);

    useEffect(() => {
        fetch('http://localhost:8000').then(res => res.json()).then(data => {
            setCurrentUser({
                email: data.user.email || '',
                username: data.user.display_name || '',
                image: data.user.image || '/spotify-logo.png'
            });
            console.log(data);
            setIsLoading(false);
        });
    }, []);

    const handlePlaylistSelect = (playlist: Playlist) => {
        setSelectedPlaylist(playlist);
    };

    return (
        !isLoading ? (
            <div className="add-to-playlist-container">
                <div className="playlist-container">
                    {currentUser.email ? (
                        <User username={currentUser.username} image={currentUser.image} />
                    ) : (
                        <div className="spotify-button-container">
                            <SpotifyButton 
                                title="Link Spotify"
                                img="./SpotifyButton.png"
                            />
                        </div>
                    )}

                    <h2 className="playlist-title">PLAYLISTS</h2>
                    <div className="playlist-scroll">
                        <PlaylistList/>
                    </div>
                    
                    <div className="recommended-songs-container">
                        <h2 className="recommended-songs-title">Recommended Songs</h2>
                        <div className="song-scroll">
                            <RecomendedSongList playlist={selectedPlaylist} />
                        </div>
                    </div>  
                </div>
            </div>
        ) : (
            <></>
        )
    );
};

export default AddToPlaylist;
