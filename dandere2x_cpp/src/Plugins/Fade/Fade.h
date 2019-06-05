//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_CPP_FADE_H
#define DANDERE2X_CPP_FADE_H

#include "Image.h"
#include <memory>
#include <iostream>
#include <fstream>
#include <Image/ImageUtils.h>

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
        this->image2 = image2;
        this->image2_compressed = image2_compressed;
        this->block_size = block_size;
        this->fade_file = fade_file;
    }

    void save();

    void run();

private:

    std::shared_ptr<Image> image1;
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

    void add_scalar_to_block(int x, int y, int scalar);

    int bound_integer(int min, int max, int val);

    Image::Color add_scalar_to_color(Image::Color input_color, int scalar);


};

#endif //DANDERE2X_CPP_FADE_H
