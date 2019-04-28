//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#include "Image.h"

#define STB_IMAGE_IMPLEMENTATION

#include "stb_image.h"

Image::Image(std::string file_name) {

    unsigned char *rgb; //the raw pixels
    int width, height, bpp;
    //decode
    this->stb_image = stbi_load(file_name.c_str(), &width, &height, &bpp, 3);

    this->stb_image = stb_image;
    this->height = height;
    this->width = width;
    //the pixels are now in the vector "image", 4 bytes per pixel, ordered RGBARGBA...,
}

Image::~Image() {
    stbi_image_free(this->stb_image);
}


Image::Color Image::get_color(int x, int y) {
    if (x > width - 1 || y > height - 1 || x < 0 || y < 0)
        throw std::invalid_argument("invalid dimensions");


    Image::Color color;
    color.r = stb_image[x * 3 + 3 * y * width];
    color.g = stb_image[x * 3 + 3 * y * width + 1];
    color.b = stb_image[x * 3 + 3 * y * width + 2];

    return color;
}


void Image::set_color(int x, int y, Image::Color color) {
    if (x > width - 1 || y > height - 1 || x < 0 || y < 0)
        throw std::invalid_argument("set color has invalid dimensions");

    stb_image[x * 3 + 3 * y * width] = color.r;
    stb_image[x * 3 + 3 * y * width + 1] = color.g;
    stb_image[x * 3 + 3 * y * width + 2] = color.b;
}