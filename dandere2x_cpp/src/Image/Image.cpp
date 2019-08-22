//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#include "Image.h"

#define STB_IMAGE_IMPLEMENTATION

#include "stb_image.h"



/*
 * Assumptions:
 *
 * - Assume file will exist eventually
 *
 * - Assume file is readible by stbi_image
 */
Image::Image(std::string file_name) {
    if (!dandere2x::file_exists(file_name))
        throw std::runtime_error("Could not find image file");

    unsigned char *rgb; //the raw pixels
    int width, height, bpp;

    //decode
    this->stb_image = stbi_load(file_name.c_str(), &width, &height, &bpp, 3);
    this->stb_image = stb_image;
    this->height = height;
    this->width = width;
    //the pixels are now in the vector "image", are in 'stb_image' 4 bytes per pixel, ordered RGBARGBA...,

    this->image_colors.resize(this->width, std::vector<Image::Color>(this->height));

    // Put all the colors into image_colors

    for(int x = 0; x < width; x++){
        for(int y = 0; y < height; y++){
            this->image_colors[x][y] = this->construct_color(x,y);
        }
    }
}

Image::~Image() {
    stbi_image_free(this->stb_image);
}


Image::Color &Image::get_color(int x, int y) {
    if (x > width - 1 || y > height - 1 || x < 0 || y < 0)
        throw std::invalid_argument("invalid dimensions");

    return image_colors[x][y];
}


void Image::set_color(int x, int y, Image::Color &color) {
    if (x > width - 1 || y > height - 1 || x < 0 || y < 0)
        throw std::invalid_argument("set color has invalid dimensions");

    image_colors[x][y] = color;
}


Image::Color Image::construct_color(int x, int y) {
    if (x > width - 1 || y > height - 1 || x < 0 || y < 0)
        throw std::invalid_argument("invalid dimensions");

    Image::Color color;
    color.r = stb_image[x * 3 + 3 * y * width + 0];
    color.g = stb_image[x * 3 + 3 * y * width + 1];
    color.b = stb_image[x * 3 + 3 * y * width + 2];

    return color;
}