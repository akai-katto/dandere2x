import os
import threading
import time

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value
from wrappers.cv2.progress_frame_extractor_cv2 import ProgressiveFramesExtractorCV2


class MinDiskUsage:
    """
    A class to facilitate the actions needed to operate min_disk_usage.
    """

    def __init__(self, context: Context):

        self.context = context
        self.frame_count = context.frame_count
        self.progressive_frame_extractor = ProgressiveFramesExtractorCV2(self.context)

    def run(self):
        """
        Waits for signal_merged_count to change, then deletes the respective files before it.
        """

        for x in range(1, self.frame_count - 1):

            # wait for signal to get ahead of MinDiskUsage
            while x >= self.context.signal_merged_count:
                time.sleep(.00001)

            # when it does get ahead, extract the next frame
            self.progressive_frame_extractor.next_frame()
            self.__delete_used_files(x)

    def extract_initial_frames(self):
        """
        Extract 'max_frames_ahead' initial frames to start out with.
        """
        max_frames_ahead = self.context.max_frames_ahead

        for x in range(max_frames_ahead):
            self.progressive_frame_extractor.next_frame()

    def __delete_used_files(self, remove_before):
        """
        Delete the files produced by dandere2x up to index_to_remove.
        """

        # load context

        pframe_data_dir = self.context.pframe_data_dir
        residual_data_dir = self.context.residual_data_dir
        correction_data_dir = self.context.correction_data_dir
        fade_data_dir = self.context.fade_data_dir
        input_frames_dir = self.context.input_frames_dir
        compressed_static_dir = self.context.compressed_static_dir
        compressed_moving_dir = self.context.compressed_moving_dir
        residual_upscaled_dir = self.context.residual_upscaled_dir

        # get the files to delete "_r(emove)"

        index_to_remove = str(remove_before - 2)

        prediction_data_file_r = pframe_data_dir + "pframe_" + index_to_remove + ".txt"
        residual_data_file_r = residual_data_dir + "residual_" + index_to_remove + ".txt"
        correction_data_file_r = correction_data_dir + "correction_" + index_to_remove + ".txt"
        fade_data_file_r = fade_data_dir + "fade_" + index_to_remove + ".txt"

        input_image_r = input_frames_dir + "frame" + index_to_remove + ".jpg"

        compressed_file_static_r = compressed_static_dir + "compressed_" + index_to_remove + ".jpg"
        compressed_file_moving_r = compressed_moving_dir + "compressed_" + index_to_remove + ".jpg"

        # "mark" them
        remove = [prediction_data_file_r, residual_data_file_r, correction_data_file_r,
                  fade_data_file_r, input_image_r,  # upscaled_file_r,
                  compressed_file_static_r, compressed_file_moving_r]

        upscaled_file_r = residual_upscaled_dir + "output_" + get_lexicon_value(6, int(remove_before)) + ".png"
        remove.append(upscaled_file_r)

        # remove
        threading.Thread(target=self.__delete_files_from_list, args=(remove,), daemon=True).start()

    @staticmethod
    def __delete_files_from_list(files):
        """
        Delete all the files in a given list
        """
        for item in files:
            c = 0
            while True:
                if os.path.isfile(item):
                    try:
                        os.remove(item)
                        break
                    except OSError:
                        c += 1
                else:
                    c += 1
                if c == 20:
                    break
                time.sleep(0.1)
