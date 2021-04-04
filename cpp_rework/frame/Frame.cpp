
/*
    This file is part of the Dandere2x project.

    Dandere2x is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Dandere2x is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
*/

/*
========= Copyright aka_katto 2018, All rights reserved. ============
Original Author: aka_katto 
Date: 4/11/20 
Purpose: 

=====================================================================
 */

#include <iostream>
#include <random>
#include "Frame.h"

// local includes
#include "external_headers/stb_image.h"
#include "external_headers/stb_image_write.h"

//////////////////
// Constructors //
//////////////////

//----------------------------------------------------
// Purpose: Create a frame loading from a file string.
//----------------------------------------------------
Frame::Frame(const string &file_name) {

    // Using stb_image, load the file using the input string.
    int width, height, bpp;
    unsigned char *stb_image = stbi_load(file_name.c_str(), &width, &height, &bpp, 3);
    this->height = height;
    this->width = width;
    this->file_name = file_name;
    this->bpp = bpp;

    // Begin the process of putting the stb image into our wrapper.
    this->image_colors.resize(this->width, std::vector<Frame::Color>(this->height));

    // Fill our wrapper's image with stbi image information
    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            this->image_colors[x][y] = this->construct_color(stb_image, x, y);

    // Free used memory..
    stbi_image_free(stb_image);
}

//----------------------------------------------------
// Purpose: todo
//----------------------------------------------------
Frame::Frame(const string &file_name, const int compression) {
    int width, height, bpp;
    unsigned char *stb_image = stbi_load(file_name.c_str(), &width, &height, &bpp, 3);

    string temp_name = std::tmpnam(nullptr);
    stbi_write_jpg(temp_name.c_str(), width, height, bpp, stb_image, compression);
    stbi_image_free(stb_image);

    stb_image = stbi_load(temp_name.c_str(), &width, &height, &bpp, 3);
    this->height = height;
    this->width = width;
    this->file_name = file_name;
    this->bpp = bpp;

    // Begin the process of putting the stb image into our wrapper.
    this->image_colors.resize(this->width, std::vector<Frame::Color>(this->height));

    // Fill our wrapper's image with stbi image information
    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            this->image_colors[x][y] = this->construct_color(stb_image, x, y);

    stbi_image_free(stb_image);

}

Frame::Frame(const string &file_name, const int compression, const bool decimal) {

    int width, height, bpp;
    unsigned char *stb_image = stbi_load(file_name.c_str(), &width, &height, &bpp, 3);
    this->height = height;
    this->width = width;
    this->file_name = file_name;
    this->bpp = bpp;

    vector<vector<Frame::Color>> base_image;
    base_image.resize(this->width, std::vector<Frame::Color>(this->height));

    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            base_image[x][y] = this->construct_color(stb_image, x, y);

    string temp_name = std::tmpnam(nullptr);
    stbi_write_jpg(temp_name.c_str(), width, height, bpp, stb_image, compression);
    stbi_image_free(stb_image);
    stb_image = stbi_load(temp_name.c_str(), &width, &height, &bpp, 3);

    // create a vector for compressed frame
    vector<vector<Frame::Color>> compressed_colors;
    compressed_colors.resize(this->width, std::vector<Frame::Color>(this->height));

    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            compressed_colors[x][y] = this->construct_color(stb_image, x, y);
    stbi_image_free(stb_image);

    // Begin the process of putting the stb image into our wrapper.
    this->image_colors.resize(this->width, std::vector<Frame::Color>(this->height));

    // Fill our wrapper's image with stbi image information
    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            this->image_colors[x][y] = average_color(base_image[x][y], average_color(base_image[x][y], compressed_colors[x][y]));

}


//-----------------------------------------------------------------------------
// Purpose: Copy Constructor that trivially copies another image.
//-----------------------------------------------------------------------------
Frame::Frame(const Frame &other) {
    this->height = other.get_height();
    this->width = other.get_width();
    this->file_name = other.get_file_name();
    this->bpp = other.bpp;

    // Begin the process of putting the stb image into our wrapper.
    this->image_colors.resize(this->width, std::vector<Frame::Color>(this->height));

    // Fill our wrapper's image with stbi image information
    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            this->image_colors[x][y] = other.get_color(x, y);

}

//-----------------------------------------------------------------------------
// Purpose:
//-----------------------------------------------------------------------------
Frame::Frame() {

}

//---------------------------------------------------------------------------------------------
// Purpose: Create an empty frame. Mostly used for debugging images. Currently makes the image
//          all black.
//-------------------------------------------------------------------------------------------
Frame::Frame(const int width, const int height, const int bpp) {

    this->file_name = "runtime created image";
    this->height = height;
    this->width = width;
    this->bpp = bpp;

    // Begin the process of putting the stb image into our wrapper.
    this->image_colors.resize(this->width, std::vector<Frame::Color>(this->height));

    Frame::Color black;
    black.r = 0;
    black.g = 0;
    black.b = 0;

    // Fill our wrapper's image with black
    for (int x = 0; x < width; x++)
        for (int y = 0; y < height; y++)
            this->image_colors[x][y] = black;
}

//---------------------------------------------------------------------------------------------
// Purpose: todo
//-------------------------------------------------------------------------------------------
void Frame::apply_noise(const int range) {

    std::random_device rd;
    std::mt19937 gen(rd());
    uniform_int_distribution<> dis(-range, range);

    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            Color edited_color = this->get_color(i, j);
            edited_color.r = max(0, min(255, edited_color.r + dis(gen)));
            edited_color.g = max(0, min(255, edited_color.g + dis(gen)));
            edited_color.b = max(0, min(255, edited_color.b + dis(gen)));
            set_color(i,j, edited_color);
        }
    }

}


//---------------------------------------------------------------------------------------------
// Purpose: todo
//-------------------------------------------------------------------------------------------
void Frame::write(const string &output) {

    unsigned char *stb_image;
    stb_image = new unsigned char[this->get_height() * this->get_width() * 3];

    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            this->deconstruct_color(stb_image, x, y);
        }
    }

    stbi_write_png(output.c_str(), width, height, bpp, stb_image, width * bpp);

}

//////////////////////
// Common Functions //
//////////////////////

//-----------------------------------------------------------------------------------------------------
// Purpose: Provides a sanity check for any Frame function accessing x or y elements. Gives a descriptive
//          error, then terminates the program. This function should be called whenever image_colors is
//          accessed.
//--------------------------------------------------------------------------------------------------
void Frame::sanity_check(const string &caller, const int x, const int y) const {
    if (is_out_of_bounds(x, y)) {
        cerr << "Function: " << caller << " attempted to access invalid frames in " << this->file_name << " \n"
             << "Image Dimensions (Width / Height): " << this->width << " " << this->height << " \n"
             << "Illegal Access at (x,y) " << x << " " << y << endl;

        throw "Ilegall Access!";
    }
}

//-----------------------------------------------------------------------------
// Purpose: Determine whether a block is within bounds of an image or not.
//-----------------------------------------------------------------------------
bool Frame::block_out_of_bounds(const int x, const int y, const int block_size) const {
    return is_out_of_bounds(x + block_size, y + block_size);
}

//-----------------------------------------------------------------------------
// Purpose: Basic check to see if a given x y is within the bounds of an image
//          or not. To be called by any bounds checker in Frame.
//-----------------------------------------------------------------------------
bool Frame::is_out_of_bounds(const int x, const int y) const {
    return x > width - 1 || y > height - 1 || x < 0 || y < 0;
}


// utility functions to assist with stb_image //

//--------------------------------------------------------------------------------------------------------
// Purpose: Get a Frame::Color object from stb_image with respect to it's (x,y) coordinate representation.
//          The way stb_image works is by having individual colors be stored next to each other.
//--------------------------------------------------------------------------------------------------------
Frame::Color Frame::construct_color(const unsigned char *stb_image, const int x, const int y) const {
    sanity_check("Frame::Color &Frame::construct_color", x, y);

    Frame::Color color;
    color.r = stb_image[x * 3 + 3 * y * width + 0];
    color.g = stb_image[x * 3 + 3 * y * width + 1];
    color.b = stb_image[x * 3 + 3 * y * width + 2];
    return color;
}

//--------------------------------------------------------------------------------------------------------
// Purpose: More or less undoes Frame::construct_color, in that it creates an stb_image array by
//          placing the colors found in the array's pixels back into a char array. This is used when
//          saving the file using stb_image_write.
//--------------------------------------------------------------------------------------------------------
void Frame::deconstruct_color(unsigned char *stb_image, const int x, const int y) {
    Color pixel = this->get_color(x, y);

    stb_image[x * 3 + 3 * y * width + 0] = pixel.r;
    stb_image[x * 3 + 3 * y * width + 1] = pixel.g;
    stb_image[x * 3 + 3 * y * width + 2] = pixel.b;
}












