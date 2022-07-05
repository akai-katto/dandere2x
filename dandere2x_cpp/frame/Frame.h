
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
#include <iostream>
#include <cstdio>
#include <random>
#include <string.h>


// local includes
#include "external_headers/stb_image.h"


using namespace std;

class Frame {

public:
    struct Color {
        unsigned char r;
        unsigned char g;
        unsigned char b;
    };

    // Returns a color dictated by integer values (R,G,B) bounding them to the defined [0,255] range.
    static Color bound_color(int r, int g, int b);

    // todo
    static inline Color average_color(const Color& color_a, const Color& color_b){

        Color returned_color{};
        returned_color.r = (unsigned char) (((int) color_a.r + (int) color_b.r) / 2);
        returned_color.g = (unsigned char) (((int) color_a.g + (int) color_b.g) / 2);
        returned_color.b = (unsigned char) (((int) color_a.b + (int) color_b.b) / 2);

        return returned_color;
    }

    // Constructors //

    explicit Frame(const string& file_name);

    explicit Frame(const string& file_name, const int compression);

    explicit Frame(const Frame& other);

    explicit Frame(const int width, const int height, const int bpp);

    explicit Frame();

    void write(const string& output);

    // External Bounds Checking //
    bool block_out_of_bounds(const int x, const int y, const int block_size) const;

    bool is_out_of_bounds(const int x, const int y) const;

    // Trivial Getters //
    int get_width() const {
        return this->width;
    }

    int get_height() const {
        return this->height;
    }

    int get_bpp() const {
        return this->bpp;
    }

    string get_file_name() const {
        return this->file_name;
    }

    void apply_noise(int range);

    Frame::Color &get_color(const int x, const int y) const {
        // sanity_check("Frame::Color &Frame::get_color", x, y);
        return const_cast<Frame::Color &>(image_colors[x][y]);
    }

    void set_color(const int x, const int y, const Frame::Color &color) {
        // sanity_check("void Frame::set_color", x, y);
        image_colors[x][y] = color;
    }

private:

    // Helpers
    static int bound_integer(int min, int max, int val);

    // meta data //
    string file_name;
    int width;
    int height;

    // image information //
    vector<vector<Frame::Color>> image_colors;
    int bpp;

    // common functions //
    void sanity_check(const string &caller, const int x, const int y) const;

    // utility functions to assist with stb_image //
    Frame::Color construct_color(const unsigned char *stb_image, const int x, const int y) const;

    void deconstruct_color(unsigned char *stb_image, const int x, const int y);


};


#endif //CPP_REWORK_FRAME_H
