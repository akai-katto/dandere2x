//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_CPP_SSIM_H
#define DANDERE2X_CPP_SSIM_H

#include "../Image/Image.h"
#include "SsimStatsFunctions.h"


class SSIM {
public:


    inline static double ssim(Image &image_A, Image &image_B,
                              int initial_x, int initial_y,
                              int variable_x, int variable_y,
                              int block_size) {

        //compute the SSIM for all rgb elements
        double ssim_r = StatFunctions::ssim(image_A, image_B, initial_x, initial_y, variable_x, variable_y, block_size,
                                            'r');
        double ssim_g = StatFunctions::ssim(image_A, image_B, initial_x, initial_y, variable_x, variable_y, block_size,
                                            'g');
        double ssim_b = StatFunctions::ssim(image_A, image_B, initial_x, initial_y, variable_x, variable_y, block_size,
                                            'b');

        //return the average of all 3 individually
        return (ssim_r + ssim_g + ssim_b) / 3;
    }


};

#endif //DANDERE2X_CPP_SSIM_H
