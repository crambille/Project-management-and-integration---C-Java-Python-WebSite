#ifndef gen__h
#define gen__h

#include <stdlib.h>
#include <stdio.h>

/**
 * \brief strcuture contenant les information d-un POI: nom, longitude, latitude
 * \author Nicolas.M
 * \struct PointOfInterest gen_kml.c POI
 */
typedef struct PointOfInterest PointOfInterest;
struct PointOfInterest 
{
	char *ville;
    double longitude;
    double latitude;
    PointOfInterest *suiv;
};
typedef PointOfInterest POI;

void gen_kml(int nb, POI tabPOI[], FILE *ptS);


#endif
