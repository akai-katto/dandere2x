//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_VECTORDISPLACEMENT_H
#define DANDERE2X_VECTORDISPLACEMENT_H

class VectorDisplacement {
public:
    int x;
    int y;
    int new_x;
    int new_y;

    VectorDisplacement(int x, int y, int newX, int newY) {
        this->x = x;
        this->y = y;
        this->new_x = newX;
        this->new_y = newY;
    }
};

#endif //DANDERE2X_VECTORDISPLACEMENT_H
