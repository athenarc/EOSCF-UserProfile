import logging

from api.utils import form_mongo_url
from pymongo import MongoClient

logger = logging.getLogger(__name__)


def add_project(record):
    client = MongoClient(form_mongo_url())
    new_project = {
        'project_id': record['id'],
        'services': []
    }

    _ = client['user_profile']['user'].update_one(
        {"user_id": record['user_id']},
        {'$push': {'projects': new_project}}
    )
    logger.info('Added new project')


def delete_project(record):
    client = MongoClient(form_mongo_url())

    _ = client['user_profile']['user'].update_one(
        {'user_id': record['user_id']},
        {
            '$pull':
            {
                'projects': {'project_id': record['id']}
            }
        }
    )
    logger.info('Deleted project')
