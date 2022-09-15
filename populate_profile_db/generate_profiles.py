from populate_profile_db.rs_dump import (projects, recommendations,
                                         user_actions, users)
from tqdm import tqdm


def create_user_profile_from_dbs():
    rs_users = users.get_users()

    for usr in tqdm(rs_users, desc='Exporting authenticated users'):
        add_projects(usr)
        add_user_actions(usr)
        add_user_recommendations(usr)

    return rs_users


def create_unauthenticated_profiles_from_dbs():
    unauth_users = []
    uids = user_actions.get_unauthenticated_users()

    for uid in tqdm(uids, desc='Exporting unauthenticated users'):
        unauth_users.append({
            'unique_id': uid,
            'user_actions': user_actions.get_unauthenticated_user_actions(uid),
            'recommendations': recommendations.get_unauthenticated_user_recommendations(uid)
        })

    return unauth_users


def add_projects(usr):
    projs = projects.get_user_projects(usr['user_id'])

    usr['projects'] = projs


def add_user_actions(usr):
    usr['user_actions'] = user_actions.get_user_actions(usr['user_id'])


def add_user_recommendations(usr):
    usr['recommendations'] = recommendations.get_user_recommendations(usr['user_id'])


# def export_profiles(store_path):
#     user_profiles = create_user_profile_from_dumps()
#
#     with open(store_path, 'w') as outfile:
#         json.dump(user_profiles, outfile)
