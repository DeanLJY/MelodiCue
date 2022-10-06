<template>
  <v-card class="mx-auto">
    <v-toolbar color="secondary" dark>
      <v-toolbar-title>Suggested Tracks</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-playlist-plus</v-icon>
      </v-btn>
    </v-toolbar>

    <v-list two-line>
      <v-list-item-group
        v-model="selected"
        v-on:change="trackSelected"
        active-class="pink--text"
        multiple
      >
        <template v-for="(track, index) in topTracks">
          <v-list-item :key="track.track_uri">
            <template v-slot:default="{ active }">
              <v-list-item-content>
                <v-list-item-title
                  v-text="track.track_name"
                ></v-list-item-title>

                <v-list-item-subtitle
                  v-text="track.artist_name"
                ></v-list-item-subtitle>
              </v-list-item-content>

              <v-list-item-action>
                <v-list-item-action-text
                  v-text="track.action"
                ></v-list-item-action-text>

                <v-icon v-if="!active" color="grey lighten-1">
                  mdi-star-outline
                </v-icon>

                <v-icon v-else color="yellow darken-3"> mdi-star </v-icon>
              </v-list-item-action>
            </template>
          </v-list-item>

          <v-divider
            v-if="index < topTracks.length - 1"
            :key="index"
          ></v-divider>
        </template>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
import SongService from "@/services/SongService.js";
import { mapState, mapActions, mapGetters } from "vuex";


export default {
  name: "ListTracks",

  created() {
    SongService.getTopTracks()
    /* SongService.postTrackRecommendation(1557, ["spotify:track:6AAZigYqOch79lKcrSBOv0", "spotify:track:7s0lDK7y3XLmI7tcsRAbW0"]) */
      .then((res) => {
        this.topTracks = res.data.tracks.map((e) => e.track);
        console.log(res.data);
        console.log(this.topTracks);
      })
      .catch((err) => {
        console.log(err);
      });
  },

  computed: {
    ...mapGetters(["trackUris"]),
    ...mapState({
      playlistName: "playlist_name",
      tracks: "tracks",
    }),
  },

  methods: {
    trackSelected() {
      let self = this;
      console.log(this.selected);

      this.selected.forEach((index) => {
        console.log(index);
        let track_uri = self.topTracks[index];
        self.addTrack(track_uri);
      });

      this.selected = [];
    },
    ...mapActions(["addTrack"]),
  },

  data: () => ({
    selected: [],
    topTracks: [],
  }),
};
</script>
