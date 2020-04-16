
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
Purpose: An abstract class describing inherited d2x_cpp classes.
 
===================================================================== */


#ifndef CPP_REWORK_ABSTRACTPLUGIN_H
#define CPP_REWORK_ABSTRACTPLUGIN_H

#include <string>
#include "../frame/Frame.h"

using namespace std;

class AbstractPlugin {
public:

    // Every plugin needs to be 'ran' to some extent.
    virtual void run() = 0;

    // Write the contents of the plugin somewhere.
    virtual void write(const string &output_file) = 0;

private:

    // Every plugin needs to affect the frame somehow after it's done it's processing on it.
    virtual void update_frame() = 0;

    // Every plugin *should* utilize some sort of parallel optimization, although it doesn't need t.
    virtual void parallel_function_call(int x, int y) = 0;

};

#endif //CPP_REWORK_ABSTRACTPLUGIN_H
