
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


#include <algorithm>
#include "ExhaustiveSearch.h"

//-----------------------------------------------------------------------------
// Purpose: Create a series points that represent a box surrounding the centx
//          and centy coordinates.
//-----------------------------------------------------------------------------
std::vector<Block::Point> ExhaustiveSearch::createSearchVector(int centx, int centy) {
    std::vector<Block::Point> list = std::vector<Block::Point>();

    for (int x = centx - max_box; x < centx + max_box; x++) {
        for (int y = centy - max_box; y < centy + max_box; y++) {
            if ((x > 0 && x < width) && (y > 0 && y < height)) {
                Block::Point point;
                point.x = x;
                point.y = y;
                list.push_back(point);
            }
        }
    }

    return list;
}

Block ExhaustiveSearch::match_block(int x, int y) {
    vector<Block::Point> test = createSearchVector(x, y);
    vector<Block> blockSum = vector<Block>();

    //find initial disp
    for (int x = 0; x < test.size(); x++) {

        double sum = AbstractBlockMatch::mse_blocks(x, y, test[x].x, test[x].y);

        Block b = Block(x, y, test[x].x, test[x].y, sum);
        blockSum.push_back(b);

    }

    auto smallestBlock = std::min_element(blockSum.begin(), blockSum.end());
    return *smallestBlock;


}
