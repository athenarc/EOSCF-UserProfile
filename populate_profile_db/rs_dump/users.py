from dotenv import dotenv_values
from pymongo import MongoClient
from populate_profile_db.utils import form_mongo_url

env_variables = dotenv_values(".env")


def get_users():
    client = MongoClient(form_mongo_url())

    users = client['rs_dump']['user'].find()

    def keep_specific_attributes(user):
        return {
            'user_id': user['_id'],
            'scientific_domains': user['scientific_domains'],
            'categories': user['categories']
        }

    return [keep_specific_attributes(user) for user in users]
