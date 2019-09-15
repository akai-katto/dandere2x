//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_CPP_SSIMSTATSFUNCTIONS_H
#define DANDERE2X_CPP_SSIMSTATSFUNCTIONS_H


#include "../Image/Image.h"
#include "../Image/ImageUtils.h"

class StatFunctions {
public:

    inline static double get_component_from_color(Image::Color color_A, char color) {

        switch (color) {
            case 'r':
                return (int) color_A.r;
            case 'g':
                return (int) color_A.g;
            case 'b':
                return (int) color_A.b;
            default:
                printf("Invalid input for get_component_from_color");
                exit(1);
        }
    }

    inline static double mean_block(Image &image_A,
                                    int initial_x, int initial_y,
                                    int block_size, char color) {

        double sum = 0;

        for (int x = 0; x < block_size; x++)
            for (int y = 0; y < block_size; y++)
                sum += get_component_from_color(image_A.get_color(initial_x + x, initial_y + y), color);

        sum /= block_size * block_size;
        return sum;
    }

    inline static double variance_block(Image &image_A,
                                        int initial_x, int initial_y,
                                        int block_size, char color) {


        double mean = mean_block(image_A, initial_x, initial_y, block_size, color);

        double variance = 0;

        for (int x = 0; x < block_size; x++) {
            for (int y = 0; y < block_size; y++) {
                variance += pow(get_component_from_color(image_A.get_color(initial_x + x, initial_y + y), color) - mean,
                                2);

            }
        }
        variance /= (block_size * block_size - 1);
        variance = pow(variance, .5);
        return variance;
    }

    inline static double covariance(Image &image_A, Image &image_B,
                                    int initial_x, int initial_y,
                                    int variable_x, int variable_y,
                                    int block_size, char color) {

        double mean_A = mean_block(image_A, initial_x, initial_y, block_size, color);
        double mean_B = mean_block(image_B, variable_x, variable_y, block_size, color);

        double covariance = 0;

        for (int x = 0; x < block_size; x++) {
            for (int y = 0; y < block_size; y++) {
                covariance +=
                        (get_component_from_color(image_A.get_color(initial_x + x, initial_y + y), color) - mean_A) *
                        (get_component_from_color(image_B.get_color(variable_x + x, variable_y + y), color) - mean_B);

            }
        }
        covariance /= (block_size * block_size - 1);
        return covariance;
    }

    inline static double ssim(Image &image_A, Image &image_B,
                              int initial_x, int initial_y,
                              int variable_x, int variable_y,
                              int block_size, char color) {

        double ssim = 0;

        double mean_a = mean_block(image_A, initial_x, initial_y, block_size, color);
        double mean_b = mean_block(image_B, variable_x, variable_y, block_size, color);

        double var_a = variance_block(image_A, initial_x, initial_y, block_size, color);
        double var_b = variance_block(image_B, variable_x, variable_y, block_size, color);
        double covar_ab = covariance(image_A, image_B, initial_x, initial_y, variable_x, variable_y, block_size, color);

        double c1 = (0.01 * 255);
        double c2 = (0.03 * 255);


        ssim = ((2 * mean_a * mean_b + c1) * (2 * covar_ab + c2))
               /
               ((mean_a * mean_a + mean_b * mean_b + c1) * (var_a * var_a + var_b * var_b + c2));
        return ssim;
    }


};

#endif //DANDERE2X_CPP_SSIMSTATSFUNCTIONS_H
