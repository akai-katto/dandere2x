from dandere2x import Dandere2x
import json
from wrappers.waifu2x_wrappers.waifu2x_vulkan import Waifu2xVulkan
from context import Context


with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)

context = Context(config_json)

waifu2x = Waifu2xVulkan(context)


waifu2x.upscale_file("C:\\Users\\windwoz\\Desktop\\1.2.12_github\\1.2.1.2\\demo_folder\\workspace\\inputs\\frame1.jpg",
                     "C:\\Users\\windwoz\\Desktop\\1.2.12_github\\1.2.1.2\\demo_folder\\workspace\\upscaled.png")