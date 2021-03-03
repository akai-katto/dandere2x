
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
 
===================================================================== */


#ifndef CPP_REWORK_EXHAUSTIVESEARCH_H
#define CPP_REWORK_EXHAUSTIVESEARCH_H


#include "AbstractBlockMatch.h"

class ExhaustiveSearch : public AbstractBlockMatch {
public:
    ExhaustiveSearch(const Frame &desired_image, const Frame &input_image) : AbstractBlockMatch(desired_image,
                                                                                                input_image) {

    }

    // Implementation of match_block
    Block match_block(int x, int y, int block_size) override;

    void set_max_box(int max_box_arg) { this->max_box = max_box_arg; }

private:

    std::vector<Block::Point> createSearchVector(int centx, int centy);

    int max_box = 10;

};


#endif //CPP_REWORK_EXHAUSTIVESEARCH_H
