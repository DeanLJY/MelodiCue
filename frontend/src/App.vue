<template>
  <v-app>
    <v-app-bar app color="secondary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="@/assets/logo.svg"
          transition="scale-transition"
          width="40"
        />

        <h1>Spotifake</h1>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge"
        target="_blank"
        text
      >
        <span class="mr-2">Dataset</span>
        <v-icon>mdi-database</v-icon>
      </v-btn>
      <v-btn
        href="https://github.com/falloutone/melodicue"
        target="_blank"
        text
      >
        <span class="mr-2">Fork me</span>
        <v-icon>mdi-github</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <PlaylistCreator />
    </v-main>
  </v-app>
</template>

<script>
import PlaylistCreator from "./components/PlaylistCreator";

export default {
  name: "App",

  components: {
    PlaylistCreator,
  },

  data: () => ({
    //
  }),
};
</script>
