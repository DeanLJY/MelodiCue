<template>
  <v-container>
    <v-row>
      <v-col sm="4">
        <ListPlaylists />
      </v-col>
      <v-col sm="4">
        <TrackBuilder />
      </v-col>
      <v-col sm="4">
        <ListTracks />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ListPlaylists from "./ListPlaylists";
import TrackBuilder from "./TrackBuilder";
import ListTracks from "./ListTracks";

export default {
  name: "PlaylistCreator",

  components: {
    ListPlaylists,
    TrackBuilder,
    ListTracks,
  },

  data: () => ({}),
};
</script>
