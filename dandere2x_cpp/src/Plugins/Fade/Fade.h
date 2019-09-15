//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_CPP_FADE_H
#define DANDERE2X_CPP_FADE_H

/**
 * Description:
 *
 * Sometimes two images can be replicated by applying scalar values to blocks. This happens when a scene
 * is fade to black or fade to white: we need to simply try and guess a good scalar value to add to an
 * entire block to bring us closer to the desired image.
 *
 * Inputs:
 *
 * - image1 input image
 *
 * - image2 is hopefully image1, but faded to black / faded to white.
 *
 * Runtime:
 *
 * -  See if we can find good scalars for each block in order to replicate image2 using image + scalars.
 *
 * Outputs:
 *
 * - A series of vectors and scalars that will bring image1 to look like image2.
 *
 * - Draw over image2 using pieces found in image1 (if it is correct)
 *
 *
 */

#include "Image.h"
#include <memory>
#include <iostream>
#include <fstream>
#include <Image/ImageUtils.h>
#include "Image/SSIM/SSIM.h"

using namespace std;


class Fade {

    struct FadeBlock {
        int x;
        int y;
        double scalar;
    };


public:

    Fade(std::shared_ptr<Image> image1, std::shared_ptr<Image> image2, std::shared_ptr<Image> image2_compressed,
         int block_size, std::string fade_file) {

        this->image1 = image1;
        this->image1_copy = make_shared<Image>(*image1);
        this->image2 = image2;
        this->image2_compressed = image2_compressed;
        this->block_size = block_size;
        this->fade_file = fade_file;
    }

    void save();

    void run();

private:

    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image1_copy;
    std::shared_ptr<Image> image2;
    std::shared_ptr<Image> image2_compressed;
    int block_size;
    std::string fade_file;
    std::vector<FadeBlock> fade_blocks;

    double mse_fade(Image &preceding_image, Image &original_image,
                    int initial_x, int initial_y,
                    int variable_x, int variable_y,
                    int block_size, double scalar);

    double get_scalar_for_block(int x, int y);

    void draw_over(int x_start, int y_start, int scalar);

    void add_scalar_to_copy(int x_start, int y_start, int scalar);

    int bound_integer(int min, int max, int val);

    Image::Color add_scalar_to_color(Image::Color input_color, int scalar);


};

#endif //DANDERE2X_CPP_FADE_H
