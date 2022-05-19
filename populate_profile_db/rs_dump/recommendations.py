import yaml
from pymongo import MongoClient

with open('credentials.yaml') as file:
    mongo_config = yaml.load(file, Loader=yaml.FullLoader)['MONGO']
    MONGO_CONNECTION_STRING = f"mongodb://{mongo_config['USERNAME']}:{mongo_config['PASSWORD']}" \
                              f"@{mongo_config['HOST']}:{mongo_config['PORT']}"


def get_user_recommendations(user_id):
    client = MongoClient(MONGO_CONNECTION_STRING)

    specific_user = {
        'user': user_id
    }
    result = client['rs_dump']['recommendation'].find(
        filter=specific_user
    )

    def keep_specific_values(user_action, attributes):
        return {attribute: user_action.get(attribute) for attribute in attributes}

    kept_attributes = ['timestamp', 'page_id', 'panel_id', 'services']
    return [keep_specific_values(recom, kept_attributes) for recom in result]


def get_unauthenticated_user_recommendations(uid):
    client = MongoClient(MONGO_CONNECTION_STRING)

    specific_user = {
        'unique_id': uid
    }
    result = client['rs_dump']['recommendation'].find(
        filter=specific_user
    )

    def keep_specific_values(user_action, attributes):
        return {attribute: user_action.get(attribute) for attribute in attributes}

    kept_attributes = ['timestamp', 'page_id', 'panel_id', 'services']
    return [keep_specific_values(recom, kept_attributes) for recom in result]
