import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'
import Home from './pages/Home'
import Songs from './pages/Songs'
import Playlists from './pages/Playlists'
import AddtoPlaylist from './pages/AddToPlaylist'
// import WebPlayback from './components/WebPlayback/WebPlayback'
import { useEffect, useState } from 'react'
import SideMenu from './components/SideMenu/SideMenu.tsx'
import Search from './pages/Search.tsx'
import SpotifyPlayer from 'react-spotify-web-playback';
import PlaylistDetails from './pages/PlaylistDetails.tsx'
import ThisOrThat from './pages/ThisorThat'
import Discover from "./pages/Discover"

function App() { 
  const [token, setToken] = useState<string | null>(null)
  const [user, setSubscription] = useState<string>('')
  const [uris, setUris] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetch('http://localhost:8000/getToken')
      .then(res => res.json())
      .then(data =>{
        if (data) {
          console.log('Token: ', data.access_token)
          setToken(data.access_token)
        }
        else {
          console.error('Failed to get token')
        }
      }
    )
    .catch(error => console.error('Error Fetching Token: ', error))
  }
  ,[])

  useEffect(() => {
    if (token !== null) {
      fetch('http://localhost:8000/getUser')
        .then(res => res.json())
        .then(data => {
          if (data) {
            // console.log('User: ', data)
            
          
            setSubscription(data.product)
          }
          else {
            console.error('Failed to set user')
          }
        }
      )
      .catch(error => console.error('Error Fetching User: ', error))

      // needs implementation on backend for pulling and setting URI
      fetch('http://localhost:8000/api/getUris')
        .then(res => {
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        })
        .then(data => {
          if (data) {
            console.log('URIs: ', data)
            setUris(data.uris)
          }
          else {
            console.error('Failed to get URIs')
          }
        })
        .catch(error => console.error('Error Fetching URIs: ', error))
        setIsLoading(false)
    }
  }, [token])

  useEffect(() => {
    const handleBeforeUnload = () => {
      // Perform any cleanup or save state here
      console.log('User is about to leave the page');
      const playerElement = document.querySelector('.player-container');
      if (playerElement) {
        playerElement.remove();
      }
      setToken(null);
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  return (
    <Router>
      <div className='App'>
      <SideMenu />
      {isLoading ? (
        <></>
      ) : (
        <>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/songs" element={<Songs />} />
          <Route path="/playlists" element={<Playlists />} />
          <Route path="/search" element={<Search />} />
          <Route path="/playlist/:playlistID" element={<PlaylistDetails />} />
          <Route path="/add-to-playlist" element={<AddtoPlaylist />} />
          <Route path ="/this-or-that" element={<ThisOrThat />} />
          <Route path="/discover" element={<Discover />} />

          
          {/* <Route path="logout" element={<Logout />} /> */}
          {/* <Route path='/discover' element={<Discover />} /> */}
          {/* <Route path='/this-or-that' element={<ThisOrThat />} /> */}
        </Routes>
        {/* {token && <WebPlayback token={token} />} */}
        <div className="player-container">
          <div className="player">
            {token && (user && user == 'premium') ? <SpotifyPlayer 
            token={token} 
            uris={uris.length > 0 ? uris : []} // Ensure uris is an array
            // persistDeviceSelection={true}
            // magnifySliderOnHover={true}
            initialVolume={0.75}
            showSaveIcon={true}
            syncExternalDevice={true}
            styles={{
              bgColor: 'black',
              color: 'white',
              loaderColor: '#fff',
              sliderColor: '#1cb954',
              sliderHandleColor: '#fff',
              trackArtistColor: '#ccc',
              trackNameColor: '#fff',
            }}/> : <></>}
          </div>
        </div>
        </>
      )}  
      </div>
    </Router>
  )
}

export default App
