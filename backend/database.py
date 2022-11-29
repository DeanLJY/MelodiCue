from gqlalchemy import Memgraph
from time import sleep

memgraph = Memgraph("memgraph", 7687)


class KafkaStreamConfig:
    TOPIC_NAME = "spotify"
    STREAM_NAME = "spotify"


def _wait_for_memgraph():
    for i in range(3):
        try:
            memgraph.execute_and_fetch("MATCH (n) RETURN n LIMIT 1")
            return
        except Exception as exp:
            sleep(2)
            print(exp)
    raise Exception("Could not connect to memgraph!")


def setup_memgraph():
    _wait_for_memgraph()
    memgraph.ensure_indexes([])
    memgraph.ensure_constraints([])

    streams = [
        stream_row["name"] for stream_row in memgraph.execute_and_fetch("SHOW STREAMS;")
    ]
    # Wait for kafka to set up
    sleep(5)
    if KafkaStreamConfig.STREAM_NAME not in streams:
        memgraph.execute(
            f"CREATE KAFKA STREAM {KafkaStreamConfig.STREAM_NAME} TOPICS {KafkaStreamConfig.TOPIC_NAME} TRANSFORM transformations.spotify BOOTSTRAP_SERVERS 'kafka:9092';"
        )
        memgraph.execute(f"START STREAM {KafkaStreamConfig.STREAM_NAME}")
    else:
        print("Stream already running!")
