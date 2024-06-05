import spotipy
from spotipy import SpotifyClientCredentials

from app.ai_assistant_module.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

class SpotifyService: pass
class YoutubeService: pass
class Song:

    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album
        self.youtube_link = None
        self.spotify_link = None
        self.added_by_user = None
        self.added_timestamp = None



class MusicLinkConverter:

    def __init__(self):
        self.song = None

    def find_song(self, link):
        if 'spotify' in link:
            self.song = SpotifyToYoutubeConverter().get_song_by_link(link)
        elif 'youtube' in link:
            #self.song = YoutubeToSpotifyConverter().get_song_by_link(link)
            pass

class SpotifyToYoutubeConverter():
    def __init__(self):
        self.auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_song_by_link(self, spotify_link):
        track_id = spotify_link.split('/')[-1].split('?')[0]
        track = self.sp.track(track_id)
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        song_name = track['name']

        song = Song(song_name, artist_name, album_name)
        song.spotify_link = spotify_link
        return song




if __name__ == "__main__":
    msl = MusicLinkConverter()
    msl.convert('https://open.spotify.com/track/4ipzXe2jmoeN7zm2VMb4eX?si=834133550b8b4b7c')

#https://open.spotify.com/album/5OZ44LaqZbpP3m9B3oT8br?si=sa66CyVGRW2QNHLYWb0oXg