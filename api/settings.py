import argparse

import yaml
from dotenv import dotenv_values


def read_settings():
    parser = argparse.ArgumentParser(description="User profile CMD.")
    parser.add_argument(
        "--config_file", help="path to config file", type=str, required=True
    )
    args = parser.parse_args()

    with open(args.config_file) as file:
        backend_settings = yaml.load(file, Loader=yaml.FullLoader)

    credentials = dotenv_values(".env")

    return {
        'BACKEND': backend_settings,
        'CREDENTIALS': credentials
    }


APP_SETTINGS = read_settings()
