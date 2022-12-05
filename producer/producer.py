"""Sends playlists to kafka.

Usage:
    python3 producer.py path/to/data
"""
import json
import os
import time
from functools import wraps

import kafka


def process_mpd(path, producer):
    count = 0
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            with open(fullpath) as f:
                js = f.read()

            mpd_slice = json.loads(js)
            for playlist in mpd_slice["playlists"]:
                process_playlist(playlist, producer)
            count += 1
            print(count)


def process_playlist(playlist, producer):
    producer.send("spotify", json.dumps(playlist).encode("utf-8"))
    print(playlist)
    producer.flush()
    time.sleep(1)


def main():
    # Wait for kafka to set up
    time.sleep(10)
    producer = kafka.KafkaProducer(bootstrap_servers=["kafka:9092"])
    process_mpd("data", producer)


if __name__ == "__main__":
    main()
