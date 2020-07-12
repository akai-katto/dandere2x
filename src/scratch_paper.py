from context import Context
from dandere2x import Dandere2x

import yaml

with open("dandere2x_win32.yaml", "r") as read_file:
    config = yaml.safe_load(read_file)

context = Context(config)
dandere2x = Dandere2x(context)
dandere2x.start()

import time
time.sleep(5)
dandere2x.context.controller.kill()

dandere2x.join()