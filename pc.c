#include "pc.h"


int main(int argc, char* argv[]){
    // Must provide filename
    if (argc < 2){
        fprintf(stderr, "Fewer than 2 arguments were provided. Expected a filename as the first argument.\n");
        exit(EXIT_FAILURE);
    }

    // Open file
    char* filename = argv[1];
    FILE* fp = fopen(filename, "r");
    if (!fp){
        fprintf(stderr, "Null file pointer when opening file \"%s\".\n", filename);
        exit(EXIT_FAILURE);
    }
    fclose(fp);

    // Create list of words

    return 0;
}
