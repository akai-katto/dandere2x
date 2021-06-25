//
// Created by Tyler on 4/19/2021.
//

#ifndef CPP_REWORK_LAB_UTILITIES_H
#define CPP_REWORK_LAB_UTILITIES_H
#include <math.h>

class LabUtilities{
public:

    struct Lab{
        double l;
        double a;
        double b;
    };

    Lab rgb_to_lab(int R_value, int G_value, int B_value) {
        double RGB[3];
        double XYZ[3];
        double Lab[3];
        double RGB2[3];
        double XYZ2[3];
        double Lab2[3];
        double adapt[3];
        double value;

        double trans[3];
        double transf[3];
        double newXYZ[3];
        double newRGB[3];

        //maybe change to global, XYZ[0] = X_value

        adapt[0] = 0.950467;
        adapt[1] = 1.000000;
        adapt[2] = 1.088969;

        RGB[0] = R_value * 0.003922;
        RGB[1] = G_value * 0.003922;
        RGB[2] = B_value * 0.003922;

        XYZ[0] = 0.412424 * RGB[0] + 0.357579 * RGB[1] + 0.180464 * RGB[2];
        XYZ[1] = 0.212656 * RGB[0] + 0.715158 * RGB[1] + 0.0721856 * RGB[2];
        XYZ[2] = 0.0193324 * RGB[0] + 0.119193 * RGB[1] + 0.950444 * RGB[2];

        Lab[0] = 116 * H(XYZ[1] / adapt[1]) - 16;
        Lab[1] = 500 * (H(XYZ[0] / adapt[0]) - H(XYZ[1] / adapt[1]));
        Lab[2] = 200 * (H(XYZ[1] / adapt[1]) - H(XYZ[2] / adapt[2]));

        RGB2[0] = R_value2 * 0.003922;
        RGB2[1] = G_value2 * 0.003922;
        RGB2[2] = B_value2 * 0.003922;

        XYZ2[0] = 0.412424 * RGB2[0] + 0.357579 * RGB2[1] + 0.180464 * RGB2[2];
        XYZ2[1] = 0.212656 * RGB2[0] + 0.715158 * RGB2[1] + 0.0721856 * RGB2[2];
        XYZ2[2] = 0.0193324 * RGB2[0] + 0.119193 * RGB2[1] + 0.950444 * RGB2[2];

        Lab2[0] = 116 * H(XYZ2[1] / adapt[1]) - 16;
        Lab2[1] = 500 * (H(XYZ2[0] / adapt[0]) - H(XYZ2[1] / adapt[1]));
        Lab2[2] = 200 * (H(XYZ2[1] / adapt[1]) - H(XYZ2[2] / adapt[2]));

        if ( Lab2[0] > 903.3*0.008856 )
            trans[1] = pow ( (Lab2[0]+16)*0.00862, 3);
        else
            trans[1] = Lab2[0] * 0.001107;

        if ( trans[1] > 0.008856 )
            transf[1] = (Lab2[0]+16)*0.00862;
        else
            transf[1] = (903.3*trans[1]+16)*0.00862;

        transf[0] = Lab2[1] * 0.002 + transf[1];
        transf[2] = transf[1] - Lab2[2] * 0.005;

        if ( pow( transf[0], 3 ) > 0.008856 )
            trans[0] = pow( transf[0], 3 );
        else
            trans[0] =  ((116 * transf[0]) - 16) * 0.001107;

        if ( pow( transf[2], 3 ) > 0.008856 )
            trans[2] = pow( transf[2], 3 );
        else
            trans[2] =  ((116 * transf[2]) - 16) * 0.001107;

        newXYZ[0] = trans[0] * adapt[0];
        newXYZ[1] = trans[1] * adapt[1];
        newXYZ[2] = trans[2] * adapt[2];

        newRGB[0] = 3.24071 * newXYZ[0] + (-1.53726) * newXYZ[1] + (-0.498571) * newXYZ[2];
        newRGB[1] = (-0.969258) * newXYZ[0] + 1.87599 * newXYZ[1] + 0.0415557 * newXYZ[2];
        newRGB[2] = 0.0556352 * newXYZ[0] + (-0.203996) * newXYZ[1] + 1.05707 * newXYZ[2];

        newRGB[0] *= 255;
        newRGB[1] *= 255;
        newRGB[2] *= 255;

        //printf("r=%f g=%f b=%f nr=%f ng=%f nb=%f\n",Lab[0],Lab[1],Lab[2],Lab2[0],Lab2[1],Lab2[2]);

        value = pow((Lab[0] - Lab2[0]), 2) + pow((Lab[1] - Lab2[1]), 2) + pow((Lab[2] - Lab2[2]), 2);
        return value;
    }

    double H(double q) {
        double value;
        if ( q > 0.008856 ) {
            value = pow ( q, 0.333333 );
            return value;
        }
        else {
            value = 7.787*q + 0.137931;
            return value;
        }
    }

};


#endif //CPP_REWORK_LAB_UTILITIES_H
