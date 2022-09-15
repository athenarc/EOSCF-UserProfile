from api.settings import APP_SETTINGS


def form_mongo_url() -> str:
    return f"mongodb://{APP_SETTINGS['CREDENTIALS']['USER_PROFILE_MONGO_USERNAME']}" \
           f":{APP_SETTINGS['CREDENTIALS']['USER_PROFILE_MONGO_PASSWORD']}" \
           f"@{APP_SETTINGS['CREDENTIALS']['USER_PROFILE_MONGO_HOST']}" \
           f":{APP_SETTINGS['CREDENTIALS']['USER_PROFILE_MONGO_PORT']}"
