from context import Context
from dandere2x import Dandere2x

import threading

import yaml

def thread_test(dandere2x: Dandere2x):
    import time
    time.sleep(5)
    dandere2x.kill()

with open("C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\sideways_vid\\54\\suspended_session_data.yaml", "r") as read_file:
    config = yaml.safe_load(read_file)

# with open("dandere2x_win32.yaml", "r") as read_file:
#     config = yaml.safe_load(read_file)

context = Context(config)
context.load_video_settings()

dandere2x = Dandere2x(context)
dandere2x.start()

# class sleeper(threading.Thread):
#     def __init__(self, d2x):
#
#         super().__init__()
#         self.d2x = d2x
#
#     def run(self) -> None:
#         import time
#         time.sleep(15)
#         self.d2x.kill()
#
#
# sleeper_obj = sleeper(dandere2x)
# sleeper_obj.start()

dandere2x.join()
# sleeper_obj.join()