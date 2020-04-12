
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
Purpose: 
 
===================================================================== */


#include <iostream>
#include <cmath>
#include "SSIM_Function.h"

//------------------------------------------------------------------------------------------
// Purpose: Use the SSIM Formula (implementation described in the header file's description).
//
// Notes:
//       - Returns -1 if illegal / out of bounds arguments
//         ( -1 isn't a possible value for SSIM's potential outputs)
//------------------------------------------------------------------------------------------
double SSIM_Function::compute_ssim_color(const Frame& image_a, const Frame& image_b,
                                         const int image_a_x_start, const int image_a_y_start,
                                         const int image_b_x_start, const  int image_b_y_start,
                                         const int block_size, const SSIM_Function::RGB rgb_component) {

    // Invalid argument condition
    if (image_a.block_within_bounds(image_a_x_start, image_a_y_start, block_size) ||
        image_b.block_within_bounds(image_b_x_start, image_b_y_start, block_size))
        return -1;

    double mx = compute_average_color(image_a, image_a_x_start, image_a_y_start, block_size, rgb_component);
    double my = compute_average_color(image_b, image_b_x_start, image_b_y_start, block_size, rgb_component);

    double sigxy = 0;
    double sigsqx = 0;
    double sigsqy = 0;

    for (int x = 0; x < block_size; x++) {
        for (int y = 0; y < block_size; y++) {
            sigsqx += pow((get_rgb_from_color(image_a.get_color(image_a_x_start + x, image_a_y_start + y), rgb_component) - mx), 2);
            sigsqy += pow((get_rgb_from_color(image_b.get_color(image_b_x_start + x, image_b_y_start + y), rgb_component) - my), 2);

            sigxy += (get_rgb_from_color(image_a.get_color(image_a_x_start + x, image_a_y_start + y), rgb_component) - mx) *
                     (get_rgb_from_color(image_b.get_color(image_b_x_start + x, image_b_y_start + y), rgb_component) - my);
        }
    }

    double total_nunber_of_pixels = block_size * block_size;

    sigsqx /= total_nunber_of_pixels;
    sigsqy /= total_nunber_of_pixels;
    sigxy /= total_nunber_of_pixels;

    double c1 = pow((0.01 * 255), 2);
    double c2 = pow((0.03 * 255), 2);

    double numerator = (2 * mx * my + c1) * (2 * sigxy + c2);
    double denominator = (pow(mx, 2) + pow(my, 2) + c1) * (sigsqx + sigsqy + c2);

    double ssim = numerator / denominator;
    return ssim;
}


//-----------------------------------------------------------------------------
// Purpose: Compute the average color (aka luma) of a block.
//-----------------------------------------------------------------------------
double SSIM_Function::compute_average_color(const Frame& image, const int start_x, const int start_y, const int block_size,
                                            SSIM_Function::RGB rgb_component) {

    double sum = 0;
    for (int x = 0; x < block_size; x++)
        for (int y = 0; y < block_size; y++)
            sum += get_rgb_from_color(image.get_color(start_x + x, start_y + y), rgb_component);

    sum /= block_size * block_size;
    return sum;
}

//-----------------------------------------------------------------------------
// Purpose: Extract a color component from a color.
//-----------------------------------------------------------------------------
char SSIM_Function::get_rgb_from_color(const Frame::Color& col, const SSIM_Function::RGB rgb_component) {

    switch(rgb_component){
        case 'r':
            return col.r;
        case 'g':
            return col.g;
        case 'b':
            return col.b;
    }

    cerr << "Invalid rgb_component requested from SSIM_Function::get_rgb_from_color: " << rgb_component << endl;
    exit(1);
}