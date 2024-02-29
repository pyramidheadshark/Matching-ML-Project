import configparser


def create_config():
    config = configparser.ConfigParser()

    # Добавление параметров конфигурации
    config['General'] = {'debug': True, 'log_level': 'info'}
    config['Database'] = {'db_name': 'example_db',
                          'db_host': 'localhost', 'db_port': '5432'}

    # Write the configuration to a file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    create_config()