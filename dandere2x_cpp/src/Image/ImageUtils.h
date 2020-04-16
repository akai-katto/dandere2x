//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt



/** I wrote this before I realized namespaces exist. This is essentially a namespace
 *  for functions that show up commonly in various image computations.
 */
#ifndef DANDERE2X_IMAGEUTILS_H
#define DANDERE2X_IMAGEUTILS_H

#include "../Image/Image.h"

class ImageUtils {
public:

    /*
     * Notes on this function:
     *
     * - This is the inner most call. This is called literally a few million times.
     *
     * - I tried to optimize this function by creating a hash / lookup table, but it
     *   seemed to behave slower.
     */
//    inline static double root_square(const Image::Color &color_A, const Image::Color &color_B) {
//
//        int r1 = (int) color_A.r;
//        int r2 = (int) color_B.r;
//
//        int g1 = (int) color_A.g;
//        int g2 = (int) color_B.g;
//
//        int b1 = (int) color_A.b;
//        int b2 = (int) color_B.b;
//
//        return sqrt(pow((r2 - r1), 2) + pow((g2 - g1), 2) + pow((b2 - b1), 2));
//    }


    /*
     * Note on this function:
     *
     * - this is the inner most function call
     *
     * - this is my linear version of root_square, which is just root.
     *
     * - Computationally, this is much faster as an inner most call. Much much faster, and results are
     * the same (experimentally) give or take.
     *
     */

    inline static int square(const Image::Color &color_A, const Image::Color &color_B) {

        int r1 = (int) color_A.r;
        int r2 = (int) color_B.r;

        int g1 = (int) color_A.g;
        int g2 = (int) color_B.g;

        int b1 = (int) color_A.b;
        int b2 = (int) color_B.b;

        //return (r2 - r1) + (g2 - g1) + (b2 - b1);
        return (r2 - r1) * (r2 - r1) + (g2 - g1) * (g2 - g1) + (b2 - b1) * (b2 - b1);
    }

    // Calculuates mean squared error of an entire image
    static double mse_image(Image &image_A,
                            Image &image_B) {
        double sum = 0;

        for (int x = 0; x < image_A.width; x++)
            for (int y = 0; y < image_A.height; y++)
                sum += square(image_A.get_color(x, y), image_B.get_color(x, y));

        sum /= (image_A.height * image_A.width);
        return sum;
    }

    // todo, is this PSNR function written correctly?
    static double psnr(Image &imageA,
                       Image &imageB) {
        double sum = 0;

        for (int x = 0; x < imageA.width; x++) {
            for (int y = 0; y < imageA.height; y++) {
                sum += square(imageA.get_color(x, y), imageB.get_color(x, y));
            }
        }

        sum /= (imageA.height * imageA.width);

        double result = 20 * log10(255) - 10 * log10(sum);
        return result;
    }

    //Calculuates mean squared error between two blocks, where initial_x and initial_y
    //are the starting positions in image_A, and variable_x and variable_y are the
    //starting positions in image_B
    inline static double mse(Image &image_A, Image &image_B,
                             int initial_x, int initial_y,
                             int variable_x, int variable_y,
                             int block_size) {

        double sum = 0;
        try {
            for (int x = 0; x < block_size; x++)
                for (int y = 0; y < block_size; y++)
                    sum += square(image_A.get_color(initial_x + x, initial_y + y),
                                       image_B.get_color(variable_x + x, variable_y + y));
        }
        catch (std::invalid_argument e) { //make the MSE really high if it went out of bounds (i.e a bad match)
            return 9999;
        }

        sum /= block_size * block_size;
        return sum;
    }
};

#endif //DANDERE2X_IMAGEUTILS_H
