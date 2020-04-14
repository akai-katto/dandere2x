#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import threading

from context import Context
from dandere2xlib.core.plugins.correction import correct_image
from dandere2xlib.core.plugins.fade import fade_image
from dandere2xlib.core.plugins.pframe import pframe_image
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, get_list_from_file_wait, wait_on_file
from dandere2xlib.utils.thread_utils import CancellationToken
from wrappers.ffmpeg.pipe import Pipe
from wrappers.frame.asyncframe import AsyncFrameWrite, AsyncFrameRead
from wrappers.frame.frame import Frame


class Merge(threading.Thread):
    """
    Description:
        - This class is the driver for merging all the files that need to be merged together.
          Essentially, it calls the 'make_merge_image' method for every image that needs to be upscaled.
        - Other tasks are to ensure the files exist, async writing for optimizations, as well
          as signalling to other parts of Dandere2x we've finished upscaling.
    """

    def __init__(self, context: Context):

        self.context = context
        # load variables from context
        self.workspace = context.workspace
        self.upscaled_dir = context.residual_upscaled_dir
        self.merged_dir = context.merged_dir
        self.residual_data_dir = context.residual_data_dir
        self.pframe_data_dir = context.pframe_data_dir
        self.correction_data_dir = context.correction_data_dir
        self.fade_data_dir = context.fade_data_dir
        self.frame_count = context.frame_count
        self.extension_type = context.extension_type
        self.nosound_file = context.nosound_file
        self.preserve_frames = context.preserve_frames
        self.logger = logging.getLogger(__name__)
        self.start_frame = 1

        # setup the pipe for merging

        self.pipe = Pipe(context, self.nosound_file)

        # Threading Specific

        self.alive = True
        self.cancel_token = CancellationToken()
        self._stopevent = threading.Event()
        threading.Thread.__init__(self, name="MergeThread")

    def join(self, timeout=None):
        self.pipe.join_ffmpeg_subprocess()
        threading.Thread.join(self, timeout)

    def kill(self):
        self.alive = False
        self.pipe.kill_thread()
        self.cancel_token.cancel()
        self._stopevent.set()

    def set_start_frame(self, start_frame):
        self.start_frame = start_frame

    @staticmethod
    def make_merge_image(context: Context, frame_residual: Frame, frame_previous: Frame,
                         list_predictive: list, list_residual: list, list_corrections: list, list_fade: list):
        """
        This section can best be explained through pictures. A visual way of expressing what 'merging'
        is doing is this section in the wiki.

        https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works#part-2-using-observations-to-save-time

        Inputs:
            - frame(x)
            - frame(x+1)_residual
            - Residual vectors mapping frame(x+1)_residual -> frame(x+1)
            - Predictive vectors mapping frame(x) -> frame(x+1)

        Output:
            - frame(x+1)
        """

        # Load context
        logger = logging.getLogger(__name__)

        out_image = Frame()
        out_image.create_new(frame_previous.width, frame_previous.height)

        # If list_predictive is empty, then the residual frame is simply the newly
        # produced image.
        if not list_predictive:
            out_image.copy_image(frame_residual)
            return out_image

        # By copying the image first as the first step, all the predictive elements of the form (x,y) -> (x,y)
        # are also copied. This allows us to ignore copying vectors (x,y) -> (x,y), which prevents redundant copying,
        # thus saving valuable computational time.
        out_image.copy_image(frame_previous)

        ###################
        # Plugins Section #
        ###################

        # Note: Run the plugins in the SAME order it was ran in dandere2x_cpp. If not, it won't work correctly.
        out_image = pframe_image(context, out_image, frame_previous, frame_residual, list_residual, list_predictive)
        out_image = fade_image(context, out_image, list_fade)
        out_image = correct_image(context, out_image, list_corrections)

        return out_image

    def run(self):

        self.pipe.start_pipe_thread()
        # Load the genesis image + the first upscaled image.
        frame_previous = Frame()
        frame_previous.load_from_string_wait(self.merged_dir + "merged_" + str(self.start_frame) + self.extension_type,
                                             self.cancel_token)

        self.pipe.save(frame_previous)

        f1 = Frame()
        f1.load_from_string_wait(self.upscaled_dir + "output_" + get_lexicon_value(6, self.start_frame) + ".png",
                                 self.cancel_token)

        last_frame = False
        for x in range(self.start_frame, self.frame_count):

            ###################################
            # Loop-iteration pre-requirements #
            ###################################

            # Check if we're at the last image, which affects the behaviour of the loop.
            if x == self.frame_count - 1:
                last_frame = True

            # Pre-load the next iteration of the loop image ahead of time, if we're not on the last frame.
            if not last_frame:
                background_frame_load = AsyncFrameRead(
                    self.upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png",
                    self.cancel_token)
                background_frame_load.start()

            #######################
            # Loop-iteration Core #
            #######################

            # Load the needed vectors to create the merged image.
            prediction_data_list = get_list_from_file_wait(self.pframe_data_dir + "pframe_" + str(x) + ".txt",
                                                           self.cancel_token)
            residual_data_list = get_list_from_file_wait(self.residual_data_dir + "residual_" + str(x) + ".txt",
                                                         self.cancel_token)
            correction_data_list = get_list_from_file_wait(self.correction_data_dir + "correction_" + str(x) + ".txt",
                                                           self.cancel_token)
            fade_data_list = get_list_from_file_wait(self.fade_data_dir + "fade_" + str(x) + ".txt",
                                                     self.cancel_token)

            if not self.alive:
                self.logger.info("Merge.py killed at frame " + str(x))
                return

            self.logger.info("Upscaling frame " + str(x))
            # Create the actual image itself.
            frame_next = self.make_merge_image(self.context, f1, frame_previous,
                                               prediction_data_list, residual_data_list,
                                               correction_data_list, fade_data_list)

            ###############
            # Saving Area #
            ###############

            # Directly write the image to the ffmpeg pipe line.
            self.pipe.save(frame_next)

            # Manually write the image if we're preserving frames (this is for enthusiasts / debugging).
            if self.preserve_frames:
                output_file = self.workspace + "merged/merged_" + str(x + 1) + self.extension_type
                background_frame_write = AsyncFrameWrite(frame_next, output_file)
                background_frame_write.start()

            #######################################
            # Assign variables for next iteration #
            #######################################

            # last_frame + 1 does not exist, so don't load.
            if not last_frame:
                # We need to wait until the next upscaled image exists before we move on.
                while not background_frame_load.load_complete:
                    wait_on_file(self.upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png",
                                 self.cancel_token)

                f1 = background_frame_load.loaded_image

            frame_previous = frame_next

            # Signal to the rest of the dandere2x process we've finished upscaling frame 'x'.
            self.context.signal_merged_count = x

        self.pipe.wait_finish_stop_pipe()

        # need to migrate tracks, but not in merge.


# For debugging
def main():
    pass


if __name__ == "__main__":
    main()
