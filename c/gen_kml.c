
/****************************************************************************
 * Copyright (C) 2015 by Alyssa Andriot, Jonathan Salone, Medar Nciolas	    *                              
 *  \version 2.0  															*
 * 	\file gen_kml.c															*
 *  																		*
 *                                                               			*
 ****************************************************************************/

/**
 * \file gen_kml.c	
 * \author Medar {Alyssa Andriot, Jonathan Salone, Medar Nciolas}
 * \date 25 Juin 2015
 * \brief programme recevant un fichier json en paramétre et générant une route retournée au serveur sous la forme d'un fichier kml
 *
 * Here typically goes a more extensive explanation of what the header
 * defines. Doxygens tags are words preceeded by either a backslash \
 * 
 * \see file:///home/nmedar/Documents/integration/c/doc/html/globals.html
 * \see file:///home/nmedar/Documents/integration/c/doc/html/globals_func.html
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <unistd.h>
#include <ctype.h>
#include "cJSON.h"
//bibliothéque spécifique au programme//
#include "aleat.h"
#include "alpha.h"
#include "gen.h"
#include "hamil.h"


/**
 * \enum verbeux
 * \def distancec
 */
int verbeux=0;
double distancec = 10000000;






int main(int argc, char **argv)//int nb_POI, char **pathFilename,char **nom_F_sortie)
{ 
	int nArg=0;
	int nb_POI =0;
	char nom_F_sortie[32];
	char nom_F_entre[32];
	char algo_selected[32];
	
	if(argc<1)
	{printf("aucun argument fournis \n");
		exit(0);}
	
	for (nArg=0;nArg<=argc-1;nArg++)
	{
		if (strcmp(argv[nArg] ,"-v")==0 || strcmp(argv[nArg],"--verbose")==0)
		/**
		* \param[in] argv pointeur sur option
		* si l'option corespondante au mode verbeux est détectée
		*/
		{
			verbeux=1;/*on passe la variable magique à 1 pour indiquer à chaque fonction le mode de fonctonnement du programme*/
			printf("le mode verbeux est actif");
		}
		else if (strcmp(argv[nArg] ,"-o")==0 || strcmp(argv[nArg] ,"--out")==0)/*si l'option corespondante au fichier de sortie(kml) est détectée*/
		{												/*on répéte les mêmes opérations*/
			if(strlen(argv[nArg+1])>32)
				{printf("le nom du fichier d'entrée et trop long \n");exit(0);
					if (verbeux==1)printf("le fichier %s est créé et sélectioné comme sortie",nom_F_entre);	
				}
			else {strcpy(nom_F_sortie, argv[nArg+1]);nArg++;}
		}
		else if (strcmp(argv[nArg] ,"-h")==0 || strcmp(argv[nArg] ,"--help")==0)/*si l'option corespondante à l'aide est détectée*/
		{
			printf("aide en commande: \n -option de contrôle du programme\n -i fichier ou --in fichier : chemin vers le fichier JSON d’entrée\n-o fichier ou --out fichier : chemin vers le fichier KML de sortie\n-h ou --help : affiche l’aide\n-v ou --verbose : mode verbeux\n-a nom ou --algo nom : nom de l’algorithme de planification à utiliser\n commandes pour sélectionner l’algorithme de planification à utiliser:\n \"algo_aleat\": correspond au chemin aléatoire \n \"algo_alpha\": détermine une route en fonction du nom des villes (trie alphabétique) \n \"algo_hamil\": permet de générer une route hamiltoniene \n merci de relancer le programme \n  ");/* on affiche l'aide*/
			exit(0);
		}
		else if(strcmp(argv[nArg] ,"-i")==0 || strcmp(argv[nArg],"--in")==0)/*si l'option corespondante au fichier JSON est détectée*/
		{
			if(strlen(argv[nArg+1])>32)
				{printf("le nom du fichier d'entrée et trop long \n");exit(0);}/*on teste si la taille du nomn ne dpasse pas la taille allouée en mémoire*/
			else {strcpy(nom_F_entre, argv[nArg+1]);nArg++;
					if (verbeux==1)printf("le fichier %s est sélectioné comme source",nom_F_entre);	
				}/*puis on sauvegarde le nom dans ledit buffer.*/
		}
		
		else if (strcmp(argv[nArg] ,"-a")==0 || strcmp(argv[nArg],"--algo")==0) /*si l'option corespondante à la selection de l'algo est détectée*/
		{                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
			if(strlen(argv[nArg+1])>32)
				{printf("le nom du fichier d'entrée et trop long");exit(0);}
			else {strcpy(algo_selected, argv[nArg+1]);nArg++;if (verbeux==1)printf("l'algo %s est créé et sélectioné comme sortie",nom_F_entre);	}
		}
	}
	
	if(nArg<6)
	{printf("trop peu d'argument fournis \n");exit(0);}
	
	int courant;
	cJSON *objJson;/** */
	cJSON *itemJson;
	cJSON *coord;
	cJSON *data;
	
	///////////////////////////////////////////////////
	
	FILE *ptE; /*pointeur sur le fichier json transmit en paramétre*/
	ptE=fopen(nom_F_entre,"r");
	if(ptE==NULL){printf("erreur detectée sur le fichier json, fichier inexistant ou mauvais nom renseigné");exit(0);}
	if( access(nom_F_sortie, F_OK) != -1)
	{
		if(remove(nom_F_sortie) == 0)
		{
			puts("Suppression du fichier kml existant.\n");
		}
	}
	
	FILE *ptS;/*pointeur sur le fichie kml de sortie*/
	ptS = fopen(nom_F_sortie,"a");
	
	fseek(ptE, 0, SEEK_END);/*détermine la taille du fichier transmit en paramétre du main*/
	long fsize =ftell(ptE);
	printf("%ld\n",fsize);
	char jsonbuffer[fsize];
	fseek(ptE, 0, SEEK_SET);
	
	int jl=fread(jsonbuffer,1,fsize,ptE);/*on récupére le contenu du fichier json et on le place dans un tableau*/
	if(verbeux==1)printf("on récupére le contenu du fichier json et on le place dans un tableau de %d octets\n",jl);
	objJson=cJSON_Parse(jsonbuffer);/* on parse le contenu du tableau pour en faire un objet json (structure)*/
	if(verbeux==1)printf("on parse le contenu du tableau pour en faire un objet json (structure)");
 	if (!objJson) {printf("Error before: [%s]\n",cJSON_GetErrorPtr());}
	/*on récupére les informations qui nous intéresse et on les stocke dans la structure prévu à cet effet*/
	/**************************/
	nb_POI = cJSON_GetArraySize(objJson);
	if(verbeux==1)printf(" nombre de POI détecté aprés mesure %d\n",nb_POI);
	POI ordreville[nb_POI];
	int statuville[nb_POI];
	PointOfInterest * tabPOI;
	tabPOI = malloc (nb_POI * sizeof(PointOfInterest));

	/*********************/	
	for(courant=0;courant<nb_POI;courant++)
	{
		if(verbeux==1)printf("récupération des données du POI %d\n",courant);
		itemJson=cJSON_GetArrayItem(objJson,courant);
		data=cJSON_GetObjectItem(itemJson,"name");
		tabPOI[courant].ville=data->valuestring;
		if(verbeux==1)printf("récupération du nom: %s, ",tabPOI[courant].ville);
		coord=cJSON_GetObjectItem(itemJson,"coord");
		data=(cJSON_GetObjectItem(coord,"lon"));
		tabPOI[courant].longitude=data->valuedouble;
		if(verbeux==1)printf("de la longitude: %f, ",tabPOI[courant].longitude);
		data=(cJSON_GetObjectItem(coord,"lat"));
		tabPOI[courant].latitude=data->valuedouble;
		if(verbeux==1)printf("de la latitude: %f \n",tabPOI[courant].latitude);
		tabPOI[courant].suiv=NULL;
	}
	
	if((nb_POI<3||nb_POI>7)){printf("le nombre de ville à livrer est non conforme aux limites imposée, plus de 7 ou moins de 3 \n");exit(0);}
	if (verbeux==1)printf("%d point de livraison demandés",nb_POI);
	
	 AntiMaj(tabPOI,nb_POI);
	/*verifie les si chiffres */
	 AntiChiffre(tabPOI,nb_POI);

	if(strcmp (algo_selected, "algo_aleat")==0) algo_aleat(nb_POI,tabPOI,ptS);
	else if (strcmp (algo_selected , "algo_alpha")==0) algo_Alpha(nb_POI,ptS,tabPOI);
	else if(strcmp(algo_selected,"algo_hamil")==0)
	{
		reinitialisertabstatut( statuville,ordreville, tabPOI[0] ,tabPOI[nb_POI-1], nb_POI);
		algohamiltonien(nb_POI, tabPOI, tabPOI[0], tabPOI[nb_POI-1], ordreville, statuville);
		if (verbeux==1){	int n;
			for(n=0; n < nb_POI;n++)
			{
				printf("route choie par la fonction hamiltoniene %s\n", ordreville[n].ville);
			}
		}
		gen_kml(nb_POI,ordreville,ptS);
		
	}
	else {printf("erreur l'algo demandée n'est pas bon...veuillez recommencer");exit(0);}	
	
	printf("gen closed\n");
	fclose(ptE);  
	free(tabPOI);
	 fclose(ptS);  
     printf("kml close\n");
	return 0; 
}
