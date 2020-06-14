
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
Purpose: Find blocks using my custom-made implementation of diamond
         search. The algorithm is described here:
         https://en.wikipedia.org/wiki/Block-matching_algorithm#Diamond_Search

         Note, I added a few heuristics of my own.
 
===================================================================== */


#ifndef CPP_REWORK_DIAMONDSEARCH_H
#define CPP_REWORK_DIAMONDSEARCH_H

#include "AbstractBlockMatch.h"

class DiamondSearch : public AbstractBlockMatch {
public:

    // For some reason putting constructor in .cpp file gives an error...
    DiamondSearch(Frame &desired_image, Frame &input_image, int block_size) : AbstractBlockMatch(desired_image, input_image, block_size){

    }

    // Implementation of match_block
    Block match_block(int x, int y);

    // for manually tweaking Diamond Search
    void set_max_checks(int max_checks);
    void set_step_size(int step_size);

private:
    int max_checks = 256;  // Cutoff point for when to give up a search.
    int step_size = 2;
    int CHECKS_PER_STEP = 16; // For how many points to probe.
    Block::Point* get_diamond_search_points(int x_origin, int y_origin, int step_size);
    static bool flag_invalid_points(int x_bounds, int y_bounds, Block::Point points[], int size, int block_size, bool flagged[]);

};


#endif //CPP_REWORK_DIAMONDSEARCH_H
