
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
Purpose: Provide a memoization function / table for various block
         matching algorithms to use.
===================================================================== */


#ifndef CPP_REWORK_BLOCKMATCHINGMEMOIZATION_H
#define CPP_REWORK_BLOCKMATCHINGMEMOIZATION_H

#include "../../frame/Frame.h"
#include "Block.h"

#include <memory>
#include <map>

using namespace std;

class BlockMatchingMemoization {

public:

    BlockMatchingMemoization(){}

    [[nodiscard]] Block &get_memoized_block(const Block &block) const;

    [[nodiscard]] bool is_memoized(const Block &block) const;

    bool add_to_memoized(const Block &block);

private:

    map<unsigned long, Block> memoize_table;

};



#endif //CPP_REWORK_BLOCKMATCHINGMEMOIZATION_H
