
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
#include "AbstractPlugin.h"
#include "../frame/Frame.h"
#include "block_plugins/Block.h"
#include "../evaluator/AbstractEvaluator.h"
#include "block_plugins/block_matching/AbstractBlockMatch.h"

using namespace std;
class PredictiveFrame : AbstractPlugin {
public:
    PredictiveFrame(AbstractEvaluator *eval,
                    AbstractBlockMatch *block_matcher,
                    shared_ptr<Frame> current_frame,
                    const shared_ptr<Frame>& next_frame,
                    const shared_ptr<Frame>& next_frame_compressed,
                    const int block_size) : AbstractPlugin(move(current_frame),
                                                     next_frame,
                                                     next_frame_compressed,
                                                     block_size){
        this->eval = eval;
        this->block_matcher = block_matcher;
    }

    void run() override;

    void write(const string &output_file) override;

protected:

    void update_frame() override;


private:

    void parallel_function_call(int x, int y) override;

    vector<Block> matched_blocks;
    AbstractEvaluator *eval;
    AbstractBlockMatch *block_matcher;

};


#endif //CPP_REWORK_PREDICTIVEFRAME_H
