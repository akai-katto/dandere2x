from context import Context
from dandere2x import Dandere2x
from wrappers.ffmpeg.pipe_thread import Pipe
from wrappers.frame.frame import Frame

import yaml

with open("dandere2x_win32.yaml", "r") as read_file:
    config = yaml.safe_load(read_file)

context = Context(config)
context.load_video_settings()


# pipe = Pipe(context, "output.mkv")
# test = Frame()
# test.create_new(1920,1080)
# pipe.start()
# print('rawr')
# pipe.save(test)
# pipe.join()

#
dandere2x = Dandere2x(context)
dandere2x.start()
#
# # import time
# # time.sleep(5)
# # dandere2x.context.controller.kill()
#
dandere2x.join()