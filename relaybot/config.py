# -*- coding: utf-8 -*-
import json
import os

config_path = os.path.join(os.getcwd(),'relaybot','config.json')
config = json.loads(''.join(open(config_path, 'r').readlines()))


def reload_config():
    config = json.loads(''.join(open(config_path, 'r').readlines()))


def save_config():
    configstr = json.dumps(config, indent=4, sort_keys=True)
    with open(config_path, 'w') as config_file:
        config_file.write(configstr)


def add_to(steamid, key):
    config[key].append(steamid)
    save_config()


def remove_from(steamid, key):
    config[key].remove(steamid)
    save_config()
