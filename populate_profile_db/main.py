import subprocess
import time

from dotenv import dotenv_values
from populate_profile_db.populate_db import execute_db_population

env_variables = dotenv_values(".env")


def docker_compose_up(compose_file: str):
    compose_file_name = compose_file.split('/')[-1]
    with open(f'storage/logs/logs-{compose_file_name[:-4]}.txt', 'w') as log_file:
        subprocess.run(["docker-compose", f"-f{compose_file}", "up", "-d"],
                       stdout=log_file,
                       stderr=log_file)


def docker_compose_stop(compose_file: str):
    compose_file_name = compose_file.split('/')[-1]
    with open(f'storage/logs/logs-{compose_file_name[:-4]}.txt', 'w') as log_file:
        subprocess.run(["docker-compose", f"-f{compose_file}", "stop"],
                       stdout=log_file,
                       stderr=log_file)


def is_mongo_ready() -> bool:
    output = subprocess.run([f"docker exec -i mongo_profile sh -c \"mongosh "
                             f"--username {env_variables['USER_PROFILE_MONGO_USERNAME']} "
                             f"--password {env_variables['USER_PROFILE_MONGO_PASSWORD']} "
                             "--eval \\\"printjson(db.serverStatus().ok)\\\"\""],
                            capture_output=True, shell=True)

    try:
        return str(output.stdout).split('\\n')[-2] == "1"
    except IndexError:
        return False


def import_dumps() -> None:
    # RS dump
    _ = subprocess.run(["docker exec -i mongo_profile sh -c \"mongorestore "
                        f"--username {env_variables['USER_PROFILE_MONGO_USERNAME']} "
                        f"--password {env_variables['USER_PROFILE_MONGO_PASSWORD']} "
                        "--authenticationDatabase admin "
                        f"--db {env_variables['RS_MONGO_DB']} --dir /dump/recommender\""],
                       capture_output=True, shell=True)


def wait_for_dbs(max_retries=20, sleep_seconds=3) -> None:
    for _ in range(max_retries):
        mongo_ready = is_mongo_ready()

        if mongo_ready:
            return

        time.sleep(sleep_seconds)

    raise ConnectionError(f"DBs were not ready after {max_retries} retries.")


def main():
    # DOCKER_COMPOSE_PATH = 'docker-compose-init.yml'
    #
    # # Start the two databases
    # print("> Starting mongo container...", end='')
    # docker_compose_up(DOCKER_COMPOSE_PATH)
    #
    # # Make sure that both mongo and postgres are up and running
    # wait_for_dbs(max_retries=60, sleep_seconds=3)
    # print("Done")

    print("> Importing RS mongo dump...", end='', flush=True)
    import_dumps()
    print("Done")

    print("> Populating user profile collection...", flush=True)
    execute_db_population()
    print("Done")

    # print("> Stopping mongo and postgres containers...", end='')
    # docker_compose_stop(DOCKER_COMPOSE_PATH)
    # print("Done")


if __name__ == '__main__':
    main()
