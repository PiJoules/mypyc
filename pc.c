#include "pc.h"


/**
 * File object stuff
 */
typedef struct FileIterator FileIterator;
typedef struct File File;

struct FileIterator {
    File* file_obj;
    int has_next;
};

struct File {
    FILE* file_pointer;
    char* filename;
};


/**
 * Create a file object.
 */
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
    file_obj->file_pointer = fp;  // Save fp so can fclose easily later.

    file_obj->filename = filename;
    return file_obj;
}

/**
 * Create the file iterator.
 */
FileIterator* File_get_iterator(File* file_obj){
    FileIterator* file_iter = (FileIterator*)malloc(sizeof(FileIterator));
    if (!file_iter){
        fprintf(stderr, "Could not malloc %zu bytes for FileIterator object.\n", sizeof(FileIterator));
        exit(EXIT_FAILURE);
    }
    file_iter->file_obj = file_obj;

    // Has next if we have not reached end of file.
    file_iter->has_next = !feof(file_obj->file_pointer);
    return file_iter;
}

/**
 * Get file iterator value.
 */
char* FileIterator_next(FileIterator* iterator){
    // Reached end of iterator
    if (!iterator){
        return NULL;
    }

    FILE* fp = iterator->file_obj->file_pointer;
    char* line = get_line(fp);
    iterator->has_next = !feof(fp);
    return line;
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
