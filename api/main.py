import logging

import sentry_sdk
import uvicorn
from api.routes.add_routes import initialize_routes
from api.settings import APP_SETTINGS
from api.user.databus.listeners import (initialize_databus_listeners,
                                        shutdown_databus_listeners)
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(asctime)s | %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')


@app.get("/health")
def health_check():
    return {"message": "App has initialised and is running"}


@app.on_event("startup")
async def startup_event():
    sentry_sdk.init(dsn=APP_SETTINGS['CREDENTIALS']['SENTRY_DSN'],
                    traces_sample_rate=1.0)
    initialize_routes(app)
    initialize_databus_listeners()


@app.on_event("shutdown")
async def shutdown_event():
    shutdown_databus_listeners()


def start_app():
    uvicorn.run("api.main:app",
                host=APP_SETTINGS['BACKEND']['FASTAPI']['HOST'],
                port=APP_SETTINGS['BACKEND']['FASTAPI']['PORT'],
                reload=APP_SETTINGS['BACKEND']['FASTAPI']['RELOAD'],
                debug=APP_SETTINGS['BACKEND']['FASTAPI']['DEBUG'],
                workers=APP_SETTINGS['BACKEND']['FASTAPI']['WORKERS'],
                reload_dirs=["user_profile/api"])


if __name__ == '__main__':
    start_app()
