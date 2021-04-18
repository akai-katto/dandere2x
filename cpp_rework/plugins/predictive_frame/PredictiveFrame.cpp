
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
#include <math.h>
#include <fstream>
#include "PredictiveFrame.h"
#include "../../frame/Frame_Utilities.h"

//-----------------------------------------------------------------------------
// Purpose: Match every block using the chosen block_matching algorithm chosen
//          and the chosen evaluation function. This code is intended to be
//          done on multiple cores, hence should work in parallel.
//-----------------------------------------------------------------------------
void PredictiveFrame::parallel_function_call(int x, int y) {

    // Check if stationary block match works.
    if (eval->evaluate(this->current_frame,
                       this->next_frame, this->next_frame_compressed,
                       x, y,
                       x, y,
                       block_size)) {

        matched_stationary_blocks += 1;
        this->matched_blocks[x][y] = make_shared<Block>(x, y, x, y, 1);
        return;
    }

    // Find (x,y) in frame_2 in frame_1. Note we have to go in the reverse. We can't go frame_1 -> frame_2 since
    // the matched blocks may not be on perfect intervals of block_size.
    // Since we're going frame_2 -> frame_1, the matched block is "being matched in reverse", so flip the block
    // so we can go frame_1 -> frame_2.
    Block matched_block = this->block_matcher->match_block(x, y, block_size);
    matched_block.reverse_block();

    // Check to see if the current matched block produces a valid match
    if (eval->evaluate(this->current_frame,
                       this->next_frame, this->next_frame_compressed,
                       matched_block,
                       block_size)) {

        matched_moving_blocks += 1;
        this->matched_blocks[x][y] = make_shared<Block>(matched_block.x_start, matched_block.y_start,
                                                        matched_block.x_end, matched_block.y_end,
                                                        1);
        return;
    }

    // -1 denotes an invalid block.
    this->matched_blocks[x][y] = make_shared<Block>(x, y,
                                                    x, y,
                                                    -1);
}


//-----------------------------------------------------------------------------
// Purpose: todo
//-----------------------------------------------------------------------------
void PredictiveFrame::run() {

    double psnr = eval->psnr_two_frames(current_frame, next_frame);

    // Don't conduct block matches if the PSNR is terribly low.
    if (psnr < 10) {
        std::cout << "PSNR " << psnr << std::endl;
        std::cout << "PSNR is low - not going to match blocks" << std::endl;
    }
    else{
        match_blocks();
    }

}

//-----------------------------------------------------------------------------
// Purpose: todo
//-----------------------------------------------------------------------------
void PredictiveFrame::match_blocks() {

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
// Purpose: Writes the residuals (i.e the blocks that did not get matched )
//-----------------------------------------------------------------------------
void PredictiveFrame::write(const string &predictive_vectors_output, const string &residual_vectors_output) {
    int max_blocks_possible = (current_frame.get_height() * this->current_frame.get_width()) / (this->block_size * this->block_size);

    if (max_blocks_possible <=
        ((block_size * block_size) * (matched_moving_blocks + matched_stationary_blocks)) / ((block_size + bleed) * (block_size + bleed))) {
        // We decided not to keep any of the blocks.. abandon all the progress we did in this function

        std::cout << "Too many missing blocks - conducting redraw" << std::endl;
        this->write_blocks(predictive_vectors_output, {});
        this->write_blocks(residual_vectors_output, {});
    }
    else{
        write_positive_case(predictive_vectors_output, residual_vectors_output);
        update_frame();
    }
}

void PredictiveFrame::write_positive_case(const string &predictive_vectors_output, const string &residual_vectors_output) {
    // I apologize to myself / any maintainer that this is in a big function, but couldn't find a way to make this
    // split up into a few smaller bits and pieces.

    /**
     * Part 1: Getting the movement vectors.
     *
     * The goal here is to create a series of vectors (literal vectors not c++) mapping the missing blocks of an image,
     * to a new, smaller image in order for the "residuals" of the image to be upscaled independently,
     * then re-patched together.
     *
     * The vectors are then written to a file to be processed by dandere2x_python in order for them to be
     * stitched back together once it's finished.
     */

    cout << "matched moving blocks: " << matched_moving_blocks << endl;
    // Create vectors matching the missing blocks to the residuals image.
    vector<shared_ptr<Block>> missing_blocks = PredictiveFrame::get_missing_blocks(this->matched_blocks);
    vector<shared_ptr<Block>> vector_displacements;

    int missing_blocks_length = missing_blocks.size();
    int dimension = sqrt(missing_blocks_length) + 1; // The dimension of the output image

    // Start cycling through each missing block, giving it an (x,y) coordinate in the new smaller output image.
    for (int x = 0; x < dimension; x++) {
        for (int y = 0; y < dimension; y++) {

            // Break if we pre-maturely finished.
            if (missing_blocks.empty()) {
                break;
            }

            // Create the displacement matching the two images via vectors.
            shared_ptr<Block> current = missing_blocks[0];
            vector_displacements.push_back(make_shared<Block>(current->x_start , current->y_start,
                                                              x, y, 0));
            missing_blocks.erase(missing_blocks.begin(), missing_blocks.begin() + 1);
        }
    }

    /**
     * Part 2: Writing the output files.
     *
     * Now that we have all the necessary data, writing the actual files for dandere2x_python to use (we send them via
     * text files).
     */
    this->write_blocks(predictive_vectors_output, matched_blocks);
    vector<vector<shared_ptr<Block>>> argument_vector = {vector_displacements};
    this->write_blocks(residual_vectors_output, argument_vector); // why is this not writing anything out?
}

//-----------------------------------------------------------------------------
// Purpose: Updates next_frame using the matched blocks found in current_frame.
//          In other words, the blocks found in next_frame that could be
//          made with blocks from current_frame need to be updated.
//-----------------------------------------------------------------------------
void PredictiveFrame::update_frame() {
    FrameUtilities::copy_frame_using_blocks(next_frame,
                                            current_frame,
                                            this->matched_blocks,
                                            this->block_size);
}


void PredictiveFrame::debug_visual(const string &output_image) {
    Frame debug_frame = Frame(current_frame.get_width(), current_frame.get_height(), this->current_frame.get_bpp());
    FrameUtilities::copy_frame_using_blocks(debug_frame,
                                            current_frame,
                                            this->matched_blocks,
                                            this->block_size);
    debug_frame.write(output_image);
}

void PredictiveFrame::debug_predictive(const string &output_image) {
    this->next_frame.write(output_image);
}


//-----------------------------------------------------------------------------
// Purpose: Filters out "matched_blocks" into a single dimensional vector,
//          only including the blocks that were not valid. This function
//          doesn't need to be static but is done so for readability.
//-----------------------------------------------------------------------------
vector<shared_ptr<Block>> PredictiveFrame::get_missing_blocks(const vector<vector<shared_ptr<Block>>> &blocks) {

    vector<shared_ptr<Block>> returned_blocks;
    for (const vector<shared_ptr<Block>> &row: blocks) {
        for (const shared_ptr<Block> &block: row) {
            // todo fix this technical debt, see the issues in "Predictive Frame"
            if (block == nullptr)
                continue;

            if (block->sum == -1) { // -1 denotes an invalid block.
                returned_blocks.push_back(block);
            }
        }
    }

    return returned_blocks;
}



