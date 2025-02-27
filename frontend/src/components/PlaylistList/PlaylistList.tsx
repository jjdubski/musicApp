import React, { useEffect, useState } from 'react';
import './PlaylistList.css';
import Playlist from '../Playlist/Playlist';

interface Playlist {
    id: string;
    name: string;
    coverArt: string;
}

interface PlaylistListProps {
    onSelectPlaylist: (playlist: Playlist) => void;
}

const PlaylistList: React.FC<PlaylistListProps> = ({ onSelectPlaylist }) => {
    const [playlists, setPlaylists] = useState<Playlist[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch('http://localhost:8000/playlistAPI/playlists/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Data received:', data);
                setPlaylists(Array.isArray(data) ? data : []);
                setError(null);
            })
            .catch(error => {
                console.error('Error fetching Playlists:', error);
                setError('Failed to fetch Playlists. Please try again later.' + error);
            });
    }, []);

    return (
        <div>
            {error ? (
                <p style={{ color: 'red' }}>{error}</p>
            ) : playlists.length === 0 ? (
                <p>No playlists available</p>
            ) : (
                <div className="playlists-grid">
                    {playlists.map(playlist => (
                        <div key={playlist.id} onClick={() => onSelectPlaylist(playlist)}>
                            <Playlist
                                title={playlist.name}
                                img={playlist.coverArt}
                            />
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default PlaylistList;

