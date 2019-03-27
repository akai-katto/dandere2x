from Dandere2x import Dandere2x

# #init__(self, frame_count, waifu2x_caffe_dir, output_dir, upscaled_dir, p_setting, noise_level, scale_factor
# waifu2x_caffe_dir = "C:\\Users\\windwoz\\Desktop\\releases\\pre0.3\\dandere2x-complete\\waifu2x-caffe\\waifu2x-caffe-cui.exe"
# upscaled_dir = "C:\\Users\\windwoz\\Desktop\\pythontesting\\upscaled\\"
# output_dir = "C:\\Users\\windwoz\\Desktop\\pythontesting\\outputs\\"
#
# #le(waifu2x_caffe_dir, input, output, setting, noise_level, scale_factor):
# Waifu2x_Caffe.upscale_file(waifu2x_caffe_dir, "C:\\Users\\windwoz\\Desktop\\pythontesting\\inputs\\frame1.jpg",
#                            "C:\\Users\\windwoz\\Desktop\\pythontesting\\inputs\\output.jpg", "cudnn", "3","2.0")


# w = Waifu2x_Caffe(48, waifu2x_caffe_dir, output_dir, upscaled_dir, "cudnn", "3", "2.0")
#
#
# w.run()

d = Dandere2x('config.ini')

print(d.dandere2x_cpp_dir)
# d.start_dandere2x_cpp()
d.run()
# d.dif_thread()
