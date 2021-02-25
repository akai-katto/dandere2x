
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


#include <assert.h>
#include "BlockMatchingMemoization.h"

//-----------------------------------------------------------------------------
// Purpose: See if a block is memoized in either directions, since blocks
//          are single directional vectors.
//-----------------------------------------------------------------------------
bool BlockMatchingMemoization::is_memoized(const Block &block) const {

    bool is_memoized = false;

    if (this->memoize_table.count(block.left_to_right_hash) > 0 || this->memoize_table.count(block.right_to_left_hash) > 0)
        is_memoized = true;

    return is_memoized;
}

//------------------------------------------------
// Purpose: Return the reference if a cached block
//------------------------------------------------
Block &BlockMatchingMemoization::get_memoized_block(const Block &block) const{
    assert(is_memoized(block)); // sanity check

    return const_cast<Block &>(this->memoize_table.at(block.left_to_right_hash));
}


//-----------------------------------------------------------------------------
// Purpose: Add a block to the memoization cache. Adds for both directions
//          in order to account for blocks being single-directional vectors.
//-----------------------------------------------------------------------------
bool BlockMatchingMemoization::add_to_memoized(const Block &block) {
    assert(!is_memoized(block)); // sanity check

    memoize_table[block.left_to_right_hash] = block;
    memoize_table[block.right_to_left_hash] = block;

    return false;
}

