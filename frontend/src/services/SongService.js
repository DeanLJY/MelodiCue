import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:5000",
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export default {
  postCreatePlaylist: (playlist_name) =>
    apiClient.post("/create-playlist", { playlist_name }),
  putRenamePlaylist: (id, name) =>
    apiClient.put("/rename-playlist", {
      playlist_id: id,
      playlist_name: name,
    }),
  postAddTrack: (playlist_id, track_uri) =>
    apiClient.post("/add-track", {
      playlist_id,
      track_uri,
    }),
  postTrackRecommendation: (id, trackIds) =>
    apiClient.post("/track-recommendation", {
      playlist_id: id,
      track_ids: trackIds,
    }),
  postPlaylistRecommendation: (id, trackIds) =>
    apiClient.post("/playlist-recommendation", {
      playlist_id: id,
      track_ids: trackIds,
    }),
  getTrendingTracks: () => apiClient.get("/trending-tracks"),
  getTopPlaylists: () => apiClient.get("/top-playlists"),
  getTopTracks: () => apiClient.get("/top-tracks"),
};
