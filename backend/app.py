# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from gqlalchemy import Memgraph
from models import Track, Playlist, to_cypher_value

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object("config")
memgraph = Memgraph()


class Status:
    SUCCESS = "success"
    FAILURE = "failure"


@app.route("/get-tracks")
def get_tracks():
    try:
        results = memgraph.execute_and_fetch(f"MATCH (n:Track) RETURN n;")
        tracks = [Track.create_from_data(result["n"]) for result in results]
        return jsonify({"tracks": tracks, "status": Status.SUCCESS, "message": ""})
    except Exception as exp:
        return jsonify({
            "status": Status.FAILURE,
            "message": exp
        })


@app.route("/top-tracks", defaults={"num_of_tracks": 10})
@app.route("/top-tracks/<int:num_of_tracks>")
def get_top_tracks(num_of_tracks):
    try:
        results = memgraph.execute_and_fetch(
            "MATCH (n:Track)<-[r]-(m) RETURN n, COUNT(m) AS edg_count ORDER BY edg_count"
            f" DESC LIMIT {num_of_tracks};"
        )

        tracks = [
            {
                "track": Track.create_from_data(result["n"]),
                "num_of_playlists": result["edg_count"],
            }
            for result in results
        ]
        return jsonify({"tracks": tracks, "status": Status.SUCCESS, "message": ""})
    except Exception as exp:
        return jsonify({
            "status": Status.FAILURE,
            "message": exp
        })


@app.route("/top-playlists", defaults={"num_of_playlists": 10})
@app.route("/top-playlists/<int:num_of_playlists>")
def get_playlists_with_most_tracks(num_of_playlists):
    try:
        results = memgraph.execute_and_fetch(
            "MATCH (n:Playlist)-[r]->(m) RETURN n, COUNT(m) AS edg_count ORDER BY"
            f" edg_count DESC LIMIT {num_of_playlists};"
        )
        playlists = [
            {
                "playlist": Playlist.create_from_data(result["n"]),
                "num_of_tracks": result["edg_count"],
            }
            for result in results
        ]
        return jsonify({"playlists": playlists, "status": Status.SUCCESS, "message": ""})
    except Exception as exp:
        return jsonify({
            "status": Status.FAILURE,
            "message": exp
        })



@app.route("/add-track", methods=["POST"])
def add_track():
    try:
        data = request.get_json()
        playlist_id = data["playlist_id"]
        track_id = data["track_id"]

        playlist_result = next(
            memgraph.execute_and_fetch(f"MATCH (n) WHERE ID(n) = {playlist_id} RETURN n;"),
            None,
        )
        track_result = next(
            memgraph.execute_and_fetch(f"MATCH (n) WHERE ID(n) = {track_id} RETURN n;"),
            None,
        )

        playlist = (
            Playlist.create_from_data(playlist_result["n"]) if playlist_result else None
        )
        track = Track.create_from_data(track_result["n"]) if track_result else None
        if not playlist:
            return jsonify({"error": True, "message": "Playlist does not exist!"})
        if not track:
            return jsonify({"error": True, "message": "Track does not exist!"})
        playlist.num_tracks += 1
        playlist.num_edits += 1
        playlist.duration_ms += track.duration_ms
        # Find out if playlist contains any track with existing album

        same_album_num = next(
            memgraph.execute_and_fetch(
                f"MATCH (n:Playlist)-[r]->(m) WHERE id(n) = {playlist_id} and m.album_name"
                f" = {to_cypher_value(track.album_name)} RETURN count(m) as counts;"
            ),
            0,
        )

        if same_album_num == 0:
            playlist.num_albums += 1
        # Find out if playlist contains any track with existing artist
        same_artist_num = next(
            memgraph.execute_and_fetch(
                f"MATCH (n:Playlist)-[r]->(m) WHERE id(n) = {playlist_id} and m.artist_name"
                f" = {to_cypher_value(track.artist_name)} RETURN count(m) as counts;"
            ),
            0,
        )
        if same_artist_num == 0:
            playlist.num_artists += 1
        memgraph.execute(
            f"MATCH (n), (m) WHERE id(n) = {playlist_id} AND id(m) = {track_id} CREATE"
            f" (n)-[:HAS]->(m) SET n = {to_cypher_value(playlist.to_map())};"
        )
        return jsonify({"status": Status.SUCCESS, "message": "Track added successfully!"})
    except Exception as exp:
        return jsonify({"status": Status.FAILURE, "message": Status.FAILURE})


@app.route("/create-playlist", methods=["POST"])
def create_playlist():
    try:
        data = request.get_json()
        name = to_cypher_value(data["name"])
        playlist = Playlist(name)
        result = memgraph.execute_and_fetch(
            f"CREATE (n:{Playlist.LABEL} {{{playlist.to_cypher()}}}) RETURN id(n) as"
            " playlist_id;"
        )
        playlist_id = next(result)["playlist_id"]
        return jsonify(
            {
                "playlist_id": playlist_id,
                "status": Status.SUCCESS,
                "message": "Created successfully!",
            }
        )
    except Exception as exp:
        return jsonify({"status": Status.FAILURE, "message": str(exp)})


@app.route("/")
def home():
    return render_template("pages/placeholder.home.html")


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template("errors/500.html"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
