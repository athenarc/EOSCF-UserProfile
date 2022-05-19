import logging

import stomp

logger = logging.getLogger(__name__)


def default_subscription_condition(connection: stomp.Connection) -> bool:
    """Default condition, it can be overwritten in `subscribe_to_databus`"""
    return connection.is_connected()


def subscribe_to_databus(
    host: str,
    port: int,
    username: str,
    password: str,
    topic: str,
    subscription_id: str,
    listener: stomp.ConnectionListener,
    ssl: bool = True,
) -> stomp.Connection:
    """
    Subscribe to the databus and block until kill signal is issued
    """
    connection = stomp.Connection([(host, port)])
    connection.set_listener("", listener)

    try:
        connection.connect(username=username, password=password, wait=True, ssl=ssl)
        connection.subscribe(destination=topic, id=subscription_id, ack="auto")
        logger.info(f"Subscribed to {topic} on {host}:{port}")

    except KeyboardInterrupt:
        connection.disconnect()

    return connection
