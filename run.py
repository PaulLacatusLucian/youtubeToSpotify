from sportifyClient import SpotifyClient
from youtubeClient import YouTubeClient

def run():
    try:
        youtubeClient = YouTubeClient(
            r'C:\Users\paul2\PycharmProjects\youtubeToSpotify\creds\client_secret_1068687941253-gfaiobjfjft06jgs933r1npt7glckt25.apps.googleusercontent.com.json')
        sportifyClient = SpotifyClient(
            '66480a24ab1544c2b4379f051c8aaa25',
            '1eafde01ece74bfba10293cccc50f418',
            'http://localhost:8080/callback'
        )

        playlists = youtubeClient.get_playlists()

        for index, playlist in enumerate(playlists):
            print(f"{index}: {playlist.title}")

        choice = int(input("Enter your choice: "))
        chosen_playlist = playlists[choice]
        print(f"You selected: {chosen_playlist.id}, {chosen_playlist.title}")

        user_id = sportifyClient.get_current_user_info()
        playlist_id = sportifyClient.create_new_playlist(user_id, chosen_playlist.title)
        songs = youtubeClient.get_video_from_playlist(chosen_playlist.id)
        print(f"Attempting to add {len(songs)} songs")

        try:
            for song in songs:
                if song.artist and song.track:
                    try:
                        sportify_song_id = sportifyClient.search_song(song.artist, song.track)
                        if sportify_song_id:
                            sportifyClient.add_song_to_spotify_playlist(playlist_id, sportify_song_id)
                    except Exception as song_error:
                        print(f"Error processing song {song.artist} - {song.track}: {song_error}")
        except Exception as playlist_error:
            print(f"An error occurred while processing the playlist: {playlist_error}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    run()
