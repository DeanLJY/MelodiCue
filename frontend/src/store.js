import Vue from "vue";
import Vuex from "vuex";
import SongService from "@/services/SongService";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    playlist_id: null,
    playlist_name: "My Playlist",
    tracks: [], // { track_name, artist_name, track_uri  }
  },
  mutations: {
    SET_PLAYLIST_ID(state, playlist_id) {
      state.playlist_id = playlist_id;
    },
    SET_PLAYLIST_NAME(state, playlist_name) {
      state.playlist_name = playlist_name;
    },
    ADD_TRACK(state, track) {
      console.log("ADD_TRACK track", track);
      state.tracks.push(track);
    },
  },
  getters: {
    trackUris: (state) => state.tracks.map((track) => track.track_uri),
  },
  actions: {
    createPlaylist({ commit, state }) {
      SongService.postCreatePlaylist(state.playlist_name)
        .then((res) => {
          console.log("createPlaylist", res.data);
          commit("SET_PLAYLIST_ID", res.data.playlist_id);
        })
        .catch((err) => console.log(err));
    },
    addTrack({ commit, state }, track_uri) {
      console.log("addTrack ACTION");
      console.log("state.playlist_id", state.playlist_id);
      console.log("track_uri", track_uri);
      SongService.postAddTrack(state.playlist_id, track_uri).then((res) => {
        commit("ADD_TRACK", {
          track_name: res.data.track_name,
          artist_name: res.data.artist_name,
          track_uri: res.data.track_uri,
        });
      });
    },
  },
});
