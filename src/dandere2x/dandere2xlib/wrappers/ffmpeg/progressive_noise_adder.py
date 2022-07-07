import threading


from dandere2x.dandere2xlib.utils.dandere2x_utils import rename_file_wait, wait_on_file
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import apply_noise_to_image


class ProgressiveNoiseAdder(threading.Thread):

    def __init__(self, extracted_frames_dir: str, noised_frames_dir: str, frame_count):
        super().__init__()
        self.extracted_frames_dir = extracted_frames_dir
        self.noised_frames_dir = noised_frames_dir

        self.ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        self.frame_count = frame_count

    def join(self, timeout=None):
        threading.Thread.join(self, timeout)

    def _noise_image_sub_thread(self, frame_number: int):
        extracted_image = self.extracted_frames_dir + "frame%s.png" % frame_number
        noise_extracted_image_temp = self.noised_frames_dir + "temp%s.png" % frame_number
        noise_extracted_image = self.noised_frames_dir + "frame%s.png" % frame_number

        apply_noise_to_image(ffmpeg_dir=self.ffmpeg_path,
                             input_image=extracted_image,
                             output_file=noise_extracted_image_temp)

        rename_file_wait(noise_extracted_image_temp, noise_extracted_image)

    def run(self):
        for count in range(1, self.frame_count + 1):
            extracted_image = self.extracted_frames_dir + "frame%s.png" % count

            wait_on_file(extracted_image)

            noise_sub_thread = threading.Thread(target=self._noise_image_sub_thread, args=(count,))
            noise_sub_thread.start()

