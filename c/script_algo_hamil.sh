#!/bin/bash
# ce script test le programme avec l'algo de génération de route hamiltoniéne.
# gcc *.c -o cCalculator -lm permet de compiler le programme si  l'exécutable n'est pas présent
ls example.kml #démontre que le fichier n'est pas présent dans le fichier
echo le fichier kml n\'est pas encore créé
./cCalculator -i test.JSON -o example.kml -a algo_hamil #lance l'éxecution du programme avec le fichier d'exemple fournit avec le code source
ls example.kml
echo le fichier est bien présent, voyons ce qu\'il contient
nano example.kml # affiche dans l'invit de commande le contenu du fichier créé.
echo le fichier est créé corectement. 
exit 0
