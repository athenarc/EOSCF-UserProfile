from populate_profile_db.mp_dump.queries import projects, user
from populate_profile_db.rs_dump.recommendations import (
    get_unauthenticated_user_recommendations, get_user_recommendations)
from populate_profile_db.rs_dump.user_actions import (
    get_unauthenticated_user_actions, get_unauthenticated_users,
    get_user_actions)
from tqdm import tqdm


def create_user_profile_from_dbs():
    users = user.get_users()
    users = [attributes.to_dict() for _, attributes in users.iterrows()]

    for usr in tqdm(users, desc='Exporting authenticated users'):
        add_scientific_domain(usr)
        add_categories_of_interest(usr)
        add_projects(usr)
        add_user_actions(usr)
        add_user_recommendations(usr)

    return users


def create_unauthenticated_profiles_from_dbs():
    unauth_users = []
    uids = get_unauthenticated_users()

    for uid in tqdm(uids, desc='Exporting unauthenticated users'):
        unauth_users.append({
            'unique_id': uid,
            'user_actions': get_unauthenticated_user_actions(uid),
            'recommendations': get_unauthenticated_user_recommendations(uid)
        })

    return unauth_users


def add_scientific_domain(usr):
    usr['user_scientific_domains'] = user.get_user_scientific_domains(usr['id'])


def add_categories_of_interest(usr):
    usr['user_categories'] = user.get_user_interest_categories(usr['id'])


def add_projects(usr):
    projs = projects.get_projects(usr['id'])
    projs = [attributes.to_dict() for _, attributes in projs.iterrows()]

    for proj in projs:
        proj['project_scientific_domain'] = projects.get_project_scientific_domains(proj['id'])
        proj['services'] = projects.get_project_services(proj['id'])

    usr['projects'] = projs


def add_user_actions(usr):
    usr['user_actions'] = get_user_actions(usr['id'])


def add_user_recommendations(usr):
    usr['recommendations'] = get_user_recommendations(usr['id'])


# def export_profiles(store_path):
#     user_profiles = create_user_profile_from_dumps()
#
#     with open(store_path, 'w') as outfile:
#         json.dump(user_profiles, outfile)
