import json


with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)

print(config_json['dandere2x']['block_size'])

config_json['dandere2x']['block_size'] = 15

print(config_json['dandere2x']['block_size'])
