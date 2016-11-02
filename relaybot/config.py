# -*- coding: utf-8 -*-
import json
import os

config_path = os.path.join(os.getcwd(),'relaybot','config.json')
print config_path
print ''.join(open(config_path, 'r').readlines())
config = json.loads(''.join(open(config_path, 'r').readlines()))
