from heapq import nlargest

import mgp


@mgp.read_proc
def get(context: mgp.ProcCtx, playlist: mgp.Vertex) -> mgp.Record(playlists=list):
    """Returns a list of playlist_ids that are similar to the given playlist.
    Calculates similar playlists by calculating the proximity of each to the
    given one.

    Example usage:
        MATCH (playlist:Playlist)
        WITH playlist
        LIMIT 1
        CALL similar_playlists.get(playlist) YIELD playlists
        RETURN playlists

    :param int playlist_id: User playlist.
    :return: List of playlist.
    :rtype: mgp.Record(playlist_ids=list[dict[str][Any]])
    """
    tracks = set(map(lambda edge: edge.to_vertex.id, playlist.out_edges))
    return mgp.Record(
        playlists=list(
            map(
                lambda vertex: dict(vertex.properties),
                nlargest(
                    10,
                    filter(
                        lambda vertex: "Playlist" in vertex.labels,
                        context.graph.vertices,
                    ),
                    key=lambda vertex: len(
                        tracks
                        & set(map(lambda edge: edge.to_vertex.id, vertex.out_edges))
                    ),
                ),
            )
        )
    )
