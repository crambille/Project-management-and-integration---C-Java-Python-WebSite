
cCalculator: cJSON.o gen.o hamil.o alpha.o aleat.o gen_kml.o
				gcc -o cCalculator cJSON.o gen.o hamil.o alpha.o aleat.o gen_kml.o
				
cJSON.o: cJSON.c
			gcc -o cJSON.o -c cJSON.c -W -Wall -ansi -pedantic
			
gen.o: gen.c
			gcc -o gen.o -c gen.c -W -Wall -ansi -pedantic

hamil.o: hamil.c
			gcc -o hamil.o -c hamil.c -W -Wall -ansi -pedantic

alpha.o: aplha.c
			gcc -o alpha.o -c alpha.c -W -Wall -ansi -pedantic

aleat.o: aleat.c
			gcc -o aleat.o -c aleat.c -W -Wall -ansi -pedantic

gen_kml.o: gen_kml.c cJSON.h
			gcc -o gen_kml.o -c gen_kml.c -W -Wall -ansi -pedantic
			
clean: 
			rm -rf *.o

mrproper: clean
			rm -rf cCalculator
