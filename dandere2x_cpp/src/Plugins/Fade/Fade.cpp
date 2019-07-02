//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#include "Fade.h"


/**
 * Public Functions
 */


void Fade::save() {
    std::ofstream out(this->fade_file + ".temp");

    for (int x = 0; x < fade_blocks.size(); x++)
        out << fade_blocks[x].x << "\n" <<
               fade_blocks[x].y << "\n" <<
               fade_blocks[x].scalar << std::endl;

    out.close();
    std::rename((this->fade_file + ".temp").c_str(), this->fade_file.c_str());
}


void Fade::run() {

    int height = image1->height;
    int width = image1->width;

    for (int x = 0; x < width / block_size; x++) {
        for (int y = 0; y < height / block_size; y++) {

            // get a scalar value transforming a block at (x,y) f_1 to best match the block in f_2
            int scalar = get_scalar_for_block(x * block_size, y * block_size);

            // find the MSE loss using this weak scalar prediction
            double fade_mse = mse_fade(*image1, *image2, x * block_size, y * block_size,
                                       x * block_size, y * block_size, block_size, scalar);

            // find the max MSE loss from the compressed image
            double compressed_mse = ImageUtils::mse(*image2, *image2_compressed, x * block_size, y * block_size,
                                                    x * block_size, y * block_size, block_size);

            // only add it to the list of accepted fades if it matches the MSE requirement.
            // If the scalar is zero, don't include (since there won't be any affect)
            if (fade_mse < compressed_mse && scalar !=0 ) {
                FadeBlock current_fade;

                current_fade.scalar = scalar;
                current_fade.x = x * block_size;
                current_fade.y = y * block_size;

                fade_blocks.push_back(current_fade);
                draw_over(x * block_size, y * block_size, scalar);
            }
        }
    }
}

/**
 * Private Functions
 */


/*
 * Calculaute the MSE difference between the (preceding block + scalar) and the true image.
 */
double Fade::mse_fade(Image &preceding_image, Image &original_image,
                      int initial_x, int initial_y,
                      int variable_x, int variable_y,
                      int block_size, double scalar) {

    double sum = 0;
    try {
        for (int x = 0; x < block_size; x++)
            for (int y = 0; y < block_size; y++)
                sum += ImageUtils::root_square(original_image.get_color(initial_x + x, initial_y + y),
                                               add_scalar_to_color(preceding_image.get_color(variable_x + x, variable_y + y), scalar));
    }
    catch (std::invalid_argument e) { //make the MSE really high if it went out of bounds (i.e a bad match)
        return 9999;
    }

    sum /= block_size * block_size;
    return sum;
}

// essentially we're flattening the block array and computing the mean of all the valeus
// https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.flatten.html

double Fade::get_scalar_for_block(int x, int y) {

    int sum = 0;

    for (int i = x; i < x + block_size; i++) {
        for (int j = y; j < y + block_size; j++) {

            Image::Color col1 = image1->get_color(i, j);
            Image::Color col2 = image2->get_color(i, j);

            sum += (int) (col2.r - col1.r) + (int) (col2.g - col1.g) + (int) (col2.b - col1.b);
        }
    }

    return (sum / ((block_size * block_size) * 3));

}


void Fade::draw_over(int x, int y, int scalar) {

    for (int i = x; i < x + block_size; i++)
        for (int j = y; j < y + block_size; j++)
            image1->set_color(i, j, add_scalar_to_color(image1->get_color(i, j), scalar));


}


// Prevent an integer from going above RGB limits to avoid problems in code.
// i.e 266 -> 255
int Fade::bound_integer(int min, int max, int val) {
    if (val < min)
        return min;
    if (val > max)
        return max;

    return val;
}

// Prevent a color from leaving 8 Bit RGB space by calling bound integer for all colors.
Image::Color Fade::add_scalar_to_color(Image::Color input_color, int scalar) {
    Image::Color return_color;

    int r = (int) input_color.r;
    int g = (int) input_color.g;
    int b = (int) input_color.b;

    return_color.r = (char) bound_integer(0, 255, r + scalar);
    return_color.g = (char) bound_integer(0, 255, g + scalar);
    return_color.b = (char) bound_integer(0, 255, b + scalar);

    return return_color;

}