# import time
#
# from dandere2x import Dandere2x
# import json
# from context import Context
#
# start = time.time()
#
# # resume only works if
#
# with open("dandere2x.json", "r") as read_file:
#     config_json = json.load(read_file)
#
# context = Context(config_json)
#
# d = Dandere2x(context)
# d.resume_concurrent()
#
# end = time.time()
#
# print("\n duration: " + str(time.time() - start))
#
#

from wrappers.frame.frame import Frame

f = Frame()

f.load_from_string("C:\\Users\\windwoz\\Documents\\github_projects\\src\\workspace\\workspace1\\inputs\\frame1.jpg")