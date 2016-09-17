#include "alpha.h"



/**
 * \fn static void aff (struct PointOfInterest const *a, size_t n)
 * \brief fonction chargée de gérer les information du mode verbeu pour le trie alphabétique
 * \author Jonathan Salone
 */
static void aff(struct PointOfInterest const *a, size_t n)
{
   size_t i;
   for (i = 0; i < n; i++)
   {
      /* pointeur intermediaire pour alleger l'ecriture */
      struct PointOfInterest const *p = a + i;
     if(verbeux==1)printf ("%-10s %lf %lf\n",p->ville, p->longitude, p->latitude);
   }
   printf ("\n");
}
 
 /**
  * \fn static int compare_ville(void const *a, void const *b)
 *  \brief fonction chargée de comparer deux ville
 * 
 *  details: elle génére deux structure de type PointOfInterest
 *  dans laquelle elle stocke un poi. La fonction strcmp permet de vérifier si ces deux poi sont identique.
 * 	puis elle retourne l'information.
 * 
 * \author Jonathan Salone
 * 
 */
static int compare_ville(void const *a, void const *b)
{
   /* definir des pointeurs type's et initialise's
      avec les parametres */
   struct PointOfInterest const *pa = a;
   struct PointOfInterest const *pb = b;
 
   /* evaluer et retourner l'etat de l'evaluation (tri croissant) */
   return strcmp (pa->ville, pb->ville);
}
 
 
/**
 * \fn void algo_Alpha(int nb_POI,FILE *ptS,PointOfInterest tabPOI[]) 
 * \brief fonction chargée de trié les point de passage par ordre alphabétique afin de définir une route.
 * 
 * l'action de trie se fera par l'intermédiaire de la 
 * fonction  void qsort(void *base, size_t nmemb, size_t size,int (*compar)(const void *, const void *));
 * 																
 * \author Jonathan Salone
 */
void algo_Alpha(int nb_POI,FILE *ptS,PointOfInterest tabPOI[]) 
{ 
/* affichage du tableau dans l'etat */
   /*aff (tab, sizeof tab / sizeof *tab);*/
   if(verbeux==1){ printf("On prend les informations suivantes\n");
	aff (tabPOI, nb_POI);}
	/*trie du tableau via la fonction qsort*/
   qsort (tabPOI, nb_POI, sizeof(struct PointOfInterest), compare_ville);
 
/* affichage du tableau apres le tri */
	if(verbeux==1){ printf("puis on les trie de la façon suivante\n");
   aff (tabPOI, nb_POI);}
   gen_kml(nb_POI,tabPOI,ptS);
 
} 

/**
 * \fn void AntiMaj(PointOfInterest tabPOI[], int nb_POI)
 *  fonction chragée de suprimer les majuscule dans le nom des poi (non utilisée)
 * \author Jonathan Salone
 * 
 */
void AntiMaj(PointOfInterest tabPOI[], int nb_POI)
{
	int i;
	int j;
	int maj=0;
	char str;
	if(verbeux==1){
		printf("\n**** Vérification majuscule ***\n");}
	/*boucle pour tester tout les variables*/
	for (i=0;i<nb_POI;i++){
		for (j=0;j<20;j++){
			str= tabPOI[i].ville[j];
			maj=isupper(str);
			if(maj!=0)
			{
				if(verbeux==1){
					printf( "\n majuscule %c\n",str);}
				/*fonction convertie majuscule en minuscule*/
				tabPOI[i].ville[j]=tolower(str); 	
			}
			if(verbeux==1){
				printf("%c",str);}
		}
		if(verbeux==1){
			printf("\n");}
	}
}


/**
 * \fn void AntiChiffre(PointOfInterest tabPOI[], int nb_POI)
 *  fonction chragée de uprimer les chiffres dans le nom des poi (non utilisée)
 * \author Jonathan Salone
 * 
 */
void AntiChiffre(PointOfInterest tabPOI[], int nb_POI)
{
	int i;
	int j;
	int maj=0;
	char str;
	int test;
	if(verbeux==1){
		printf("\n**** Vérification chiffre ***\n");}
	/**boucle pour tester tout les variables*/
	for (i=0;i<nb_POI;i++){
		for (j=0;j<30;j++){
			str= tabPOI[i].ville[j];
			maj=isdigit(str);
			if(maj!=0)
			{
				if(verbeux==1){
					printf( "\n chiffre %c\n",str);}
			}	
			if(maj!=0)
			{
				/*déplace le chiffre a la fin du mot et est automatiquement supprimé par la structure*/
				test=tabPOI[i].ville[j];
				tabPOI[i].ville[j]=tabPOI[i].ville[j+1];
				tabPOI[i].ville[j+1]=test;
			}
			if(verbeux==1){
				printf("%c",str);}
		}
		if(verbeux==1){
			printf("\n");}
	}
}


