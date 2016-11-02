# -*- coding: utf-8 -*-
import json
import os

config_path = os.path.join(os.getcwd(),'relaybot','config.json')
config = json.loads(''.join(open(config_path, 'r').readlines()))
