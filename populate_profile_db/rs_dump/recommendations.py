from dotenv import dotenv_values
from pymongo import MongoClient

from populate_profile_db.utils import form_mongo_url


def get_user_recommendations(user_id):
    client = MongoClient(form_mongo_url())

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
    client = MongoClient(form_mongo_url())

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
