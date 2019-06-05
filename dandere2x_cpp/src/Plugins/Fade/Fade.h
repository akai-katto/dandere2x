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

using namespace std;


class Fade {

    struct FadeBlock {
        int x;
        int y;
        double scalar;
    };


public:
    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image2;
    std::shared_ptr<Image> image2_compressed;
    int block_size;
    std::string fade_file;
    std::vector<FadeBlock> fade_blocks;

    Fade(std::shared_ptr<Image> image1, std::shared_ptr<Image> image2, std::shared_ptr<Image> image2_compressed,
         int block_size, std::string fade_file) {

        this->image1 = image1;
        this->image2 = image2;
        this->image2_compressed = image2_compressed;
        this->block_size = block_size;
        this->fade_file = fade_file;
    }

    void save() {
        std::ofstream out(this->fade_file + ".temp");

        for (int x = 0; x < fade_blocks.size(); x++) {
            out << fade_blocks[x].x << "\n" <<
                fade_blocks[x].y << "\n" <<
                fade_blocks[x].scalar << std::endl;
        }
        out.close();
        std::rename((this->fade_file + ".temp").c_str(), this->fade_file.c_str());

    }

    //Calculuates mean squared error between two blocks, where initial_x and initial_y
    //are the starting positions in image_A, and variable_x and variable_y are the
    //starting positions in image_B
    double mse_fade(Image &image_A, Image &image_B,
                    int initial_x, int initial_y,
                    int variable_x, int variable_y,
                    int block_size, double scalar) {

        double sum = 0;
        try {
            for (int x = 0; x < block_size; x++)
                for (int y = 0; y < block_size; y++)
                    sum += ImageUtils::root_square(image_B.get_color(initial_x + x, initial_y + y),
                                       add_scalar_to_color(image_A.get_color(variable_x + x, variable_y + y), scalar));
        }
        catch (std::invalid_argument e) { //make the MSE really high if it went out of bounds (i.e a bad match)
            return 9999;
        }

        sum /= block_size * block_size;
        return sum;
    }

    void fade_all_blocks() {
        for (int x = 0; x < 1920 / 30; x++) {
            for (int y = 0; y < 1080 / 30; y++) {

                int scalar = get_scalar_for_block(x * block_size, y * block_size);

                FadeBlock current_fade;
                current_fade.scalar = scalar;
                current_fade.x = x * block_size;
                current_fade.y = y * block_size;

                //cout << "scalar: "  << scalar << endl;

                double fade_mse = mse_fade(*image1, *image2,  x * block_size, y * block_size, x * block_size, y * block_size,
                                           block_size, scalar);

                //cout << "fade: " << fade_mse << endl;

                double compressed_mse = ImageUtils::mse(*image2, *image2_compressed,x * block_size, y * block_size,
                                                        x * block_size, y * block_size, block_size );

                //cout << "compressed: " << compressed_mse << endl;

                if (fade_mse <  compressed_mse){
                    fade_blocks.push_back(current_fade);
                    add_scalar_to_block(x * block_size, y * block_size, scalar);
                }



            }
        }
    }


    int get_scalar_for_block(int x, int y) {

        int sum = 0;

        for (int i = x; i < x + block_size; i++) {
            for (int j = y; j < y + block_size; j++) {
                sum += sum_pixel(i, j);
            }
        }

        return (sum / ((block_size * block_size) * 3));

    }

    void add_scalar_to_block(int x, int y, int scalar) {

        for (int i = x; i < x + block_size; i++) {
            for (int j = y; j < y + block_size; j++) {
                image1->set_color(i, j, add_scalar_to_color(image1->get_color(i, j), scalar));
            }
        }

    }

    int sum_pixel(int x, int y) {
        Image::Color col1 = image1->get_color(x, y);
        Image::Color col2 = image2->get_color(x, y);

        return (int) (col2.r - col1.r) + (int) (col2.g - col1.g) + (int) (col2.b - col1.b);
    }

    void add_scalar_to_all() {
        for (int x = 0; x < 100; x++) {
            for (int y = 0; y < 100; y++) {
                image1->set_color(x, y, add_scalar_to_color(image1->get_color(x, y), -14));
            }
        }
    }

    int bound_integer(int min, int max, int val) {
        if (val < min)
            return min;
        if (val > max)
            return max;

        return val;
    }

    Image::Color add_scalar_to_color(Image::Color input_color, int scalar) {
        Image::Color return_color;

        int r = (int) input_color.r;
        int g = (int) input_color.g;
        int b = (int) input_color.b;

        return_color.r = (char) bound_integer(0, 255, r + scalar);
        return_color.g = (char) bound_integer(0, 255, g + scalar);
        return_color.b = (char) bound_integer(0, 255, b + scalar);

        return return_color;

    }


};

#endif //DANDERE2X_CPP_FADE_H
