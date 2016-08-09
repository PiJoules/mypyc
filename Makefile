.PHONY: all

CC = gcc
CFLAGS = 
EXE = lc.c
OBJECTS =
OUTPUT = lc

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $<

all:
	$(CC) $(CFLAGS) -o $(OUTPUT) $(EXE) $(OBJECTS)

