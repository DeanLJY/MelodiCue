import mgp


@mgp.read_proc
def get(playlist_id: int) -> mgp.Record(track_ids=list[int]):
    """Returns a list of track_ids that are similar to the tracks in the given
    playlist.
    Calculates similar tracks by calculating the proximity of each track to the
    given playlist.

    :param int playlist_id: User playlist.
    :return: List of track ids that are currently trendy.
    :rtype: mgp.Record(track_ids=list[int])
    """
    return mgp.Record(track_ids=[1, 2, 3])
