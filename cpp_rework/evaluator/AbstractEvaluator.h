
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


class AbstractEvaluator {

public:

    //-----------------------------------------------------------------------------
    // Any evaluator will have to give a binary "yes the matched block passes the constant-quality check" or
    // "no it doesn't". Since each metric is different (i.e higher number in some means better, lower number means worse)
    // it's left to the implementation to determine what quantifies that a block is matched or not.
    //-----------------------------------------------------------------------------
    bool evaluate(const Frame &current_frame,
                  const Frame &next_frame,
                  const Frame &next_frame_compressed,
                  int initial_x, int initial_y,
                  int variable_x, int variable_y,
                  int block_size) {

        // primitive sanity check for any evaluation
        if (current_frame.block_out_of_bounds(initial_x, initial_y, block_size) ||
            current_frame.block_out_of_bounds(variable_x, variable_y, block_size))
            return false;

        return evaluate_implementation(current_frame, next_frame, next_frame_compressed, initial_x, initial_y,
                                       variable_x, variable_y, block_size);
    }

protected:

    virtual bool evaluate_implementation(const Frame &current_frame,
                                         const Frame &next_frame,
                                         const Frame &next_frame_compressed,
                                         int initial_x, int initial_y,
                                         int variable_x, int variable_y,
                                         int block_size) = 0;

};


#endif //CPP_REWORK_ABSTRACTEVALUATOR_H
