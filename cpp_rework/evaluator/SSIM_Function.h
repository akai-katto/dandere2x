
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
Purpose: Compute the Structural Similarity Index Metric (SSIM) between
         two images.

Notes:
 - Note sure if this is implemented correctly - needs peer review.
 - Implementation was inspired / modified from this java implementation:
   "SsimCalculator.java" from
   https://github.com/rhys-e/structural-similarity
 - Again, I'm not sure if our implementations are correct or not. The
   outputs greatly differ from the outputs Python's Numpy Library
   gives for SSIM is different from mine.
===================================================================== */


#ifndef CPP_REWORK_SSIM_FUNCTION_H
#define CPP_REWORK_SSIM_FUNCTION_H


#include "../frame/Frame.h"
#include "AbstractEvaluator.h"

class SSIM_Function: public AbstractEvaluator{

public:
    bool evaluate(const Frame &current_frame,
                  const Frame &next_frame,
                  const Frame &current_frame_compressed,
                  int initial_x, int initial_y,
                  int variable_x, int variable_y,
                  int block_size)
                  override;

    static inline double compute_ssim(const Frame& image_a, const Frame& image_b,
                                      int image_a_x_start, int image_a_y_start,
                                      int image_b_x_start, int image_b_y_start,
                                      int block_size);

public:
    // short-handed notation used for class
    using RGB = char; // 'r' == 'red', 'g' == 'green', 'b' == 'blue

    static inline double compute_ssim_color(const Frame& image_a, const Frame& image_b,
                                            int image_a_x_start, int image_a_y_start,
                                            int image_b_x_start, int image_b_y_start,
                                            int block_size, RGB rgb_component);

    static inline double compute_average_color(const Frame &image,
                                               int start_x, int start_y,
                                               int block_size, RGB rgb_component);

    static inline char get_rgb(const Frame::Color &col, const RGB rgb_component);



};


#endif //CPP_REWORK_SSIM_FUNCTION_H
