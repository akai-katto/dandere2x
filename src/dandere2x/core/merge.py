#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This file is part of the Dandere2x project.
    Dandere2x is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Dandere2x is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Dandere2x.  If not, see <https://www.gnu.org/licenses/>.
""""""
========= Copyright aka_katto 2018, All rights reserved. ============
Original Author: aka_katto 
Purpose: This class / thread is responsible for turning 'residual' 
         images into complete images by using the upscaled images
         and previous frames.
         
         An added responsibility of this class is to directly save
         the finished images into a 'finished' (no audio migrations)
         video, which is done by using the pipe class to pipe frames
         into ffmpeg. 
         
Comments / Notes: This is probably the most difficult to understand
                  dandere2x method due to it's overloaded nature, 
                  since it needs to do the most heavy lifting in 
                  dandere2x as well as needing to deal with the most
                  optimizations. I highly recommend having 
                  `make_merge_image` open when trying to underfirestand 
                  this method to supplement the confusing nature 
====================================================================="""
import logging
import threading

from dandere2x.dandere2x_service.dandere2x_service_context import Dandere2xServiceContext
from dandere2x.dandere2x_service.dandere2x_service_controller import Dandere2xController
from dandere2x.core.residual_plugins.pframe import pframe_image
from dandere2x.dandere2xlib.utils.dandere2x_utils import get_lexicon_value, get_list_from_file_and_wait, wait_on_file
from dandere2x.dandere2xlib.wrappers.ffmpeg.pipe_thread import Pipe
from dandere2x.dandere2xlib.wrappers.frame.asyncframe import AsyncFrameRead
from dandere2x.dandere2xlib.wrappers.frame.frame import Frame


class Merge(threading.Thread):
    """
    Description:
        - This class is the driver for merging all the files that need to be merged together.
          Essentially, it calls the 'make_merge_image' method for every image that needs to be upscaled.
        - Other tasks are to ensure the files exist, async writing for optimizations, as well
          as signalling to other parts of Dandere2x we've finished upscaling.
    """

    def __init__(self, context: Dandere2xServiceContext, controller: Dandere2xController):
        # Threading Specific
        threading.Thread.__init__(self, name="MergeThread")

        self.context = context
        self.controller = controller
        # load variables from context
        self.log = logging.getLogger(name=context.service_request.input_file)

        # setup the pipe for merging
        self.pipe = Pipe(self.context.service_request.output_file, context=context, controller=controller)

    def join(self, timeout=None):
        self.log.info("Join called.")
        self.pipe.join()
        threading.Thread.join(self, timeout)
        self.log.info("Join finished.")

    def run(self):
        self.log.info("Started")
        self.pipe.start()

        # Load the genesis image + the first upscaled image.
        frame_previous = Frame()
        frame_previous.load_from_string_controller(
            self.context.merged_dir + "merged_" + str(1) + ".jpg",
            self.controller)

        # Load and pipe the 'first' image before we start the for loop procedure, since all the other images will
        # inductively build off this first frame.
        frame_previous = Frame()
        frame_previous.load_from_string_controller(
            self.context.merged_dir + "merged_" + str(1) + ".jpg", self.controller)
        self.pipe.save(frame_previous)

        current_upscaled_residuals = Frame()
        current_upscaled_residuals.load_from_string_controller(
            self.context.residual_upscaled_dir + "output_" + get_lexicon_value(6, 1) + ".png",
            self.controller)

        last_frame = False
        for x in range(1, self.context.frame_count):
            ########################################
            # Pre-loop logic checks and conditions #
            ########################################

            # Check if we're at the last image, which affects the behaviour of the loop.
            if x == self.context.frame_count - 1:
                last_frame = True

            # Pre-load the next iteration of the loop image ahead of time, if we're not on the last frame.
            if not last_frame:
                """ 
                By asynchronously loading frames ahead of time, this provides a small but meaningful
                boost in performance when spanned over N frames. There's some code over head but 
                it's well worth it. 
                """
                background_frame_load = AsyncFrameRead(
                    self.context.residual_upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png",
                    self.controller)
                background_frame_load.start()

            ######################
            # Core Logic of Loop #
            ######################

            # Load the needed vectors to create the merged image.

            prediction_data_list = get_list_from_file_and_wait(
                self.context.pframe_data_dir + "pframe_" + str(x) + ".txt",
                self.controller)
            residual_data_list = get_list_from_file_and_wait(
                self.context.residual_data_dir + "residual_" + str(x) + ".txt",
                self.controller)
            correction_data_list = get_list_from_file_and_wait(
                self.context.correction_data_dir + "correction_" + str(x) + ".txt",
                self.controller)
            fade_data_list = get_list_from_file_and_wait(self.context.fade_data_dir + "fade_" + str(x) + ".txt",
                                                         self.controller)

            # Create the actual image itself.
            current_frame = self.make_merge_image(self.context, current_upscaled_residuals, frame_previous,
                                                  prediction_data_list, residual_data_list, correction_data_list,
                                                  fade_data_list)
            ###############
            # Saving Area #
            ###############
            # Directly write the image to the ffmpeg pipe line.
            self.pipe.save(current_frame)

            # Manually write the image if we're preserving frames (this is for enthusiasts / debugging).
            # if self.preserve_frames:
            # if True:
            #     output_file = self.context.merged_dir + "merged_" + str(x + 1) + ".jpg"
            #     background_frame_write = AsyncFrameWrite(current_frame, output_file)
            #     background_frame_write.start()

            #######################################
            # Assign variables for next iteration #
            #######################################
            if not last_frame:
                # We need to wait until the next upscaled image exists before we move on.
                while not background_frame_load.load_complete:
                    wait_on_file(self.context.residual_upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png",
                                 self.controller)

            """
            Now that we're all done with the current frame, the current `current_frame` is now the frame_previous
            (with respect to the next iteration). We could obviously manually load frame_previous = Frame(n-1) each
            time, but this is an optimization that makes a substantial difference over N frames.
            """
            frame_previous = current_frame
            current_upscaled_residuals = background_frame_load.loaded_image
            self.controller.update_frame_count(x)

        self.pipe.kill()

    @staticmethod
    def make_merge_image(context: Dandere2xServiceContext, frame_residual: Frame, frame_previous: Frame,
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
        out_image = Frame()
        out_image.create_new(frame_previous.width, frame_previous.height)

        # If list_predictive is empty, then the residual frame is simply the newly produced image.
        if not list_predictive:
            out_image.copy_image(frame_residual)
            return out_image

        """
        By copying the image first as the first step, all the predictive elements of the form (x,y) -> (x,y)
        are also copied. This allows us to ignore copying vectors (x,y) -> (x,y), which prevents redundant copying,
        thus saving valuable computational time.
        """
        out_image.copy_image(frame_previous)

        ###################
        # Plugins Section #
        ###################

        # Note: Run the residual_plugins in the SAME order it was ran in dandere2x_cpp. If not, it won't work correctly.
        out_image = pframe_image(context, out_image, frame_previous, frame_residual, list_residual, list_predictive)
        # out_image = fade_image(context, out_image, list_fade)
        # out_image = correct_image(context, out_image, list_corrections)

        return out_image

    def set_start_frame(self, start_frame):
        self.start_frame = start_frame


# For debugging
def main():
    pass


if __name__ == "__main__":
    main()
