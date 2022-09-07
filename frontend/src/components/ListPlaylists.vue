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
              v-text="playlist.playlist_name"
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
export default {
  name: "ListPlaylists",

  data: () => ({
    playlists: [
      {
        active: false,
        icon: "mdi-playlist-music",
        playlist_id: 1,
        playlist_name: "First",
        tracks: [
          {
            track_uri: "1",
            track_name: "First - Track 1",
            artist_name: "First Artist",
          },
          {
            track_uri: "2",
            track_name: "First - Track 2",
            artist_name: "First Artist",
          },
          {
            track_uri: "3",
            track_name: "First - Track 3",
            artist_name: "First Artist",
          },
        ],
      },
      {
        active: false,
        icon: "mdi-playlist-music",
        playlist_id: 2,
        playlist_name: "Second",
        tracks: [
          {
            track_uri: "1",
            track_name: "Second - Track 1",
            artist_name: "Second Artist",
          },
          {
            track_uri: "2",
            track_name: "Second - Track 2",
            artist_name: "Second Artist",
          },
          {
            track_uri: "3",
            track_name: "Second - Track 3",
            artist_name: "Second Artist",
          },
        ],
      },
    ],
  }),
};
</script>
