import pandas as pd
from populate_profile_db.mp_dump.connection import connect_and_query


def get_users():
    user_attributes = ['id', 'roles_mask', 'created_at']

    select_attributes = ', '.join(user_attributes)
    query = f'SELECT {select_attributes} FROM users'
    results = pd.DataFrame(connect_and_query(query, ()), columns=user_attributes)

    return results


def get_user_scientific_domains(user_id) -> list[str]:
    query = f"""
    SELECT scientific_domains.name
    FROM scientific_domains, user_scientific_domains
    WHERE user_scientific_domains.scientific_domain_id = scientific_domains.id AND
            user_scientific_domains.user_id = {user_id}
    """

    return [domain[0] for domain in connect_and_query(query, ())]


def get_user_interest_categories(user_id) -> list[str]:
    query = f"""
    SELECT categories.name
    FROM categories, user_categories
    WHERE user_categories.category_id = categories.id AND user_categories.user_id = {user_id}
    """

    return [interest[0] for interest in connect_and_query(query, ())]
