<template>
  <v-card class="mx-auto">
    <v-toolbar color="secondary" dark>
      <v-toolbar-title>Suggested Playlists</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-playlist-music</v-icon>
      </v-btn>
    </v-toolbar>

    <v-list>
      <v-list-group
        v-for="playlist in playlists"
        :key="playlist.playlist_id"
        v-model="playlist.active"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-icon>
            <v-icon>mdi-playlist-music</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title
              v-text="playlist.name"
            ></v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item v-for="track in playlist.tracks" :key="track.track_uri">
          <v-list-item-content>
            <v-list-item-title v-text="track.track_name"></v-list-item-title>
            <v-list-item-subtitle
              v-text="track.artist_name"
            ></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-card>
</template>

<script>
import SongService from "@/services/SongService.js";
import { mapState } from "vuex";

export default {
  name: "ListPlaylists",

  created() {
    /* SongService.getTopPlaylists() */
    SongService.postPlaylistRecommendation(1557, this.tracks)

      .then((res) => {
        console.log("suggested playlist");
        console.log(res.data.playlists);
        this.playlists = res.data.playlists.map((e) => e.playlist);
      })
      .catch((err) => {
        console.log(err);
      });
  },

  computed: {
    ...mapState({
      playlistName: "playlist_name",
      tracks: "tracks",
    }),
  },

  data: () => ({
    playlists: []
  }),
};
</script>
