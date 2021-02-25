
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


#ifndef CPP_REWORK_BLOCKMATCHINGMEMOIZATIONTESTCASES_H
#define CPP_REWORK_BLOCKMATCHINGMEMOIZATIONTESTCASES_H

#include "../plugins/block_plugins/BlockMatchingMemoization.h"
#include <assert.h>

class TestBlockMatchingMemoization {
public:

    static void run_test_cases() {

        BlockMatchingMemoization memo_test;

        for (int i = 0; i < 500; i++) {
            for (int j = 0; j < 500; j++) {
                Block test_block(0, 0, i, j, 2);
                assert(!memo_test.is_memoized(test_block));
                memo_test.add_to_memoized(test_block);
                assert(memo_test.is_memoized(test_block));
            }
        }

        for (int i = 0; i < 500; i++) {
            for (int j = 0; j < 500; j++) {
                Block test_block(i, j, 0, 0, 2);
                assert(memo_test.is_memoized(test_block));

                Block test_get = memo_test.get_memoized_block(test_block);
                assert(test_block.is_equivalent(test_get));
            }
        }



    }
};


#endif //CPP_REWORK_BLOCKMATCHINGMEMOIZATIONTESTCASES_H
