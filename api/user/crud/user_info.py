import logging

from api.utils import form_mongo_url
from pymongo import MongoClient

logger = logging.getLogger(__name__)


def update_user_information(record):
    client = MongoClient(form_mongo_url())

    _ = client['user_profile']['user'].update_one(
        {"user_id": record['id']},
        {'$push': {
            'scientific_domains': record['scientific_domains'],
            'categories': record['categories']
        }}
    )
    logger.info('Updated user profile information')
