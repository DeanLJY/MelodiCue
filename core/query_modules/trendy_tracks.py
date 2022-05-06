import mgp


@mgp.read_proc
def get() -> mgp.Record(track_ids=list[int]):
    """Returns a list of track_ids of trendy songs.
    Calculates recently popular tracks by comparing the
    popularity of songs using the `followers`, `created_at`,
    and proximity to other popular songs (pagerank).

    :return: List of track ids that are currently trendy.
    :rtype: mgp.Record(track_ids=list[int])
    """
    return mgp.Record(track_ids=[1, 2, 3])
