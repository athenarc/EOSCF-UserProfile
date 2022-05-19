import pandas as pd
from populate_profile_db.mp_dump.connection import connect_and_query


def get_projects(user_id):
    attributes = ['id', 'name', 'reason_for_access', 'additional_information', 'customer_typology', 'email',
                  'user_group_name', 'organization', 'countries_of_partnership', 'webpage', 'status']

    # select_attributes = ', '.join([f"projects.{attribute}" for attribute in attributes])
    select_attributes = ', '.join(attributes)
    query = f"""
    SELECT {select_attributes}
    FROM projects
    WHERE projects.user_id = {user_id}
    """

    results = pd.DataFrame(connect_and_query(query, ()), columns=attributes)

    return results


def get_project_scientific_domains(proj_id):
    query = f"""
    SELECT scientific_domains.name
    FROM project_scientific_domains, scientific_domains
    WHERE project_scientific_domains.project_id = {proj_id}
        AND scientific_domains.id = project_scientific_domains.scientific_domain_id
    """

    return [domain[0] for domain in connect_and_query(query, ())]


def get_project_services(proj_id):
    query = f"""
        SELECT services.id
        FROM offers, services, project_items
        WHERE project_items.offer_id = offers.id AND offers.service_id = services.id
            AND project_id = {proj_id}
        """

    return [service[0] for service in connect_and_query(query, ())]
