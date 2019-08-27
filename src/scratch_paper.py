from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
import json

with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)


d = Dandere2x_Gui_Wrapper(config_json)

d.start()
#

# import time
# from wrappers.frame import Frame
#
# start = time.time()
#
#
# f1 = Frame()
#
# f1.load_from_string("C:\\Users\\windwoz\\Pictures\\computational_tests\\3D\\output1.jpg")
#
#
# print("\n "
#       "duration: " + str(time.time() - start))
