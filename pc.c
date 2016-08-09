#include "pc.h"


/**
 * File object stuff
 */
typedef struct FileIterator FileIterator;
typedef struct File File;

struct FileIterator {
    FileIterator* next_iter;
    char* line;
};

struct File {
    FileIterator* iterator;
    char* filename;
    FILE* file_pointer;
};

File* open(char* filename){
    File* file_obj = (File*)malloc(sizeof(File));
    if (!file_obj){
        fprintf(stderr, "Could not malloc %zu bytes for File object.\n", sizeof(File));
        exit(EXIT_FAILURE);
    }

    // Set file pointer
    FILE* fp = fopen(filename, "r");
    if (!fp){
        fprintf(stderr, "Null file pointer when opening file \"%s\".\n", filename);
        exit(EXIT_FAILURE);
    }
    file_obj->file_pointer = fp;
    file_obj->filename = filename;

    return file_obj;
}

void File_close(File* file){
    fclose(file->file_pointer);
    free(file);
}
/* End of File object stuff */



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
    //ssize_t read_len
    //while ((read))

    // Close file
    File_close(file);

    // Create list of words

    return 0;
}
