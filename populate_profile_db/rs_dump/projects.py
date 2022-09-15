from dotenv import dotenv_values
from pymongo import MongoClient
from populate_profile_db.utils import form_mongo_url


def get_user_projects(user_id):
    client = MongoClient(form_mongo_url())

    specific_user = {
        'user_id': user_id
    }
    projects = client['rs_dump']['project'].find(
        filter=specific_user
    )

    def keep_specific_attributes(project):
        return {
            'project_id': project['_id'],
            'services': project['services']
        }

    return [keep_specific_attributes(project) for project in projects]
