#include "pc.h"


int main(int argc, char* argv[]){
    // Must provide filename
    if (argc < 2){
        fprintf(stderr, "Fewer than 2 arguments were provided. Expected a filename as the first argument.\n");
        exit(EXIT_FAILURE);
    }

    // Open file
    char* filename = argv[1];
    File* file = open(filename);

    // Read lines
    FileIterator* iterator = File_get_iterator(file);
    while (iterator->has_next){
        char* line = FileIterator_next(iterator);
        printf("%s", line);
        free(line);
    }
    free(iterator);

    // Close file
    File_close(file);

    // Create list of words

    return 0;
}
