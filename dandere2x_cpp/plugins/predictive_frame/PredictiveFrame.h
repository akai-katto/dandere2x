
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
Purpose: Given two frames, try to find as many matching blocks between
         them, either by using stationary block matching techniques,
         or by using motion-prediction block matching algorithm.
===================================================================== */


#ifndef CPP_REWORK_PREDICTIVEFRAME_H
#define CPP_REWORK_PREDICTIVEFRAME_H

#include <memory>
#include <utility>
#include "../AbstractPlugin.h"
#include "../../frame/Frame.h"
#include "../block_plugins/Block.h"
#include "../../evaluator/AbstractEvaluator.h"
#include "../block_plugins/block_matching/AbstractBlockMatch.h"

using namespace std;

class PredictiveFrame : public AbstractPlugin {
public:
    PredictiveFrame(AbstractEvaluator *eval,
                    AbstractBlockMatch *block_matcher,
                    shared_ptr<Frame> current_frame,
                    shared_ptr<Frame> next_frame,
                    shared_ptr<Frame> next_frame_compressed,
                    const int block_size,
                    const int bleed) : AbstractPlugin(current_frame,
                                                      next_frame,
                                                      next_frame_compressed, block_size) {
        this->eval = eval;
        this->block_matcher = block_matcher;
        this->bleed = bleed;

        // Due to multiprocessing / multithreading with omp, we need to instantiate the shared vectors before
        // the code starts running.
        // todo, fix this to not use as much memory, we're reserving pointers for each pixel, when each block should
        // be the stuff getting reserved.
        this->matched_blocks.resize(next_frame->get_width(), vector<shared_ptr<Block>>(next_frame->get_height()));

    }

    void run() override;

    void update_frame(shared_ptr<Frame> final_frame) override;

    void write(const string &predictive_vectors_output, const string &residual_vectors_output);

    void debug_visual(const string &output_image);

    void debug_predictive(const string &output_image);

    int missing_pixel_cost();

protected:

    void write_positive_case(const string &predictive_vectors_output, const string &residual_vectors_output);

private:

    void match_blocks();

    void parallel_function_call(int x, int y) override;

    static vector<shared_ptr<Block>> get_missing_blocks(const vector<vector<shared_ptr<Block>>> &blocks);

    vector<vector<shared_ptr<Block>>> matched_blocks;
    AbstractEvaluator *eval;
    AbstractBlockMatch *block_matcher;
    int matched_stationary_blocks = 0;
    int matched_moving_blocks = 0;
    int bleed;
};


#endif //CPP_REWORK_PREDICTIVEFRAME_H
