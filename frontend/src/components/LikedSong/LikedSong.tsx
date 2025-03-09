import React, { useState, useEffect } from "react";
import "./LikedSong.css";
import likedsong from "/likedsong.png";

interface Song {
  trackID: string;
  title: string;
  artist: string;
  album: string;
  image: string;
  uri: string; 
}

// interface Playlist {
//   playlistID: string;
//   name: string;
//   image: string;
// }
interface LikedSongProps{
  song: Song
  onRemSong: (trackID: string) => void;
}



const AddSong: React.FC<LikedSongProps> = ({ song, onRemSong }) => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const img = new Image();
    img.src = song.image;
    img.onload = () => setIsLoading(false);
  }, [song]);

  const changeSong = async () => {
    const requestData = {
      uri: song.uri,
    };
    console.log("Changing song to:", song.uri);
    try {
      await fetch("http://localhost:8000/songAPI/playSong/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });
    } catch (error) {
      console.error("Error changing song:", error);
    }
  };

  return (
    isLoading ? ( 
      <></> 
    ) : 
    <div className="liked-song" onClick={changeSong}>
      <img className="song-image" src={song.image} alt={song.title} />
      <div className="song-info">
        <p className="song-title">{song.title}</p>
        <p className="song-artist">{song.artist}</p>
        <p className="song-album">{song.album}</p>
      </div>
      <div onClick={(e) => e.stopPropagation()}>
        <button className="add-button" onClick={(e) => {
          e.stopPropagation();
          console.log("Removing song: ", song.trackID);
          onRemSong(song.trackID);
        }}>
          <img src={likedsong} alt="likedsong" className="like-icon" />
        </button>
      </div>
    </div>
  );  
};

export default AddSong;

