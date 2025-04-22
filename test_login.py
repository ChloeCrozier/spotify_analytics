import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-read-private playlist-modify-private playlist-modify-public",
    cache_path=".cache"
))

user = sp.current_user()
print(f"Logged in as: {user['display_name']} ({user['id']})")