<template>
  <v-card class="mx-auto">
    <v-toolbar color="primary" dark>
      <v-toolbar-title>{{ playlistName }}</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-playlist-edit</v-icon>
      </v-btn>
    </v-toolbar>

    <v-list two-line>
      <v-list-item-group>
        <template v-for="(track, index) in tracks">
          <v-list-item :key="track.track_name">
            <template>
              <v-list-item-content>
                <v-list-item-title
                  v-text="track.track_name"
                ></v-list-item-title>

                <v-list-item-subtitle
                  v-text="track.artist_name"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </template>
          </v-list-item>

          <v-divider v-if="index < tracks.length - 1" :key="index"></v-divider>
        </template>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "TrackBuilder",

  created() {
    this.createPlaylist();
  },

  methods: {
    ...mapActions(["createPlaylist"]),
  },

  computed: {
    ...mapState({
      playlistName: "playlist_name",
      tracks: "tracks",
    }),
  },

  data: () => ({}),
};
</script>
