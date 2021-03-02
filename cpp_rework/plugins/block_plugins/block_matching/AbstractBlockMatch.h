
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
Purpose: An abstract block matching class that will implement a block
         matching algorithm. The rigid structure of the abstract class
         forces certain features I want (memoization mostly) and being
         interchangeable when needed without much 'plumbing' work.

         All the book keeping for memoization is done in here.
 
===================================================================== */


#ifndef CPP_REWORK_ABSTRACTBLOCKMATCH_H
#define CPP_REWORK_ABSTRACTBLOCKMATCH_H

#include "../../../frame/Frame.h"
#include "../Block.h"

class AbstractBlockMatch {
public:
    AbstractBlockMatch(const Frame &desired_image, const Frame &input_image, int block_size) {
        this->desired_image = desired_image;
        this->input_image = input_image;
        this->block_size = block_size;

        this->width = desired_image.get_width();
        this->height = desired_image.get_height();
    }

    virtual Block match_block(int x, int y) = 0;

protected:

    Frame desired_image;
    Frame input_image;
    int block_size;

    int width;
    int height;

};

#endif //CPP_REWORK_ABSTRACTBLOCKMATCH_H
