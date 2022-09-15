from dotenv import dotenv_values
from pymongo import MongoClient


from populate_profile_db.utils import form_mongo_url


def get_user_actions(user_id):
    client = MongoClient(form_mongo_url())
    specific_user = {
        'user': user_id
    }
    result = client['rs_dump']['user_action'].find(
        filter=specific_user
    )

    def keep_specific_values(user_action, attributes):
        return {attribute: user_action[attribute] for attribute in attributes}

    kept_attributes = ['unique_id', 'timestamp', 'source', 'target', 'action']
    return [keep_specific_values(action, kept_attributes) for action in result]


def get_unauthenticated_users():
    client = MongoClient(form_mongo_url())

    unauthenticated_uids = client['rs_dump']['user_action'].distinct(
        'unique_id',
        filter={'user': {'$exists': False}}
    )

    return unauthenticated_uids


def get_unauthenticated_user_actions(uid):
    client = MongoClient(form_mongo_url())
    actions = client['rs_dump']['user_action'].find(
        {'unique_id': uid}
    )

    return [action for action in actions]
