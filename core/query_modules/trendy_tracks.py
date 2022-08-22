from heapq import nlargest

import mgp


@mgp.read_proc
def get(context: mgp.ProcCtx) -> mgp.Record(tracks=list):
    """Returns a list of track_ids of trendy songs.
    Calculates recently popular tracks by comparing the
    popularity of songs using the `followers`, `created_at`,
    and proximity to other popular songs (pagerank).

    Example usage:
        CALL trendy_tracks.get() YIELD tracks

    Equivalent cypher query:
        MATCH (track:Track)<--(playlist:Playlist)
        WITH track, count(playlist) AS popularity
        RETURN track
        ORDER BY popularity DESC
        LIMIT 10

    :return: List of track ids that are currently trendy.
    :rtype: mgp.Record(tracks=list[dict[str][Any]])
    """
    return mgp.Record(
        tracks=list(
            map(
                lambda vertex: dict(vertex.properties),
                nlargest(
                    10,
                    filter(
                        lambda vertex: "Track" in vertex.labels,
                        context.graph.vertices,
                    ),
                    key=lambda vertex: sum(1 for _ in vertex.in_edges),
                ),
            )
        )
    )
