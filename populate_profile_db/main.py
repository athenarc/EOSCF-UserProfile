import subprocess
import time

from populate_profile_db.create_env import create_env_file_in_root
from populate_profile_db.populate_db import execute_db_population


def docker_compose_up(compose_file: str):
    compose_file_name = compose_file.split('/')[-1]
    with open(f'storage/logs/logs-{compose_file_name}', 'w') as log_file:
        subprocess.run(["docker-compose", f"-f{compose_file}", "up", "-d"],
                       stdout=log_file,
                       stderr=log_file)


def docker_compose_stop(compose_file: str):
    compose_file_name = compose_file.split('/')[-1]
    with open(f'storage/logs/logs-{compose_file_name}', 'w') as log_file:
        subprocess.run(["docker-compose", f"-f{compose_file}", "stop"],
                       stdout=log_file,
                       stderr=log_file)


def is_postgres_ready() -> bool:
    output = subprocess.run(["docker exec --user postgres -i postgres sh -c \"pg_isready\""],
                            capture_output=True, shell=True)

    return "accepting connections" in str(output.stdout)


def is_mongo_ready() -> bool:
    output = subprocess.run(["docker exec -i mongo sh -c \"mongo --username admin --password admin "
                             "--eval \\\"printjson(db.serverStatus().ok)\\\"\""],
                            capture_output=True, shell=True)

    try:
        return str(output.stdout).split('\\n')[-2] == "1"
    except IndexError:
        return False


def import_dumps() -> None:
    # Marketplace dump
    _ = subprocess.run(["docker exec --user postgres -i postgres sh -c \"createdb mp_dump\""],
                       capture_output=True, shell=True)
    _ = subprocess.run(["docker exec --user postgres -i postgres sh -c \"psql mp_dump < /dump/mp_db_dump_ano.sql\""],
                       capture_output=True, shell=True)

    # RS dump
    _ = subprocess.run(["docker exec -i mongo sh -c \"mongorestore --username admin --password admin "
                        "--authenticationDatabase admin --db rs_dump --dir /dump/recommender\""],
                       capture_output=True, shell=True)


def wait_for_dbs(max_retries=20, sleep_seconds=3) -> None:
    for _ in range(max_retries):
        mongo = is_mongo_ready()
        postgres = is_postgres_ready()

        if mongo and postgres:
            return

        time.sleep(sleep_seconds)

    raise ConnectionError(f"DBs were not ready after {max_retries} retries.")


if __name__ == '__main__':
    DOCKER_COMPOSE_PATH = 'docker-compose-init.yml'
    # MONGO_DOCKER_COMPOSE_PATH = 'user_profile/populate_profile_db/docker-compose-files/docker-compose-mongo.yml'
    # POSTGRES_DOCKER_COMPOSE_PATH = 'user_profile/populate_profile_db/docker-compose-files/docker-compose-postgres.yml'
    CREDENTIALS_PATH = 'credentials.yaml'

    # Set up the .env file that the compose files will use to interpolate secrets
    print("> Creating .env file...", end='')
    create_env_file_in_root(CREDENTIALS_PATH, env_file_path='.env')
    print("Done")

    # Start the two databases
    print("> Starting mongo and postgres containers...", end='')
    docker_compose_up(DOCKER_COMPOSE_PATH)
    # docker_compose_up(POSTGRES_DOCKER_COMPOSE_PATH)

    # Make sure that both mongo and postgres are up and running
    wait_for_dbs(max_retries=60, sleep_seconds=3)
    print("Done")

    print("> Importing marketplace and RS dumps...", end='')
    import_dumps()
    print("Done")

    print("> Populating user profile collection...", )
    execute_db_population()
    print("Done")

    print("> Stopping mongo and postgres containers...", end='')
    docker_compose_stop(DOCKER_COMPOSE_PATH)
    # docker_compose_stop(MONGO_DOCKER_COMPOSE_PATH)
    print("Done")
