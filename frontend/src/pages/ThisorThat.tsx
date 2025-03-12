import React, { useState, useEffect, useRef } from 'react';
import SongSelector from '../components/SongSelector/SongSelector';
import SongCard from '../components/SongCard/SongCard';
import './ThisorThat.css';
import LikedSongList from '../components/LikedSongList/LikedSongList';

interface Song {
    trackID: string;
    title: string;
    artist: string;
    album: string;
    image: string;
    uri: string;
}

const ThisorThat: React.FC = () => {
    const [playlistSongs, setPlaylistSongs] = useState<Song[]>([]);
    const [selectedPlaylistID, setSelectedPlaylistID] = useState<string | null>("liked_songs");
    const [currentIndex, setCurrentIndex] = useState(0);
    const hasFetchedSongs = useRef(false);
    const hasFetchedSong = useRef(false);
    const [currentSong, setCurrentSong] = useState<Song | null>(null);
    
    useEffect(() => {
        if(hasFetchedSong.current){
            return;
        }
        generateSong();
        hasFetchedSong.current = true;
    }, []);

    useEffect(() => {

        const fetchPlaylists = async () => {
            if (!selectedPlaylistID) {
                return;
            }
            try {
                const response = await fetch(`http://localhost:8000/playlistAPI/getPlaylistSongs/${selectedPlaylistID}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setPlaylistSongs(Array.isArray(data) ? data : []);
                setCurrentIndex(0);
            } catch (error) {
                console.error('Error fetching Playlist songs:', error);
            }
            hasFetchedSongs.current = false;
        };

        fetchPlaylists();
    }, [selectedPlaylistID]);

    const generateSong = async () => {
        try {
            const res = await fetch('http://127.0.0.1:8000/playlistAPI/generateSong/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: `give me one more song similar to ${playlistSongs.map(song => song.title).join(", ")}`,
                    num_runs: 1,
                    userInfo: "False"
                })
            });

            const data = await res.json();
            if (res.ok) {
                const newSong: Song = {
                    trackID: data.trackID,
                    title: data.title,
                    artist: data.artist,
                    album: data.album,
                    image: data.image,
                    uri: data.uri
                };
                setCurrentSong(newSong);
            } else {
                console.error('Error:', data);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    const handleSelectPlaylist = (playlistID: string) => {
        setPlaylistSongs([]);
        setSelectedPlaylistID(playlistID);
        setCurrentIndex(0);
    };

    const addToPlaylist = async() => {
        generateSong();
        try {
            const response = await fetch("http://localhost:8000/playlistAPI/addSongToPlaylist", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    trackID: currentSong?.trackID, // Sending trackID as the 'uri' cuz thats what backend expects. Spotipy can take ether
                    playlistID: selectedPlaylistID  // Sending playlistID in the expected structure
                }),
            });

            if (response.ok) {
                console.log(`Song ${currentSong?.trackID} added successfully.`);
                                // showPopup("Song added to playlist!", "success");
                // setPlaylistSongs([...playlistSongs, { trackID, title: "Unknown", artist: "Unknown", album: "Unknown", image: "", uri: "" }]); // Temporary UI update
            } else {
                console.error("Failed to add song:", await response.text());
                // const errorMessage = await response.text();
                // showPopup(`Failed to add song: ${errorMessage}`, "error");
            }
        } catch (error) {
            console.error("Error adding song:", error);
            // showPopup("Error adding song. Please try again.", "error");
        }
    };

    const handlePrevSong = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 1 + playlistSongs.length) % playlistSongs.length);
    };


    return (
        <div className="this-or-that-page">
            <div className="this-or-that-container">
                <div className="this-or-that-content">
                    <h1>Showing Songs Like</h1>
                    <SongSelector
                        title={currentSong?.title || "No Songs"}
                        artist={currentSong?.artist || ""}
                        image={currentSong?.image || ""}
                        spotifyUrl={currentSong?.uri || ""}
                        songs={playlistSongs} />

                    {playlistSongs.length > 0 && (
                        <>
                            <SongCard
                                title={currentSong?.title || "No Songs"}
                                artist={currentSong?.artist || ""}
                                album={currentSong?.album  || ""}
                                image={currentSong?.image || ""}
                            />

                            <div className="action-buttons">
                                <button className="exit-btn" onClick={generateSong}>
                                    <img src="/exit.png" alt="Exit" />
                                </button>
                                <button className="check-btn" onClick={addToPlaylist}>
                                    <img src="/check.png" alt="Check" />
                                </button>
                            </div>
                        </>
                    )}
                </div>
            </div>

            {/* Liked Songs on the Right Side */}
            <div className="liked-songs-sidebar">
                <LikedSongList/>
            </div>
        </div>
    );
};

export default ThisorThat;
