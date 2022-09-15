import json
import logging

import stomp
from api.settings import APP_SETTINGS
from api.user.crud.projects import add_project, delete_project
from api.user.crud.user_action import add_user_action
from api.user.crud.user_info import update_user_information
from api.user.databus.databus_connector import subscribe_to_databus

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


class MpDbEventListener(stomp.ConnectionListener):
    """Listener handling user action messages coming from the databus"""

    def on_error(self, frame):
        raise ListenerError(f"Mp DB event listener error: {frame.body}")

    def on_message(self, frame):
        parsed_event = json.loads(frame.body)
        logger.info(f"Mp DB event listener received: {parsed_event}")

        if 'scientific_domains' in parsed_event['record']:
            update_user_information(parsed_event['record'])
        elif parsed_event['model'] == 'Project' and parsed_event['cud'] == 'create':
            add_project(parsed_event['record'])
        elif parsed_event['model'] == 'Project' and parsed_event['cud'] == 'destroy':
            delete_project(parsed_event['record'])


def initialize_databus_listeners():
    # Subscribe to user actions
    LISTENER_CONNECTIONS.append(
        subscribe_to_databus(host=APP_SETTINGS['CREDENTIALS']['DATABUS_HOST'],
                             port=APP_SETTINGS['CREDENTIALS']['DATABUS_PORT'],
                             username=APP_SETTINGS['CREDENTIALS']['DATABUS_LOGIN'],
                             password=APP_SETTINGS['CREDENTIALS']['DATABUS_PASSWORD'],
                             listener=UserActionsListener(), subscription_id="user_action",
                             topic="/topic/user_actions")
    )

    # Subscribe to marketplace database changes
    LISTENER_CONNECTIONS.append(
        subscribe_to_databus(host=APP_SETTINGS['CREDENTIALS']['DATABUS_HOST'],
                             port=APP_SETTINGS['CREDENTIALS']['DATABUS_PORT'],
                             username=APP_SETTINGS['CREDENTIALS']['DATABUS_LOGIN'],
                             password=APP_SETTINGS['CREDENTIALS']['DATABUS_PASSWORD'],
                             listener=MpDbEventListener(), subscription_id="mp_db_events",
                             topic="/topic/mp_db_events")
    )

    logger.info(f"Successfully subscribed to {len(LISTENER_CONNECTIONS)} topics")


def shutdown_databus_listeners():
    for listener in LISTENER_CONNECTIONS:
        listener.disconnect()
