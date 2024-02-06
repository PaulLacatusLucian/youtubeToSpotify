import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient(object):
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=["user-library-read", "playlist-modify-private", "playlist-modify-public"]
        ))

    def search_song(self, artist, track):
        query = f'{artist} {track}'
        results = self.sp.search(q=query, type='track')

        items = results.get('tracks', {}).get('items', [])

        if not items:
            print(f"No results found for {artist} - {track}")
            # raise Exception(f"No song found for {artist} - {track}")

        first_result = items[0]

        if 'id' in first_result:
            return first_result['id']
        else:
            print(f"Invalid result for {artist} - {track}: {first_result}")

    def get_current_user_info(self):
        user_info = self.sp.current_user()
        return user_info['id']

    def create_new_playlist(self, user_id, playlist_name, is_public=True, is_collaborative=False, description=None):
        playlist = self.sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=is_public,
            collaborative=is_collaborative,
            description=description
        )

        return playlist['id']

    def add_song_to_spotify_playlist(self, playlist_id, song_id):
        self.sp.playlist_add_items(playlist_id, items=[f"spotify:track:{song_id}"])
