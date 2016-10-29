# -*- coding: utf-8 -*-
import json
import os

config = json.loads(''.join(open(os.path.join(os.getcwd(),'relaybot','config.json'), 'r').readlines()))
