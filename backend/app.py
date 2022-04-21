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

# Automatically tear down SQLAlchemy.
"""
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
"""

# Login required decorator.
"""
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
"""
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/get-tracks")
def get_tracks():
    results = memgraph.execute_and_fetch(f"MATCH (n:Track) RETURN n;")
    tracks = [Track.create_from_data(result["n"]) for result in results]
    return jsonify(tracks)


@app.route("/get-top-tracks", defaults={"num_of_tracks": 10})
@app.route("/get-top-tracks/<int:num_of_tracks>")
def get_most_used_tracks(num_of_tracks):
    results = memgraph.execute_and_fetch(
        "MATCH (n:Track)<-[r]-(m) RETURN n, COUNT(m) AS edg_count ORDER BY edg_count"
        f" DESC LIMIT {num_of_tracks};"
    )

    tracks = [
        {"track": Track.create_from_data(result["n"]), "num_of_playlists": result["edg_count"]}
        for result in results
    ]
    return jsonify(tracks)


@app.route("/get-top-playlists", defaults={"num_of_playlists": 10})
@app.route("/get-top-playlists/<int:num_of_playlists>")
def get_playlists_with_most_tracks(num_of_playlists):
    results = memgraph.execute_and_fetch(
        "MATCH (n:Playlist)-[r]->(m) RETURN n, COUNT(m) AS edg_count ORDER BY"
        f" edg_count DESC LIMIT {num_of_playlists};"
    )
    tracks = [
        {"playlist": Playlist.create_from_data(result["n"]), "num_of_tracks": result["edg_count"]}
        for result in results
    ]
    return jsonify(tracks)


@app.route("/add-track", methods=["POST"])
def add_track():
    try:
        data = request.get_json()
        playlist_id = to_cypher_value(data["playlist_id"])
        artist_name = to_cypher_value(data["artist_name"])
        track_uri = to_cypher_value(data["track_uri"])
        artist_uri = to_cypher_value(data["artist_uri"])
        track_name = to_cypher_value(data["track_name"])
        album_uri = to_cypher_value(data["album_uri"])
        duration_ms = to_cypher_value(data["duration_ms"])
        album_name = to_cypher_value(data["album_name"])
        memgraph.execute(
            f"CREATE (:{Track.LABEL} {{artist_name: {artist_name}, track_uri:"
            f" {track_uri}, artist_uri: {artist_uri}, track_name: {track_name},"
            f" album_uri: {album_uri}, duration_ms: {duration_ms}, album_name:"
            f" {album_name} }})"
        )
        return jsonify({"error": True})
    except Exception as exp:
        return jsonify({"error": str(exp)})


@app.route("/create-playlist", methods=["POST"])
def add_playlist():
    try:
        data = request.get_json()
        name = to_cypher_value(data["name"])
        playlist = Playlist(name)
        result = memgraph.execute_and_fetch(f"CREATE (n:{Playlist.LABEL} {{{playlist.to_cypher()}}}) RETURN id(n) as playlist_id;")
        playlist_id = next(result)["playlist_id"]
        return jsonify({
            "playlist_id": playlist_id,
            "error": None
        })
    except Exception as exp:
        return jsonify({
            "error": exp
        })


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
