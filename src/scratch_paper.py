from wrappers.ffmpeg.ffmpeg import re_encode_video, check_if_file_is_video
from context import Context
import yaml
from dandere2x import Dandere2x

from wrappers.waifu2x.waifu2x_check import verify_waifu2x_works
from wrappers.waifu2x.waifu2x_vulkan import Waifu2xVulkan

configfile = "dandere2x_%s.yaml" % "win32"

# load yaml

with open(configfile, "r") as read_file:
    config = yaml.safe_load(read_file)

context = Context(config)

d2x = Dandere2x(context)
d2x.start()


#
# # check_if_file_is_video(context.ffprobe_dir, "C:\\Users\\windwoz\\Desktop\\building_folder\\1.9_src\\requirements.txt")
#
# # re_encode_video(context.ffprobe_dir, "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\text.txt",
# #                                      "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\out.txt",
# #                                      throw_exception=True)


# # def both_paths(sofar="S"):
# #     print(sofar)
# #     return lambda x:both_paths(x + "U"), lambda  x:both_paths(x + "D")
# #
# # up,down = both_paths()
# # upup, updown = up()
#
# def myfunc(n="S"):
#     print(n)
#     return lambda: myfunc(n+"U"), lambda: myfunc(n+"D")
# #
# # up, down = myfunc()
# # upup, downdown = up()
# # _ = upup()
# # downup, downdown = down()
#
# # def hewwo():
# #     print("hewwo")
# #
# # test = lambda: hewwo()
# # test()
# #
#

def null_merge(cp):
    return lambda: cp

def eat_sentence(np):
    return (lambda x: (np + " did " + (eat_phrase(x))), lambda x: (np + " didn't " + (eat_phrase(x))))

def eat_phrase(eat_ee):
    return (" ate a " + eat_ee)

did_sentence, didnt_sentece = lambda x: eat_sentence(x) # np unsatisfied, eat_ee unsatisfied
did_sentence_bar = did_sentence("sokei")   # np now satisfied, eat_ee unsatisfied
complete_sentence = did_sentence_bar("cookie") # everything satisfied


def up(n):
    print(n+"U")

def down(n):
    print(n+"D")

def both_ways(n):
    up(n)
    down(n)