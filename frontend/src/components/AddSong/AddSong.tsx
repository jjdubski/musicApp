import React, { useEffect, useState } from "react";
import "./AddSong.css";
import Song from "../Song/Song";
import plusIcon from "/plus-icon.png"

interface Song {
  id: number;
  name: string;
  artist: string;
  album: string;
  coverArt: string;
}

const AddSong: React.FC = () => {
  const [songs, setSongs] = useState<Song[]>([]);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await fetch("http://localhost:8000/generate_response/");//not a real endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch recommended songs.");
        }
        const data = await response.json();
        setSongs(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error fetching songs:", error);
        setError("Failed to load songs. Try again later.");
      }
    };

    fetchSongs();
  }, []);

  return (
    <div className="recommended-songs-container">
      <h2 className="recommended-songs-title">Recommended Songs</h2>
      <div className="song-scroll">
        {error ? (
          <p className="error-message">{error}</p>
        ) : songs.length > 0 ? (
          songs.map((song) => (
            <div key={song.id} className="add-song">
              <Song
                title={song.name}
                artist={song.artist}
                album={song.album}
                img={song.coverArt}
              />
              <button className="add-button" onClick={() => console.log(`Added ${song.name} to playlist`)}>
              <img src={plusIcon} alt="Add song" className="add-icon" />
              </button>
            </div>
          ))
        ) : (
          <p className="no-songs">No recommended songs available</p>
        )}
      </div>
    </div>
  );
};

export default AddSong;
