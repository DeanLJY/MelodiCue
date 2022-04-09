"""Sends playlists to kafka.

Usage:
    python3 producer.py path/to/data
"""
import os
import sys
import json
import time

import kafka


producer = kafka.KafkaProducer(
    bootstrap_servers=["ec2-34-245-33-31.eu-west-1.compute.amazonaws.com:9092"]
)


def process_mpd(path):
    count = 0
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            with open(fullpath) as f:
                js = f.read()

            mpd_slice = json.loads(js)
            for playlist in mpd_slice["playlists"]:
                process_playlist(playlist)
            count += 1
            print(count)


def process_playlist(playlist):
    producer.send("spotify", json.dumps(playlist).encode("utf-8"))
    producer.flush()
    time.sleep(1)


if __name__ == "__main__":
    path = sys.argv[1]
    process_mpd(path)
