#include "hamil.h"


/**
 * \fn void copyPOI(POI *a, POI b)
 * \brief fonction chargée de transférer le deuxiéme argument dans le premier
 * \author Alyssa Andriot
*/
void copyPOI(POI *a, POI b)
{
	a->ville = b.ville;
	a->longitude = b.longitude;
	a->latitude = b.latitude;
}


/**
 * \fn POI* distancecourte(POI villeMove, POI villedepart , POI villedarriver, POI tabpoi[],int nbvilles , int statuville[])
 * \brief fonction chargée de déterminer le chemin le plus cour entre un poi de départs et un poi d'ariver
 * \author Alyssa Andriot
 */	
POI* distancecourte(POI villeMove, POI villedepart , POI villedarriver, POI tabpoi[],int nbvilles , int statuville[])
{
	double distance ;
	POI *ARRIVER=malloc(sizeof(POI));
	
	POI tabsansvilledepartetarriver[nbvilles-2];
	int i=0 ;
	int j=0;
	int statut;
	
	
	//RECUPERATION DES VILLES SANS CELLE DE DEPART ET DARRIVER
	while ( i < nbvilles) 
	{
		if ((villedepart.ville != tabpoi[i].ville) && (villedarriver.ville != tabpoi[i].ville) )
		{
			copyPOI(&tabsansvilledepartetarriver[j], tabpoi[i]);
			j++;
		}
		i++;
	}
	
	//CALCUL DE LA DISTANCE LA PLUS COURTE A PARTIR DUNE VILLE DE DEPART
	int k;
	const float radius = 6371;
	float PI = 3.1415;
	float lat1=0;
	float lat2=0;
	float long1=0;
	float long2=0;
	
	for ( k=0 ; k < nbvilles-2; k++)
	{
		if (statuville[k+1] == 0)//si la ville nest pas parcouru
		{
			if (villeMove.ville != tabsansvilledepartetarriver[k].ville)
			{
				lat1= villeMove.latitude * PI /180 ;
				lat2= tabsansvilledepartetarriver[k].latitude * PI /180 ;
				
				long1=villeMove.longitude * PI /180 ;
				long2=tabsansvilledepartetarriver[k].longitude * PI /180 ;
				
				distance =  radius * ( PI - asin(sin(lat2) * sin(lat1) + cos(long2 - long1) * cos(lat2) * cos(lat1))); 
				printf("distance : %f \n",distance);
				
				if (distancec > distance)
				{	
					distancec = distance;
					statut =k;
				}
			}
			
		}	
	}
	copyPOI(ARRIVER, tabsansvilledepartetarriver[statut]);
	statuville[statut+1]=1;
	distancec=1000000000;
	return ARRIVER;
}


/**
 * \brief INITIALISATION DU TABLEAU DES STATU DES VILLES : AUCUNE VILLE N 'A ETE PARCOURUR
 * \author Alyssa Andriot
 *
 */
void reinitialisertabstatut( int statuville[], POI ordreville[], POI villedepart ,POI villedarriver, int nbvilles)
{
	int i;
	for (i=0;  i< nbvilles ; i++)
	{
		statuville[i]=0;	
	}  

	copyPOI(&ordreville[0], villedepart);
	copyPOI(&ordreville[nbvilles-1], villedarriver);
}


/**
 * \fn void algohamiltonien(int nbvilles, POI TABpoi[], POI villedepart, POI villedarriver, POI ordreville[] ,int statuville[])
 * \brief fonction de calculer un chemin hamiltonien en deux poi identifier comme point de départ et d'arrivée
 * \author Alyssa Andriot
 * 
 */	
void algohamiltonien(int nbvilles, POI TABpoi[], POI villedepart, POI villedarriver, POI ordreville[] ,int statuville[])
{
	POI villeMove;
	copyPOI(&villeMove,villedepart );
	int l =1;
	for ( l=1; l<nbvilles-1;l++)
	{
		POI* DC =distancecourte(villeMove,villedepart ,villedarriver,TABpoi,nbvilles,statuville);
		copyPOI(&ordreville[l],*DC );
		copyPOI(&villeMove, ordreville[l]);
	}
}
