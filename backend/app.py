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
from models import Track, Playlist

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


def create_playlist(form_data):
    Memgraph.execute(f"CREATE (:TRACK {{artist_name: {form_data['ladida']}}})")


@app.route("/get-tracks")
def get_tracks():
    results = memgraph.execute_and_fetch(f"MATCH (n:Track) RETURN n;")
    tracks = [Track(result["n"]) for result in results]
    return jsonify(tracks)


@app.route("/get-top-tracks", defaults={"num_of_tracks": 10})
@app.route("/get-top-tracks/<int:num_of_tracks>")
def get_most_used_tracks(num_of_tracks):
    results = memgraph.execute_and_fetch(
        f"MATCH (n:Track)<-[r]-(m) RETURN n, COUNT(m) AS edg_count ORDER BY edg_count DESC LIMIT {num_of_tracks};"
    )

    tracks = [
        {"track": Track(result["n"]), "num_of_playlists": result["edg_count"]}
        for result in results
    ]
    return jsonify(tracks)


@app.route("/get-top-playlists", defaults={"num_of_playlists": 10})
@app.route("/get-top-playlists/<int:num_of_playlists>")
def get_playlists_with_most_tracks(num_of_playlists):
    results = memgraph.execute_and_fetch(
        f"MATCH (n:Playlist)-[r]->(m) RETURN n, COUNT(m) AS edg_count ORDER BY edg_count DESC LIMIT {num_of_playlists};"
    )
    tracks = [
        {"playlist": Playlist(result["n"]), "num_of_tracks": result["edg_count"]}
        for result in results
    ]
    return jsonify(tracks)


@app.route("/add-song", methods=["GET", "POST"])
def add_playlist():
    # "artist_name": "Degiheugi",
    # "track_uri": "spotify:track:7vqa3sDmtEaVJ2gcvxtRID",
    # "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
    # "track_name": "Finalement",
    # "album_uri": "spotify:album:2KrRMJ9z7Xjoz1Az4O6UML",
    # "duration_ms": 166264,
    # "album_name": "Dancing Chords and Fireflies"
    if request.method == "POST":
        create_track(request.form)
    else:
        return show_the_login_form()


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
