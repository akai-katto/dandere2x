import yaml
from collections import OrderedDict

def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())

def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)

setup_yaml()

configfile = "dandere2x_win32.yaml"

# load yaml

with open(configfile, "r") as read_file:
    config = yaml.safe_load(read_file)

od = OrderedDict(config)

output_file = "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\output_test.yaml"

with open(output_file, "w") as write_file:
    yaml.dump(od,write_file, sort_keys=False)