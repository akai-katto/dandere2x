from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import apply_noise_to_image

ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

import time

start = time.time()

apply_noise_to_image(ffmpeg_dir=ffmpeg_path,
                     input_image=r"C:\Users\Tyler\Desktop\3.3\workspace\ffmpeg_test\output1.jpg",
                     output_file=r"C:\Users\Tyler\Desktop\3.3\workspace\ffmpeg_test\output_noise_python.jpg"
                     )

end = time.time()
print(end - start)