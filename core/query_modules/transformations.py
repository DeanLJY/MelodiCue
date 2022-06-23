import mgp
import json
import sys


@mgp.transformation
def spotify(
    messages: mgp.Messages,
) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        try:
            message = messages.message_at(i)
            payload_as_str = message.payload().decode("utf-8").replace("'", '"')
            data = json.loads(payload_as_str)
            playlist_id = data["pid"]
            result_queries.append(
                mgp.Record(
                    query="CREATE (:Playlist {name: $name, collaborative: $collaborative,pid: $pid,modified_at: $modified_at,num_albums: $num_albums,num_tracks: $num_tracks,num_followers: $num_followers,num_edits: $num_edits,duration_ms: $duration_ms,num_artists: $num_artists});",
                    parameters={
                        "name": data["name"],
                        "collaborative": data["collaborative"],
                        "pid": playlist_id,
                        "modified_at": data["modified_at"],
                        "num_albums": data["num_albums"],
                        "num_tracks": data["num_tracks"],
                        "num_followers": data["num_followers"],
                        "num_edits": data["num_edits"],
                        "duration_ms": data["duration_ms"],
                        "num_artists": data["num_artists"],
                    },
                )
            )
        except json.JSONDecodeError as exp:
            print(f"JSON error: {exp} with {payload_as_str}", file=sys.stderr)
            return []

        for track in data["tracks"]:
            try:
                result_queries.append(
                    mgp.Record(
                        query="MATCH (playlist {pid: $pid}) MERGE (track:Track {artist_name: $artist_name, track_uri: $track_uri, artist_uri: $artist_uri, track_name: $track_name, album_uri: $album_uri, duration_ms: $duration_ms, album_name: $album_name}) CREATE (playlist)-[:HAS]->(track);",
                        parameters={
                            "pid": playlist_id,
                            "artist_name": track["artist_name"],
                            "track_uri": track["track_uri"],
                            "artist_uri": track["artist_uri"],
                            "track_name": track["track_name"],
                            "album_uri": track["album_uri"],
                            "duration_ms": track["duration_ms"],
                            "album_name": track["album_name"],
                        },
                    )
                )
            except json.JSONDecodeError as exp:
                print(f"JSON error: {exp} with {payload_as_str}", file=sys.stderr)
                continue
    return result_queries
