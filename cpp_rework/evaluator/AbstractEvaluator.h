
/*
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
*/

/*
========= Copyright akai_katto 2021, All rights reserved. ============
Original Author: akai_katto
Purpose: Dandere2x is built to have multiple evaluators, i.e the user
         can use MSE (mean squared error) or SSIM-MSE (a variation of
         SSIM I wrote that also let's MSE vote.)

         This class allows an evalutor object to be instantiated
         wherein the code can request what evaluation metric they want
         to use, allowing for one code to access both MSE and SSIM-MSE
         evaluation tools.

         As a general rule of thumb, evaluators are passed references,
         while in the rest of code, shared_ptr is passed. This stems
         from that the inner most calls should have as little overhead
         as possible.
===================================================================== */

#ifndef CPP_REWORK_ABSTRACTEVALUATOR_H
#define CPP_REWORK_ABSTRACTEVALUATOR_H

// internal includes
#include <vector>
#include <string>
#include <memory>
#include "../frame/Frame.h"
#include "../plugins/block_plugins/Block.h"

class AbstractEvaluator {

public:


    bool evaluate(const Frame &current_frame,
                  const Frame &next_frame,
                  const Frame &next_frame_compressed,
                  const Block &block,
                  const int block_size) {
        return evaluate(current_frame, next_frame, next_frame_compressed,
                        block.x_start, block.y_start,
                        block.x_end, block.y_end, block_size);
    }


    //-----------------------------------------------------------------------------
    // Any evaluator will have to give a binary "yes the matched block passes the constant-quality check" or
    // "no it doesn't". Since each metric is different (i.e higher number in some means better, lower number means worse)
    // it's left to the implementation to determine what quantifies that a block is matched or not.
    //-----------------------------------------------------------------------------
    bool evaluate(const Frame &current_frame,
                  const Frame &next_frame,
                  const Frame &next_frame_compressed,
                  const int current_frame_x, const int current_frame_y,
                  const int next_frame_x, const int next_frame_y,
                  const int block_size) {

        // primitive sanity check for any evaluation
        if (current_frame.block_out_of_bounds(current_frame_x, current_frame_y, block_size) ||
            current_frame.block_out_of_bounds(next_frame_x, next_frame_y, block_size))
            return false;

        return evaluate_implementation(current_frame, next_frame, next_frame_compressed, current_frame_x,
                                       current_frame_y,
                                       next_frame_x, next_frame_y, block_size);
    }

    // Some handy functions wherever an evaluator is used.
    double psnr_two_frames(const Frame &current_frame, const Frame &next_frame) {
        double sum = 0;

        for (int x = 0; x < current_frame.get_width(); x++) {
            for (int y = 0; y < current_frame.get_height(); y++) {
                sum += square(current_frame.get_color(x, y), next_frame.get_color(x, y));
            }
        }

        sum /= (next_frame.get_height() * next_frame.get_width());

        double result = 20 * log10(255) - 10 * log10(sum);
        return result;
    }

protected:

    virtual bool evaluate_implementation(const Frame &current_frame,
                                         const Frame &next_frame,
                                         const Frame &next_frame_compressed,
                                         const int current_frame_x, const int current_frame_y,
                                         const int next_frame_x, const int next_frame_y,
                                         const int block_size) = 0;

    //-----------------------------------------------------------------------------
    // Purpose: A simple square function which calculuates the "distance" or loss
    //          between two colors.
    //-----------------------------------------------------------------------------
    int square(const Frame::Color &color_a, const Frame::Color &color_b) {

        int r1 = (int) color_a.r;
        int r2 = (int) color_b.r;
        int g1 = (int) color_a.g;
        int g2 = (int) color_b.g;
        int b1 = (int) color_a.b;
        int b2 = (int) color_b.b;

        // Developer Note: We're using multiplication here and addition rather than POW
        // to avoid having to work with doubles for computational improvements.
        return (r2 - r1) * (r2 - r1) + (g2 - g1) * (g2 - g1) + (b2 - b1) * (b2 - b1);
    }

};


#endif //CPP_REWORK_ABSTRACTEVALUATOR_H
