//
// Created by owo on 3/1/20.
//

#ifndef DANDERE2X_CPP_SSIM_H
#define DANDERE2X_CPP_SSIM_H

#include "../Image/Image.h"

class SSIM {

public:
    static int getLumaColor(Image::Color &col, char color) {

        switch(color){
            case 'r':
                return col.r;
                break;
            case 'g':
                return col.g;
                break;
            case 'b':
                return col.b;
                break;
        }
        //return col.r * (double) 0.212655 + col.g * (double) 0.715158 + (double) 0.072187 * col.b;
    }

    static double averageLuma(Image &image, int initial_x, int initial_y, int block_size, char color) {

        double sum = 0;

        for (int x = 0; x < block_size; x++) {
            for (int y = 0; y < block_size; y++) {
                sum += getLumaColor(image.get_color(initial_x + x, initial_y + y), color);
            }
        }

        sum /= block_size * block_size;
        return sum;
    }

    static double ssim(Image &image_A, Image &image_B,
                       int initial_x, int initial_y,
                       int variable_x, int variable_y,
                       int block_size){
        double r = ssim_color(image_A, image_B, initial_x, initial_y, variable_x, variable_y, block_size, 'r');
        double g = ssim_color(image_A, image_B, initial_x, initial_y, variable_x, variable_y, block_size, 'g');
        double b = ssim_color(image_A, image_B, initial_x, initial_y, variable_x, variable_y, block_size, 'b');

        return (r + g + b) / 3;
    }

    static double ssim_color(Image &image_A, Image &image_B,
                             int initial_x, int initial_y,
                             int variable_x, int variable_y,
                             int block_size, char color) {

        double mx = averageLuma(image_A, initial_x, initial_y, block_size, color);
        double my = averageLuma(image_B, variable_x, variable_y, block_size, color);

        double sigxy = 0;
        double sigsqx = 0;
        double sigsqy = 0;
        double mse = 0;

        for (int x = 0; x < block_size; x++) {
            for (int y = 0; y < block_size; y++) {
                sigsqx += pow((getLumaColor(image_A.get_color(initial_x + x, initial_y + y), color) - mx), 2);
                sigsqy += pow((getLumaColor(image_B.get_color(variable_x + x, variable_y + y), color) - my), 2);
                mse += pow((getLumaColor(image_A.get_color(initial_x + x, initial_y + y), color))
                           - (getLumaColor(image_B.get_color(initial_x + x, initial_y + y), color)), 2);

                sigxy += (getLumaColor(image_A.get_color(initial_x + x, initial_y + y), color) - mx) * (getLumaColor(image_B.get_color(variable_x + x, variable_y + y), color) - my);
            }
        }

        double numPixelsInWin = block_size * block_size;

        sigsqx /= numPixelsInWin;
        sigsqy /= numPixelsInWin;
        sigxy /= numPixelsInWin;

        double c1 = pow((0.01 * 255), 2);
        double c2 = pow((0.03 * 255), 2);

        double numerator = (2 * mx * my + c1) * (2 * sigxy + c2);
        double denominator = (pow(mx, 2) + pow(my, 2) + c1) * (sigsqx + sigsqy + c2);

        double ssim = numerator / denominator;

        // Variables used to stabalize a weak (or zero) denominator (similar to c1 c2 in SSIM)
        double d1 = pow(0.01 * (255*255), 2);
        double d2 = pow(0.03 * (255*255), 2);

        double inverse_mse = (1 + d1) / (mse + d2);

        return ssim * inverse_mse;
    }
};


#endif //DANDERE2X_CPP_SSIM_H