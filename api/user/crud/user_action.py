import logging
from uuid import UUID

import bson
import pymongo.errors
from api.utils import form_mongo_url
from pymongo import MongoClient

logger = logging.getLogger(__name__)


def get_user_info(user_id):
    client = MongoClient(form_mongo_url())

    specific_user = {
        'user_id': user_id
    }
    result = client['user_profile']['user'].find_one(
        specific_user, {"_id": 0}
    )

    if result is None:
        return None

    transform_uuids(result)

    logger.info(f"Found user with id {user_id}")

    return result


def transform_uuids(usr):
    for action in usr['user_actions']:
        action['unique_id'] = str(UUID(bytes=action['unique_id']))
        action['source']['visit_id'] = str(UUID(bytes=action['source']['visit_id']))
        action['target']['visit_id'] = str(UUID(bytes=action['target']['visit_id']))


def add_authorized_user_action(action):
    client = MongoClient(form_mongo_url())
    print(action['user_id'])
    res = client['user_profile']['user'].update_one(
        {"user_id": action['user_id']},
        {'$push': {'user_actions': action}}
    )

    return res


def add_anonymous_user_action(action):
    unique_id = action['unique_id']

    # We first check if this is the first anonymous user action (does not exist yet to our users)
    client = MongoClient(form_mongo_url())
    res = client['user_profile']['user'].find_one(
        {'unique_id': bson.Binary.from_uuid(UUID(unique_id))}
    )
    if res is None:
        create_anonymous_user(unique_id)

    res = client['user_profile']['user'].update_one(
        {"unique_id": bson.Binary.from_uuid(UUID(unique_id))},
        {'$push': {'user_actions': action}}
    )

    return res


def add_user_action(action):
    if 'user_id' in action:
        res = add_authorized_user_action(action)
    elif action['unique_id'] is not None:
        res = add_anonymous_user_action(action)
    else:
        logger.info("No unique_id or user_id was given")
        return

    if res.matched_count != 1:
        raise ValueError(f"Failed to find user on action: {action}")
    elif res.modified_count != 1:
        raise ValueError(f"Update failed on action: {action}")

    logger.info(f"Updated actions of user with action: {action}")


def create_anonymous_user(unique_id):
    client = MongoClient(form_mongo_url())
    result = client['user_profile']['user'].insert_one(
        {
            'unique_id': bson.Binary.from_uuid(UUID(unique_id)),
            'user_actions': [],
            'recommendations': []
        }
    )

    if result.inserted_id is None:
        raise pymongo.errors.WriteError(f"Could not create anonymous user with unique id {unique_id}")
