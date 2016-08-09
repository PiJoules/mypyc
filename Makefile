.PHONY: all

CC = gcc
CFLAGS = 
EXE = pc.c
OBJECTS =
OUTPUT = pc

INCLUDE_DIR = include
LIB_DIR = lib

# Compiler
CC = gcc
CSTANDARD = c99
INCLUDES = -I$(INCLUDE_DIR)
LIBS = -L$(LIB_DIR)
override CFLAGS += -std=$(CSTANDARD) -Wall $(INCLUDES) $(LIBS)

UTILS = \
	$(LIB_DIR)/get_line.o \
	$(LIB_DIR)/file.o

# Valgrind
# --track-origins=yes if error is found
VALGRIND_ARGS += --leak-check=yes

TEST_FILE ?= samples/hello_world.pc

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $<

all: $(UTILS) $(OBJECTS)
	$(CC) $(CFLAGS) -o $(OUTPUT) $(EXE) $(OBJECTS) $(UTILS)

clean:
	rm -f $(LIB_DIR)/*.o
	rm -f $(OUTPUT)

valgrind:
	valgrind $(VALGRIND_ARGS) ./$(OUTPUT) $(TEST_FILE)

