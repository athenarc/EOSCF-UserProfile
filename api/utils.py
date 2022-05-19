from api.settings import APP_SETTINGS


def form_mongo_url() -> str:
    return f"mongodb://{APP_SETTINGS['CREDENTIALS']['MONGO']['USERNAME']}" \
           f":{APP_SETTINGS['CREDENTIALS']['MONGO']['PASSWORD']}" \
           f"@{APP_SETTINGS['BACKEND']['MONGO']['HOST']}:{APP_SETTINGS['BACKEND']['MONGO']['PORT']}"
