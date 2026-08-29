CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -g

main: main.o ldfile.o
	$(CC) main.o ldfile.o -o main

main.o: main.c ldfile.h
	$(CC) $(CFLAGS) -c main.c

ldfile.o: ldfile.c ldfile.h
	$(CC) $(CFLAGS) -c ldfile.c

clean:
	rm -f main *.o