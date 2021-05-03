
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

#include <memory>
#include <utility>
#include "../../../frame/Frame.h"
#include "../Block.h"

class AbstractBlockMatch {
public:
    AbstractBlockMatch()= default;;

    // Set the current images so we can recycle the object pointer.
    void set_images(shared_ptr<Frame> desired_image, shared_ptr<Frame> input_image){
        this->desired_image = std::move(desired_image);
        this->input_image = std::move(input_image);

        this->width = this->desired_image->get_width();
        this->height = this->desired_image->get_height();
    }

    // Any implementation assumes that desired_image and input_image is not null and already set.
    virtual Block match_block(int x, int y, int block_size) = 0;

protected:

    shared_ptr<Frame> desired_image = nullptr;
    shared_ptr<Frame> input_image = nullptr;

    int width = 0;
    int height = 0;

};


#endif //CPP_REWORK_ABSTRACTBLOCKMATCH_H
