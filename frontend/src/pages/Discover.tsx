import React, { useEffect, useState } from "react";
import SongList from "../components/SongList/SongList";
import "./Discover.css";

interface Song {
    title: string;
    artist: string;
    release_year?: string
}
  
const Discover: React.FC = () => {
  const [newSongs, setNewSongs] = useState<any[]>([]);
  const [trendingSongs, setTrendingSongs] = useState<any[]>([]);
  const [classicSongs, setClassicSongs] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/discover/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setNewSongs(data.new || []);
        setTrendingSongs(data.trending || []);
        setClassicSongs(data.classics || []);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching discover songs:", error);
        setError("Failed to load songs.");
        setLoading(false);
      });
  }, []);

  return (
    <div className="discover-container">
      <h1>Discover</h1>

      {loading ? <p>Loading songs...</p> : null}
      {error ? <p className="error-message">{error}</p> : null}

      <div className="song-section">
        <h2>New Songs</h2>
        <SongList songs={newSongs} />
      </div>

      <div className="song-section">
        <h2>Trending Songs</h2>
        <SongList songs={trendingSongs} />
      </div>

      <div className="song-section">
        <h2>Classics</h2>
        <SongList songs={classicSongs} />
      </div>
    </div>
  );
};

export default Discover;
