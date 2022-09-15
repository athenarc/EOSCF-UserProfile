from dotenv import dotenv_values
from populate_profile_db.generate_profiles import (
    create_unauthenticated_profiles_from_dbs, create_user_profile_from_dbs)
from pymongo import MongoClient

from populate_profile_db.utils import form_mongo_url


def import_user_profiles(user_profiles):
    client = MongoClient(form_mongo_url())
    client['user_profile']['user'].drop()
    client['user_profile']['user'].insert_many(user_profiles)
    client['user_profile']['user'].create_index('id', name='user_id_index')


def execute_db_population():
    authenticated_profiles = create_user_profile_from_dbs()

    # For the unauthenticated users we only keep their user_actions and recommendations
    unauthenticated_profiles = create_unauthenticated_profiles_from_dbs()

    authenticated_profiles.extend(unauthenticated_profiles)

    import_user_profiles(authenticated_profiles)


if __name__ == '__main__':
    execute_db_population()
