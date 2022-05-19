import yaml


def create_env_file_in_root(credentials_path, env_file_path) -> None:
    with open(credentials_path) as file:
        credentials = yaml.load(file, Loader=yaml.FullLoader)

    shallow_credentials = {}
    for db_name, cred in credentials.items():
        for cred_name, cred_value in cred.items():
            shallow_credentials[f"{db_name}_{cred_name}"] = cred_value

    lines = [f"{key}=\"{val}\"\n" for key, val in shallow_credentials.items()]

    with open(env_file_path, 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    create_env_file_in_root('user_profile/credentials.yaml', env_file_path='.env')
