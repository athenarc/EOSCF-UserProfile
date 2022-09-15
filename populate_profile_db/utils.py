from dotenv import dotenv_values

env_variables = dotenv_values(".env")


def form_mongo_url() -> str:
    return f"mongodb://{env_variables['USER_PROFILE_MONGO_USERNAME']}" \
           f":{env_variables['USER_PROFILE_MONGO_PASSWORD']}" \
           f"@localhost" \
           f":{env_variables['USER_PROFILE_MONGO_PORT']}"
