#!/usr/bin/env python3

import os, json

config = {"key1": "value1", "key2": "value2"}

if not os.path.isfile('config.json'):
    with open('config.json', 'w') as f:
        json.dump(config, f)

with open('config.json', 'r') as f:
    config = json.load(f)

print(config)

#edit the data
if not config.get('key3'):
     config['key3'] = 0

config['key3'] = config['key3'] + 1

# write it back to the file
with open('config.json', 'w') as f:
    json.dump(config, f)

