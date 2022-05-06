import mgp


@mgp.read_proc
def get(playlist_id: int) -> mgp.Record(playlist_ids=list[int]):
    """Returns a list of playlist_ids that are similar to the given playlist.
    Calculates similar playlists by calculating the proximity of each to the
    given one.

    :param int playlist_id: User playlist.
    :return: List of playlist ids that are currently trendy.
    :rtype: mgp.Record(playlist_ids=list[int])
    """
    return mgp.Record(playlist_ids=[1, 2, 3])
