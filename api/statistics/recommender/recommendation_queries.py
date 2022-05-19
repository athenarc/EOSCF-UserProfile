from typing import List

from api.utils import form_mongo_url
from pymongo import MongoClient


def get_number_of_recommendations_monthly(service_ids: List[int]):
    client = MongoClient(form_mongo_url())

    result = client['user_profile']['user'].aggregate([
        {
            '$match': {
                'recommendations': {
                    '$not': {
                        '$size': 0
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'recommendations.services': 1,
                'recommendations.timestamp': 1
            }
        }, {
            '$unwind': {
                'path': '$recommendations',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$unwind': {
                'path': '$recommendations.services'
            }
        }, {
            '$match': {
                'recommendations.services': {
                    '$in': service_ids
                }
            }
        }, {
            '$group': {
                '_id': {
                    'service_id': '$recommendations.services',
                    'month': {
                        '$month': '$recommendations.timestamp'
                    },
                    'year': {
                        '$year': '$recommendations.timestamp'
                    }
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$project': {
                'count': 1,
                '_id': 1
            }
        }, {
            '$sort': {
                '_id.service_id': 1,
                '_id.year': 1,
                '_id.month': 1
            }
        }
    ])

    return [(recommendations_per_service['_id'], recommendations_per_service['count'])
            for recommendations_per_service in result]
