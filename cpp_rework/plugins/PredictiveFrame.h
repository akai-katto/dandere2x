
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
#import "AbstractPlugin.h"
#import "../frame/Frame.h"

using namespace std;
class PredictiveFrame : AbstractPlugin {
public:
    PredictiveFrame(shared_ptr<Frame> frame1, shared_ptr<Frame> frame2, shared_ptr<Frame> frame_compressed,
                    int block_size, string predictive_frame_file_output, string residual_file_output, int step_size = 4);

private:
    // constructor variables
    shared_ptr<Frame> frame1;
    shared_ptr<Frame> frame2;
    shared_ptr<Frame> frame2_compressed;
    string predictive_frame_file_output;
    string residual_file_output;
    int step_size = 4;



};


#endif //CPP_REWORK_PREDICTIVEFRAME_H
