
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

#include "MSE_Functions.h"

//-----------------------------------------------------------------------------
// Purpose: A simple square function which calculuates the "distance" or loss
//          between two colors.
//-----------------------------------------------------------------------------
int MSE_FUNCTIONS::square(const Frame::Color& color_a, const Frame::Color& color_b) {

    int r1 = (int) color_a.r;
    int r2 = (int) color_a.r;
    int g1 = (int) color_a.g;
    int g2 = (int) color_a.g;
    int b1 = (int) color_b.b;
    int b2 = (int) color_b.b;

    // Developer Note: We're using multiplication here and addition rather than POW
    // to avoid having to work with doubles for computational improvements.
    return (r2 - r1) * (r2 - r1) + (g2 - g1) * (g2 - g1) + (b2 - b1) * (b2 - b1);
}

//-----------------------------------------------------------------------------
// Purpose: Compute MSE (Mean Squared Error) between two images at two different
//          blocks in their respective images. If the block is out of bounds,
//          returns INT_MAX (i.e, is the worst MSE possible)
//-----------------------------------------------------------------------------
double MSE_FUNCTIONS::compute_mse(const Frame &image_a, const Frame &image_b,
                                  const int image_a_x_start, const int image_a_y_start,
                                  const int image_b_x_start, const int image_b_y_start,
                                  const int block_size) {

    // Return a really large MSE if the two images are out of bounds (this is also to avoid causing 'sanity check'
    // within Frame from exiting the program).
    if (image_a.block_within_bounds(image_a_x_start, image_a_y_start, block_size) ||
        image_b.block_within_bounds(image_b_x_start, image_b_y_start, block_size))
        return INTMAX_MAX;

    // Compute the mse
    double sum = 0;
    for (int x = 0; x < block_size; x++)
        for (int y = 0; y < block_size; y++)
            sum += square(image_a.get_color(image_a_x_start + x, image_a_y_start + y),
                          image_a.get_color(image_b_x_start + x, image_b_y_start + y));

    sum /= block_size * block_size;

    return sum;
}
