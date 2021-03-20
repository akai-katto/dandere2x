
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
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
*/

/* 
========= Copyright aka_katto 2018, All rights reserved. ============
Original Author: aka_katto 
Date: 4/11/20 
Purpose: todo
 
===================================================================== */

#include <omp.h>

#include "PredictiveFrame.h"


// remove
#include "../evaluator/MSE_Function.h"
#include "../evaluator/SSIM_Function.h"
#include "../frame/Frame_Utilities.h"

//-----------------------------------------------------------------------------
// Purpose: Match every block using the chosen block_matching algorithm chosen
//          and the chosen evaluation function. This code is intended to be
//          done on multiple cores, hence should work in parallel.
//-----------------------------------------------------------------------------
void PredictiveFrame::parallel_function_call(int x, int y) {

    // check if stationary block match works.
    if (eval->evaluate(this->current_frame,
                       this->next_frame, this->next_frame_compressed,
                       x, y,
                       x, y,
                       block_size)) {

        this->matched_blocks[x][y] = make_shared<Block>(x, y, x, y, 1);

    } else {

        // Look for the block (x,y,block_size) in frame_2, searching for blocks in frame_1.
        Block matched_block = this->block_matcher->match_block(x, y, block_size);

        // Since we're going frame_2 -> frame_1, the matched block is "being matched in reverse", so flip the block
        // so we can go frame_1 -> frame_2.
        matched_block.reverse_block();

        if (eval->evaluate(this->current_frame,
                           this->next_frame, this->next_frame_compressed,
                           matched_block.x_start, matched_block.y_start,
                           matched_block.x_end, matched_block.y_end,
                           block_size)) {
            matched_block_count+=1;
            this->matched_blocks[x][y] = make_shared<Block>(matched_block.x_start, matched_block.y_start,
                                                            matched_block.x_end, matched_block.y_end,
                                                            1);
        }


    }
}


//-----------------------------------------------------------------------------
// Purpose: todo
//-----------------------------------------------------------------------------
void PredictiveFrame::run() {

    int x = 0;
    int y = 0;
    int num_threads = 8;

#pragma omp parallel for shared(current_frame, next_frame, next_frame_compressed, matched_blocks) private(x, y)

    for (x = 0; x < current_frame.get_width() / block_size; x++) {
        for (y = 0; y < current_frame.get_height() / block_size; y++) {
            parallel_function_call(x * block_size, y * block_size);
        }
    }

    update_frame();
}

//-----------------------------------------------------------------------------
// Purpose: todo
//-----------------------------------------------------------------------------
void PredictiveFrame::write(const string &output_file) {

    cout << "matched block count: " << matched_block_count << endl;
    //Frame new_frame = Frame(*this->next_frame);
    Frame new_frame = Frame(next_frame.get_width(), next_frame.get_height(), next_frame.get_bpp());
    FrameUtilities::copy_frame_using_blocks(next_frame,
                                            current_frame,
                                            this->matched_blocks,
                                            this->block_size);
    next_frame.write(output_file);
}

void PredictiveFrame::update_frame() {
    FrameUtilities::copy_frame_using_blocks(next_frame,
                                            current_frame,
                                            this->matched_blocks,
                                            this->block_size);
}
