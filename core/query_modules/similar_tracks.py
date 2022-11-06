from collections import OrderedDict
from typing import Dict, List

import mgp


def grade_playlist(relevant_playlist: mgp.Vertex, relevant_tracks: List[int]) -> int:
    relevant_playlist_tracks = [
        out_edge.to_vertex.id for out_edge in relevant_playlist.out_edges
    ]
    return len(list(set(relevant_playlist_tracks).intersection(relevant_tracks)))


def grade_track(relevant_track: mgp.Vertex, graded_playlists: Dict[int, int]) -> int:
    return sum(
        graded_playlists.get(in_edge.from_vertex.id, 0)
        for in_edge in relevant_track.in_edges
    )


@mgp.read_proc
def get_better(
    context: mgp.ProcCtx,
    playlist_id: int,
    tracks: mgp.List[mgp.Vertex],
) -> mgp.Record(result=mgp.Vertex, score=int):
    """Returns a list of track_ids that are similar to the tracks in
    the given playlist. Calculates similar tracks by calculating the
    proximity of each track to the given playlist.

    Cypher usage:

    MATCH (n:Playlist {pid: $playlist_id})-[]->(m:Track)
    WITH COLLECT(m) AS tracks
    CALL similar_tracks.get_better($playlist_id, tracks)
    YIELD result, score RETURN result, score ORDER BY score DESC LIMIT 10;
    """
    track_ids = [track.id for track in tracks]
    relevant_playlists = set()
    for track in tracks:
        for in_edge in track.in_edges:
            if in_edge.from_vertex.id != playlist_id:
                relevant_playlists.add(in_edge.from_vertex)

    relevant_tracks = set()
    for relevant_playlist in relevant_playlists:
        for out_edge in relevant_playlist.out_edges:
            if out_edge.to_vertex.id not in track_ids:
                relevant_tracks.add(out_edge.to_vertex)

    # 1. Grade playlists according to how many relevant_tracks they have
    graded_playlists = dict()
    for relevant_playlist in relevant_playlists:
        graded_playlists[relevant_playlist.id] = grade_playlist(
            relevant_playlist, track_ids
        )

    # 2. Grade all tracks according to in how similar playlist they are
    recommended_tracks = dict()
    for relevant_track in relevant_tracks:
        recommended_tracks[
            grade_track(relevant_track, graded_playlists)
        ] = relevant_track
    sorted_recommended_tracks = OrderedDict(
        sorted(recommended_tracks.items(), reverse=True)
    )

    scored_recommended_tracks = []
    for score, recommended_track in sorted_recommended_tracks.items():
        scored_recommended_tracks.append(
            mgp.Record(result=recommended_track, score=score)
        )
    return scored_recommended_tracks
