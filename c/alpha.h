#ifndef alpha__h
#define alpha__h

#include "gen.h"
#include <unistd.h>
#include <ctype.h>

static void aff(struct PointOfInterest const *a, size_t n);

static int compare_ville(void const *a, void const *b);

void algo_Alpha(int nb_POI,FILE *ptS,PointOfInterest tabPOI[]);

void AntiChiffre(PointOfInterest tabPOI[], int nb_POI);

void AntiMaj(PointOfInterest tabPOI[], int nb_POI);

#endif
