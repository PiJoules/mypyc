.PHONY=all

all: build test


build: *.c
	gcc -std=c11 *.c -O2

test: a.out
	valgrind --leak-check=yes ./a.out


