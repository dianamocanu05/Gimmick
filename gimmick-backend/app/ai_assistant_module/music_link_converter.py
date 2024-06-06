import spotipy
from googleapiclient.discovery import build
from spotipy import SpotifyClientCredentials
from yt_dlp import YoutubeDL

from app.ai_assistant_module.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, YOUTUBE_API_KEY


class SpotifyService:
    def __init__(self):
        self.auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_song_by_link(self, spotify_link):
        track_id = spotify_link.split('/')[-1].split('?')[0]
        track = self.sp.track(track_id)
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        song_name = track['name']

        song = Song(song_name, artist_name)
        song.album = album_name
        song.spotify_link = spotify_link
        return song

    def get_link_by_song(self, song):
        searchQuery = song.title + ' ' + song.artist + ' ' + song.album
        searchResults = self.sp.search(q=searchQuery, type="track")
        return searchResults['tracks']['items'][0]['external_urls']['spotify']


class YoutubeService:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    def get_song_by_link(self, youtube_link):
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(youtube_link, download=False)
            title = info_dict.get('title', None)
            artist = info_dict.get('artist', None)
            album = info_dict.get('album', None)
            song = Song(title, artist)
            if album is not None:
                song.album = album
            return song

    def get_link_by_song(self, song):
        query = f"{song.title} {song.artist}"
        request = self.youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=1
        )
        response = request.execute()
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        return None


class Song:

    def __init__(self, title, artist):
        self.title = title
        if artist is not None:
            self.artist = artist
        else:
            self.artist = ""
        self.album = ""
        self.youtube_link = None
        self.spotify_link = None
        self.added_by_user = None
        self.added_timestamp = None

    def to_string(self):
        print(self.title + " - " + self.artist + " (" + self.album + ")")


def convert(link):
    if 'spotify' in link:
        song = SpotifyService().get_song_by_link(link)
        song.spotify_link = link
        youtube_link = YoutubeService().get_link_by_song(song)
        song.youtube_link = youtube_link
        return youtube_link, song
    elif 'youtube' in link:
        song = YoutubeService().get_song_by_link(link)
        song.youtube_link = link
        spotify_link = SpotifyService().get_link_by_song(song)
        song.spotify_link = spotify_link
        return spotify_link, song
    else:
        return None, None


if __name__ == "__main__":
    converted_link, _ = convert('https://open.spotify.com/track/0hWCzWl04zT7P6vMy63XCN?si=344687514d914991')
    print(converted_link)
