# 🎵 MelodiCue: Curating Your Unique Sonic Journey 🎧

> "Crafting your musical soulmate with MelodiCue's personalized suggestions."

MelodiCue is an innovative music discovery application that enables users to effortlessly generate personalized playlists. By utilizing sophisticated algorithms and an extensive database of songs, MelodiCue offers a unique listening experience tailored to your individual taste.

## 📚 Table of Contents

- [About](#about)
- [Features](#features)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)

## 🚀 About

Amidst the ever-expanding universe of music, keeping up with new releases and finding undiscovered treasures can be challenging. MelodiCue aims to bridge this gap by providing a personalized music discovery experience. By analyzing your listening habits and preferences, MelodiCue curates bespoke playlists filled with tracks you'll love, ensuring your musical journey keeps evolving.

## ✨ Features

- **Personalized Suggestions**: MelodiCue's powerful algorithms analyze your music taste to propose new tracks and artists you're likely to enjoy.
- **Playlist Generation**: Effortlessly create and curate playlists based on your mood, genre preferences, or specific artists.
- **Trend Discovery**: Discover the latest music trends and popular tracks across various genres.
- **Seamless Experience**: Enjoy MelodiCue on different devices and platforms for a seamless listening experience.

## 📂 Dataset

MelodiCue harnesses the [Spotify Million Playlist Dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge), a comprehensive compilation of 5 million playlists from Spotify users. This dataset provides an invaluable source of information for refining our suggestion algorithms.<details>  <summary>Dataset Sample</summary>```json
{
    "name": "musical",
    "collaborative": "false",
    "pid": 5,
    "modified_at": 1493424000,
    "num_albums": 7,
    "num_tracks": 12,
    "num_followers": 1,
    "num_edits": 2,
    "duration_ms": 2657366,
    "num_artists": 6,
    "tracks": [
        {
            "pos": 0,
            "artist_name": "Degiheugi",
            "track_uri": "spotify:track:7vqa3sDmtEaVJ2gcvxtRID",
            "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
            "track_name": "Finalement",
            "album_uri": "spotify:album:2KrRMJ9z7Xjoz1Az4O6UML",
            "duration_ms": 166264,
            "album_name": "Dancing Chords and Fireflies"
        },
        // 10 tracks omitted
        {
            "pos": 11,
            "artist_name": "Mo' Horizons",
            "track_uri": "spotify:track:7iwx00eBzeSSSy6xfESyWN",
            "artist_uri": "spotify:artist:3tuX54dqgS8LsGUvNzgrpP",
            "track_name": "Fever 99\u00b0",
            "album_uri": "spotify:album:2Fg1t2tyOSGWkVYHlFfXVf",
            "duration_ms": 364320,
            "album_name": "Come Touch The Sun"
        }
    ]
}```

</details>

## 🚀 Getting Started

1. Install [Docker](https://www.docker.com/get-started) on your system.
2. Clone the MelodiCue repository or download the source code.

```bash
git clone https://github.com/DeanLJY/MelodiCue.git
```

3. Download the complete [Spotify Dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge#dataset) and replace the `.json` files in the directory `/producer/data`.

## ❓ Usage

1. Build and run the application using Docker:

```bash
docker-compose build
docker-compose up
```

2. Access MelodiCue through your web browser at [localhost:80](http://localhost:80).
