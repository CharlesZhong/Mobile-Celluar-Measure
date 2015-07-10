object=main.o image.o in.o jp2tools.o
objs=demo
cc=gcc
flags=-O0 -Wall -g 
LIBS=-lpthread -lpng -ljpeg -lgif -lm -lz -ljasper -lsasl2

main:$(object)
	$(cc) $(flags) $(object) -o $(objs) -L$(LIBS)
$(object):%o:%c
	$(cc) $(flags) -c $< -o $@ -L$(LIBS)
.PHONE:clean
clean:
	-rm *.o $(objs)
