import json
import logging

import stomp
from api.settings import APP_SETTINGS
from api.user.databus.databus_connector import subscribe_to_databus
from api.user.user_info import add_user_action

logger = logging.getLogger(__name__)

LISTENER_CONNECTIONS = []


class ListenerError(Exception):
    pass


class UserActionsListener(stomp.ConnectionListener):
    """Listener handling user action messages coming from the databus"""

    def on_error(self, frame):
        raise ListenerError(f"User action listener error: {frame.body}")

    def on_message(self, frame):
        parsed_action = json.loads(json.loads(frame.body))
        logger.info(f"User action listener received: {parsed_action}")
        add_user_action(parsed_action)


def initialize_databus_listeners():
    # Subscribe to user actions
    LISTENER_CONNECTIONS.append(
        subscribe_to_databus(host=APP_SETTINGS['CREDENTIALS']['DATABUS']['HOST'],
                             port=APP_SETTINGS['CREDENTIALS']['DATABUS']['PORT'],
                             username=APP_SETTINGS['CREDENTIALS']['DATABUS']['LOGIN'],
                             password=APP_SETTINGS['CREDENTIALS']['DATABUS']['PASSWORD'],
                             listener=UserActionsListener(), subscription_id="user_action",
                             topic="/topic/user_actions")
    )

    logger.info(f"Successfully subscribed to {len(LISTENER_CONNECTIONS)} topics")


def shutdown_databus_listeners():
    for listener in LISTENER_CONNECTIONS:
        listener.disconnect()
