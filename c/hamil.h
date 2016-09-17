#ifndef hamil__h
#define hamil__h

#include "gen.h"

void algohamiltonien(int nbvilles, POI TABpoi[], POI villedepart, POI villedarriver, POI ordreville[] ,int statuville[]);

void reinitialisertabstatut( int statuville[], POI ordreville[], POI villedepart ,POI villedarriver, int nbvilles);

POI* distancecourte(POI villeMove, POI villedepart , POI villedarriver, POI tabpoi[],int nbvilles , int statuville[]);

void copyPOI(POI *a, POI b);



#endif
