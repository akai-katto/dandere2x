
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
Purpose: A set of functions to perform Mean Squared Error (MSE)
         computations.
===================================================================== */


#ifndef CPP_REWORK_MSE_FUNCTIONS_H
#define CPP_REWORK_MSE_FUNCTIONS_H

#include "../frame/Frame.h"

class MSE_FUNCTIONS{

    static inline int square(const Frame::Color& color_a, const Frame::Color& color_b);
    static inline double compute_mse(const Frame& image_a, const Frame& image_b,
                                     const int initial_x, const int initial_y,
                                     const int variable_x, const int variable_y,
                                     const int block_size);

};

#endif //CPP_REWORK_MSE_FUNCTIONS_H
