import os


def env_loader():
    variables = {
        'DB_URL': os.getenv('DB_URL', ''),
        'DB_NAME': os.getenv('DB_NAME', ''),
        'ACCESS_TOKEN': os.getenv('ACCESS_TOKEN', '')
    }
    print(variables['DB_URL'])
    with open('loaded-env.txt', 'w') as f:
        for name in variables:
            f.write(f'{name}={variables[name]}\n')
        f.close()


if __name__ == "__main__":
    env_loader()