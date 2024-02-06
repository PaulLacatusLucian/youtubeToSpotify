import logging
import os
import google_auth_oauthlib
import googleapiclient.discovery

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title

class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track.split('-')[1].lstrip()

class YouTubeClient(object):
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)

        credentials = flow.run_local_server(port=8080)
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube

    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()

        playlists = [Playlist(playlist['id'], playlist['snippet']['title']) for playlist in response['items']]
        return playlists

    def get_video_from_playlist(self, playlist_id):
        songs = []

        try:
            nextPageToken = None
            while True:
                request = self.youtube_client.playlistItems().list(
                    playlistId=playlist_id,
                    part="snippet",
                    maxResults=500,
                    pageToken=nextPageToken
                )
                response = request.execute()

                for item in response.get('items', []):
                    try:
                        video_id = item['snippet']['resourceId']['videoId']
                        artist, track = self.get_artist_and_track_from_video(video_id)
                        if artist and track:
                            songs.append(Song(artist, track))
                    except KeyError as e:
                        logging.error(f"Key error while processing video item: {e}")
                    except Exception as e:
                        logging.error(f"Error processing item: {item}. Error: {e}")

                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    break

        except Exception as e:
            logging.error(f"Error fetching videos from playlist {playlist_id}: {e}")
            pass

        return songs

    def get_artist_and_track_from_video(self, video_id):
        try:
            request = self.youtube_client.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()

            items = response.get('items', [])
            if items:
                snippet = items[0]['snippet']
                artist = snippet.get('channelTitle')
                track = snippet.get('title')
            else:
                artist, track = None, None

        except Exception as e:
            logging.error(f"Error fetching video info for {video_id}: {e}")
            artist, track = None, None

        return artist, track
