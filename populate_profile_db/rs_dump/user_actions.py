import yaml
from pymongo import MongoClient

with open('credentials.yaml') as file:
    mongo_config = yaml.load(file, Loader=yaml.FullLoader)['MONGO']
    MONGO_CONNECTION_STRING = f"mongodb://{mongo_config['USERNAME']}:{mongo_config['PASSWORD']}" \
                              f"@{mongo_config['HOST']}:{mongo_config['PORT']}"


def get_user_actions(user_id):
    client = MongoClient(MONGO_CONNECTION_STRING)

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
    client = MongoClient(MONGO_CONNECTION_STRING)

    unauthenticated_uids = client['rs_dump']['user_action'].distinct(
        'unique_id',
        filter={'user': {'$exists': False}}
    )

    return unauthenticated_uids


def get_unauthenticated_user_actions(uid):
    client = MongoClient(MONGO_CONNECTION_STRING)
    actions = client['rs_dump']['user_action'].find(
        {'unique_id': uid}
    )

    return [action for action in actions]
