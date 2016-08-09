.PHONY: all

CC = gcc
CFLAGS = 
EXE = pc.c
OBJECTS =
OUTPUT = pc

INCLUDE_DIR = include

# Compiler
CC = gcc
CSTANDARD = c99
INCLUDES = -I$(INCLUDE_DIR)
LIBS = -L$(LIB_DIR)
override CFLAGS += -std=$(CSTANDARD) -Wall $(INCLUDES)

TEST_FILE ?= samples/hello_world.pc

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $<

all:
	$(CC) $(CFLAGS) -o $(OUTPUT) $(EXE) $(OBJECTS)

valgrind:
	valgrind --leak-check=yes ./$(OUTPUT) $(TEST_FILE)

