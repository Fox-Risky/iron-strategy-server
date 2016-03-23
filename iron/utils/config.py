import configparser
import os

def open_server_config():
    server_conf_path = os.path.abspath(os.path.join('conf', 'iron.conf'))
    if not os.path.exists(server_conf_path):
        raise RuntimeError("Config error: file {} does not exists".format(server_conf_path))
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join('conf', 'iron.conf')))
    return config
