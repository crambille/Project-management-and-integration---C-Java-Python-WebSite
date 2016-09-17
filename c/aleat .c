#include "aleat.h"










/**
 * \brief strcuture contenant les information d-un POI: nom, longitude, latitude
 * \author Nicolas.M
 * \struct PointOfInterest gen_kml.c POI
 */
typedef struct PointOfInterest PointOfInterest;
struct PointOfInterest 




/**
 * \fn void algo_aleat(int nb, POI tabPOI[], FILE *ptS)
 * \brief fonction chargée de générer une route en sélectionent aléatoirement les points de passage
 * 
 * detail: 
 * 
 * \author Nicolas.M
 */
void algo_aleat(int nb, POI tabPOI[], FILE *ptS)
{
	int alea[nb];
	int compt,courant,test,rcompt,rimple;
	rimple=1;test=1;
	PointOfInterest * tabPOI_Rand;
	tabPOI_Rand = malloc (nb * sizeof(PointOfInterest));
	
	for(compt=0;compt<nb;compt++){alea[compt]=18;}/*initialisation du tableau de nombre alétoire */
	srand(time(NULL));
	if(verbeux==1) printf("initialisation du tableau de nombre alétoire");
	for(compt=0;compt<=nb-1;compt++)
	{	
		test=1;
		courant=rand()%nb;/*on génére un chiffre aléatoire*/
		if(verbeux==1) printf("on génére un chiffre aléatoire %d \n",courant);
		for(rcompt=0;rcompt<=rimple-1;rcompt++)
		{
			if(courant==alea[rcompt])test=0;/*on le compare à ceux déja présent dans le tableau*/
			if(verbeux==1) printf("et on le compare à ceux déja présent dans le tableau %d ",alea[rcompt]);
		}
		if(test==0)compt=compt-1;/*si le chffre n'est pas déja présent on le sauvegarde*/
		else {
			alea[rcompt-1]=courant;
			rimple=rimple+1;
			if(verbeux==1) printf("si le chffre n'est pas déja présent on le sauvegarde \n");
		}
	}
	if(verbeux==1) printf("on utilise ensuite se tableau pour définir l'ordre dans lequel le drone parcoure les villes \n");
	/*on remplie l nouveau tableau de POI en fonction de l'ordre déterminée précédament*/
	for(compt=0;compt<=nb-1;compt++)
	{
			tabPOI_Rand[compt]=tabPOI[alea[compt]];/*on utilise ensuite se tableau pour définir l'ordre dans lequel le drone parcoure les villes*/
			if(verbeux==1) printf("ville %s en numéros %d\n",tabPOI_Rand[compt].ville,compt);
	}
	gen_kml(nb,tabPOI_Rand,ptS);
	if(verbeux==1) printf("Une route aléatoire vient d'étre réalisée\n");
}
