
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
Purpose: This class is to facilitate all the functions and uses dandere2x
         will need to use when handling images. This wrapper
         wraps around stb_image, which is really portable (but not friendly
         for dandere2x computations), and is inspired by Princeton's
         image API library:
         https://introcs.cs.princeton.edu/java/stdlib/javadoc/Picture.html

=====================================================================
*/

#ifndef CPP_REWORK_FRAME_H
#define CPP_REWORK_FRAME_H

// internal includes
#include <vector>
#include <string>

// local includes
#include "externals/stb_image.h"

#define STB_IMAGE_IMPLEMENTATION

using namespace std;

class Frame {

public:
    struct Color {
        unsigned char r;
        unsigned char g;
        unsigned char b;
    };

    // Constructors //
    Frame(const string file_name);

    Frame(const int height, const int width);

    // Getters //
    int getWidth() const;

    int getHeight() const;

    Frame::Color &get_color(const int x, const int y) const;

    // Setters //
    void set_color(const int x, const int y, const Frame::Color &color);

    // External Bounds Checking //
    bool block_within_bounds(const int x, const int y, const int block_size) const;

    bool is_out_of_bounds(const int x, const int y) const;

private:

    // meta data //
    string file_name;
    int width;
    int height;

    // image information //
    vector<vector<Frame::Color>> image_colors;

    // common functions //
    void sanity_check(const string &caller, const int x, const int y) const;

    // utility functions to assist with stb_image //
    Frame::Color construct_color(const unsigned char *stb_image, const int x, const int y) const;


};


#endif //CPP_REWORK_FRAME_H
