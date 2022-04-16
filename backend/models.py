from dataclasses import dataclass

@dataclass
class Track:
    artist_name: str
    track_uri: str
    artist_uri: str
    track_name: str
    album_uri: str
    duration_ms: int
    album_name: str

    def __init__(self, data):
        self.artist_name = data.properties["artist_name"]
        self.track_uri = data.properties["track_uri"]
        self.artist_uri = data.properties["artist_uri"]
        self.track_name = data.properties["track_name"]
        self.album_uri = data.properties["album_uri"]
        self.duration_ms = data.properties["duration_ms"]
        self.album_name = data.properties["album_name"]

@dataclass
class Playlist:
    name: str
    collaborative: str
    pid: str
    modified_at: str
    num_albums: str
    num_tracks: str
    num_followers: str
    num_edits: str
    duration_ms: str
    num_artists: str

    def __init__(self, data):
        self.name = data.properties["name"]
        self.collaborative = data.properties["collaborative"]
        self.pid = data.properties["pid"]
        self.modified_at = data.properties["modified_at"]
        self.num_albums = data.properties["num_albums"]
        self.num_tracks = data.properties["num_tracks"]
        self.num_followers = data.properties["num_followers"]
        self.num_edits = data.properties["num_edits"]
        self.duration_ms = data.properties["duration_ms"]
        self.num_artists = data.properties["num_artists"]
