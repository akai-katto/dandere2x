
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
Purpose: A set of functions to perform Mean Squared Error (MSE)
         computations.
===================================================================== */


#ifndef CPP_REWORK_MSE_FUNCTION_H
#define CPP_REWORK_MSE_FUNCTION_H

#include "../frame/Frame.h"
#include "AbstractEvaluator.h"

class MSE_FUNCTIONS : public AbstractEvaluator {

public:

    static inline int square(const Frame::Color &color_a, const Frame::Color &color_b);

    static double compute_mse(const Frame &image_a, const Frame &image_b,
                              int initial_x, int initial_y,
                              int variable_x, int variable_y, int block_size);

protected:
    bool evaluate_implementation(const Frame &current_frame,
                                 const Frame &next_frame,
                                 const Frame &next_frame_compressed,
                                 int current_frame_x, int current_frame_y,
                                 int next_frame_x, int next_frame_y,
                                 int block_size) override;

};

#endif //CPP_REWORK_MSE_FUNCTION_H
