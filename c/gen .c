#include "gen.h"




/**
 * \fn void gen_kml(int nb, POI tabPOI[], FILE *ptS)
 * 
 * \brief fonction chargée de sauvegarder au format kml les POI ainsi que la route définie par une autre fonction 
 * 
 * \author Nicolas.M
 */
void gen_kml(int nb, POI tabPOI[], FILE *ptS)
{
	int compt;
	char baliseDeb[2048];/* création du "buffer" ouvrant */
	char baliseFerm[500];/* création du "buffer" fermant*/
	sprintf((char *) &baliseDeb,"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"https://www.opengis.net/kml/2.2\">\n<Document>\n  <name>DCL</name>\n\n\n    <!-- Styles d'affichage -->\n    <!-- color format: aabbggrr -->\n    <Style id=\"beg\">\n      <IconStyle>\n        <color>ff00ff00</color>\n          <colorMode>normal</colorMode>\n      </IconStyle>\n    </Style>\n    <Style id=\"mid\">\n      <IconStyle>\n        <color>ffffffff</color>\n        <colorMode>normal</colorMode>\n      </IconStyle>\n    </Style>\n    <Style id=\"end\">\n      <IconStyle>\n        <color>ff0000ff</color>\n        <colorMode>normal</colorMode>\n      </IconStyle>\n    </Style>\n    <Style id=\"tip\">\n      <LineStyle>\n        <color>ffffeedd</color>\n        <colorMode>normal</colorMode>\n        <width>4</width>\n      </LineStyle>\n    </Style>\n\n  <!-- les Points d'intérêt géographiques -->\n"); /* on construit dans le buffer les balises ouvrante */
	sprintf((char *) &baliseFerm,"      </coordinates> \n    </LineString>\n  </Placemark>\n</Document>\n</kml>"); /* puis de férmante */
	
	char *fourtout[nb];
	fourtout[0]="beg";/*on génére en paraléle un tableau contenant les styles correpondants à chaque POI*/
	for(compt=1;compt<=nb-2;compt++){fourtout[compt]="tip";}
	fourtout[nb-1]="end";
	
	 if (ptS != NULL) /* on verifie que le fichier à est pret à recevoir les données*/
	 { 
            fprintf(ptS,"%s\n", baliseDeb);  
            for(compt=0;compt<nb;compt++)/*stocke chaque poi au format imposée*/
            {
				fprintf(ptS,"<Placemark>\n    <styleUrl>%s</styleUrl>\n    <name>%s</name>\n    <visibility>1</visibility> \n",fourtout[compt],tabPOI[compt].ville); 
				fprintf(ptS,"    <Point>\n      <coordinates>\n        %f,%f</coordinates>\n    </Point>\n  </Placemark>\n", tabPOI[compt].longitude,tabPOI[compt].latitude); 
				if(verbeux==1) printf("insertion des coordonnées du POI numéros: %d, corespondant à %s longitude: %f et latitude: %f\n",compt,tabPOI[compt].ville,tabPOI[compt].longitude,tabPOI[compt].latitude);
			}
			fprintf(ptS,"<Placemark>\n  <LineString>\n    <coordinates> \n<!-- Le tracé de livraison -->\n");
			for(compt=0;compt<nb;compt++)/*on stocke les étapes de la route*/
            {
				if(verbeux==1) printf("sauveagrde de la route définie, étapes %d\n",compt);
				fprintf(ptS,"      %f,", tabPOI[compt].longitude); 
				if(verbeux==1) printf("longitude: %f\n",tabPOI[compt].longitude);
				fprintf(ptS,"      %f,\n", tabPOI[compt].latitude);
				if(verbeux==1) printf("latitude: %f \n",tabPOI[compt].latitude);
			}
            fprintf(ptS,"%s\n", baliseFerm);  
            printf("ecriture done\n");
                   
     } 
	if(verbeux==1) printf("génération  du kml c'est términé correctement\n");
}
