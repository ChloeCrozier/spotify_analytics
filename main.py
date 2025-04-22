import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

def get_audio_features_in_batches(spotify, track_ids, batch_size=50):  # drop to 50 for safety
    audio_features = []
    for i in range(0, len(track_ids), batch_size):
        batch = [tid for tid in track_ids[i:i + batch_size] if tid]  # make sure IDs aren't None
        try:
            if batch:
                features = spotify.audio_features(batch)
                if features:
                    audio_features.extend(features)
        except spotipy.exceptions.SpotifyException as e:
            print(f"⚠️ Skipping batch {i}-{i+batch_size}, Spotify error: {e}")
    return audio_features

def print_playlist_info(sp, playlist_id):
    playlist = sp.playlist(playlist_id)
    print(f"\n🎵 Playlist: {playlist['name']}")
    print(f"📜 Description: {playlist['description']}")
    print(f"👤 Owner: {playlist['owner']['display_name']}")
    
    track_ids = [
        item['track']['id']
        for item in playlist['tracks']['items']
        if item['track'] and item['track']['id']  # ensure not None
    ]


    print(f"\n🔢 Total Tracks: {len(track_ids)}")

    features = get_audio_features_in_batches(sp, track_ids)
    print("\n🎧 Audio Features (First 5 Tracks):")
    for f in features[:5]:
        if f:
            print(f"\n🎶 Track ID: {f['id']}")
            print(f"  💃 Danceability: {f['danceability']}")
            print(f"  ⚡ Energy: {f['energy']}")
            print(f"  🕒 Tempo: {f['tempo']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <playlist_id>")
        return

    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    playlist_id = sys.argv[1]

    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    print_playlist_info(sp, playlist_id)

if __name__ == "__main__":
    main()