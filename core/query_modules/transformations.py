import mgp


@mgp.transformation
def transform_test(
    messages: mgp.Messages,
) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        payload_as_str = message.payload().decode("utf-8")
        result_queries.append(
            mgp.Record(
                query="CREATE (Test {timestamp: $timestamp, payload: $payload, topic: $topic})",
                parameters={
                    "timestamp": message.timestamp(),
                    "payload": payload_as_str,
                    "topic": message.topic_name(),
                },
            )
        )

    return result_queries
