import json
import objectpath
from io import StringIO
import sys
import os

with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)


f = open("dump.json","w+")

this_folder = ''

if getattr(sys, 'frozen', False):
    this_folder = os.path.dirname(sys.executable)
elif __file__:
    this_folder = os.path.dirname(__file__)

this_folder = this_folder.replace("/", "\\\\")

strtest = str(config_json)

strtest = strtest.replace("\'", "\"")

strtest = strtest.replace("True", "true")

strtest = strtest.replace("False", "true")

strtest = strtest.replace("None", "null")

strtest = strtest.replace("..", this_folder)

config_test_3 = json.loads(strtest)


# f.write(strtest)
#
# with open("dump.json", "r") as read_file:
#     config_json_2 = json.load(read_file)
#
# print(config_json_2['dandere2x']['workspace'])