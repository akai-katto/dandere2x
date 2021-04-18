
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

#include "MSE_Function.h"

//-----------------------------------------------------------------------------
// Purpose: A simple square function which calculuates the "distance" or loss
//          between two colors.
//-----------------------------------------------------------------------------
bool MSE_FUNCTIONS::evaluate_implementation(const Frame &current_frame,
                                            const Frame &next_frame,
                                            const Frame &next_frame_compressed,
                                            const int current_frame_x, const int current_frame_y,
                                            const int next_frame_x, const int next_frame_y, const int block_size) {

    // todo: There's an unexpected (but working) behaviour that, while i'm passing the below arguments in
    // in reverse, (see how next_frame and current_frame_x are swapped), it preferoms correctly and well.
    // I'm not sure the origin of this bug, and suspect it may occur at a higher call, but chasing it down has
    // proven not fruitful. Please fix this when I get the time.
    double image_1_image_2_mse = MSE_FUNCTIONS::compute_mse_lab(next_frame, current_frame,
                                                                current_frame_x, current_frame_y, next_frame_x,
                                                                next_frame_y,
                                                                block_size);

    double image_2_image_2_compressed_mse = MSE_FUNCTIONS::compute_mse_lab(next_frame, next_frame_compressed,
                                                                           next_frame_x, next_frame_y, next_frame_x,
                                                                           next_frame_y,
                                                                           block_size);


    if (image_1_image_2_mse <= image_2_image_2_compressed_mse) {
        return true;
    }

    return false;
}

//-----------------------------------------------------------------------------
// Purpose: A simple square function which calculuates the "distance" or loss
//          between two colors.
//-----------------------------------------------------------------------------
int MSE_FUNCTIONS::square(const Frame::Color &color_a, const Frame::Color &color_b) {

    int r1 = (int) color_a.r;
    int r2 = (int) color_b.r;
    int g1 = (int) color_a.g;
    int g2 = (int) color_b.g;
    int b1 = (int) color_a.b;
    int b2 = (int) color_b.b;

    // Developer Note: We're using multiplication here and addition rather than POW
    // to avoid having to work with doubles for computational improvements.
    return (r2 - r1) * (r2 - r1) + (g2 - g1) * (g2 - g1) + (b2 - b1) * (b2 - b1);
}

double MSE_FUNCTIONS::compute_mse(const Frame &image_a, const Frame &image_b,
                                  const int image_a_x_start, const int image_a_y_start,
                                  const int image_b_x_start, const int image_b_y_start, const int block_size) {

    // Return a really large MSE if the two images are out of bounds (this is also to avoid causing 'sanity check'
    // within Frame from exiting the program).
    if (image_a.block_out_of_bounds(image_a_x_start, image_a_y_start, block_size) ||
        image_b.block_out_of_bounds(image_b_x_start, image_b_y_start, block_size))
        return 9999;

    // Compute the mse
    double sum = 0;
    for (int x = 0; x < block_size; x++)
        for (int y = 0; y < block_size; y++) {
            sum += square(image_a.get_color(image_a_x_start + x, image_a_y_start + y),
                          image_b.get_color(image_b_x_start + x, image_b_y_start + y));
        }
    sum /= block_size * block_size;

    return sum;
}


//-----------------------------------------------------------------------------
// Purpose: Compute MSE (Mean Squared Error) between two images at two different
//          blocks in their respective images. If the block is out of bounds,
//          returns INT_MAX (i.e, is the worst MSE possible)
//-----------------------------------------------------------------------------
double MSE_FUNCTIONS::compute_mse_lab(const Frame &image_a, const Frame &image_b,
                                      int initial_x, int initial_y,
                                      int variable_x, int variable_y, int block_size) {

    // Return a really large MSE if the two images are out of bounds (this is also to avoid causing 'sanity check'
    // within Frame from exiting the program).
    if (image_a.block_out_of_bounds(initial_x, initial_y, block_size) ||
        image_b.block_out_of_bounds(variable_x, variable_y, block_size))
        return 9999;

    // Compute the mse
    double sum = 0;
    for (int x = 0; x < block_size; x++){
        for (int y = 0; y < block_size; y++) {

            auto image_a_color = image_a.get_color(initial_x + x, initial_y + y);
            auto image_b_color = image_b.get_color(variable_x + x, variable_y + y);

            sum += RGB2LAB(image_a_color.r, image_a_color.g, image_a_color.b,
                           image_b_color.r, image_b_color.g, image_b_color.b);
        }
    }
    sum /= block_size * block_size;

    return sum;
}

double MSE_FUNCTIONS::RGB2LAB(int R_value, int G_value, int B_value, int R_value2, int G_value2, int B_value2) {

    double RGB[3];
    double XYZ[3];
    double Lab[3];
    double RGB2[3];
    double XYZ2[3];
    double Lab2[3];
    double adapt[3];
    double value;

    double trans[3];
	double transf[3];
	double newXYZ[3];
	double newRGB[3];

    //maybe change to global, XYZ[0] = X_value

    adapt[0] = 0.950467;
    adapt[1] = 1.000000;
    adapt[2] = 1.088969;

    RGB[0] = R_value * 0.003922;
    RGB[1] = G_value * 0.003922;
    RGB[2] = B_value * 0.003922;

    XYZ[0] = 0.412424 * RGB[0] + 0.357579 * RGB[1] + 0.180464 * RGB[2];
    XYZ[1] = 0.212656 * RGB[0] + 0.715158 * RGB[1] + 0.0721856 * RGB[2];
    XYZ[2] = 0.0193324 * RGB[0] + 0.119193 * RGB[1] + 0.950444 * RGB[2];

    Lab[0] = 116 * H(XYZ[1] / adapt[1]) - 16;
    Lab[1] = 500 * (H(XYZ[0] / adapt[0]) - H(XYZ[1] / adapt[1]));
    Lab[2] = 200 * (H(XYZ[1] / adapt[1]) - H(XYZ[2] / adapt[2]));

    RGB2[0] = R_value2 * 0.003922;
    RGB2[1] = G_value2 * 0.003922;
    RGB2[2] = B_value2 * 0.003922;

    XYZ2[0] = 0.412424 * RGB2[0] + 0.357579 * RGB2[1] + 0.180464 * RGB2[2];
    XYZ2[1] = 0.212656 * RGB2[0] + 0.715158 * RGB2[1] + 0.0721856 * RGB2[2];
    XYZ2[2] = 0.0193324 * RGB2[0] + 0.119193 * RGB2[1] + 0.950444 * RGB2[2];

    Lab2[0] = 116 * H(XYZ2[1] / adapt[1]) - 16;
    Lab2[1] = 500 * (H(XYZ2[0] / adapt[0]) - H(XYZ2[1] / adapt[1]));
    Lab2[2] = 200 * (H(XYZ2[1] / adapt[1]) - H(XYZ2[2] / adapt[2]));

    if ( Lab2[0] > 903.3*0.008856 )
        trans[1] = pow ( (Lab2[0]+16)*0.00862, 3);
    else
        trans[1] = Lab2[0] * 0.001107;

    if ( trans[1] > 0.008856 )
        transf[1] = (Lab2[0]+16)*0.00862;
    else
        transf[1] = (903.3*trans[1]+16)*0.00862;

    transf[0] = Lab2[1] * 0.002 + transf[1];
    transf[2] = transf[1] - Lab2[2] * 0.005;

    if ( pow( transf[0], 3 ) > 0.008856 )
        trans[0] = pow( transf[0], 3 );
    else
        trans[0] =  ((116 * transf[0]) - 16) * 0.001107;

    if ( pow( transf[2], 3 ) > 0.008856 )
        trans[2] = pow( transf[2], 3 );
    else
        trans[2] =  ((116 * transf[2]) - 16) * 0.001107;

    newXYZ[0] = trans[0] * adapt[0];
    newXYZ[1] = trans[1] * adapt[1];
    newXYZ[2] = trans[2] * adapt[2];

    newRGB[0] = 3.24071 * newXYZ[0] + (-1.53726) * newXYZ[1] + (-0.498571) * newXYZ[2];
    newRGB[1] = (-0.969258) * newXYZ[0] + 1.87599 * newXYZ[1] + 0.0415557 * newXYZ[2];
    newRGB[2] = 0.0556352 * newXYZ[0] + (-0.203996) * newXYZ[1] + 1.05707 * newXYZ[2];

    newRGB[0] *= 255;
    newRGB[1] *= 255;
    newRGB[2] *= 255;

    //printf("r=%f g=%f b=%f nr=%f ng=%f nb=%f\n",Lab[0],Lab[1],Lab[2],Lab2[0],Lab2[1],Lab2[2]);

    value = pow((Lab[0] - Lab2[0]), 2) + pow((Lab[1] - Lab2[1]), 2) + pow((Lab[2] - Lab2[2]), 2);
    return value;
}

double MSE_FUNCTIONS::H(double q) {
    double value;
    if ( q > 0.008856 ) {
        value = pow ( q, 0.333333 );
        return value;
    }
    else {
        value = 7.787*q + 0.137931;
        return value;
    }
}


