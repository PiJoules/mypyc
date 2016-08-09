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
 * Custom getline implementation.
 */
char* get_line(FILE* fp){
    const size_t buffer_size = 256;
    char buffer[buffer_size];
    char* line = (char*)calloc(1, sizeof(char));
    if (!line){
        fprintf(stderr, "Could not calloc 1 byte for initial line.\n");
        return NULL;
    }

    if (ferror(fp)){
        fprintf(stderr, "Invalid file pointer.\n");
        free(line);
        return NULL;
    }
    if (feof(fp)){
        fprintf(stderr, "Reached end of file.\n");
        free(line);
        return NULL;
    }

    char* ptr;
    size_t line_size = 1;  // including null terminator
    do {
        // Read onto buffer
        // Reads either buffer_size characters,
        // until new line, or until EOF.
        if (!fgets(buffer, buffer_size, fp)){
            // EOF reached and no characters read.
            break;
        }
        size_t len = strlen(buffer);
        line_size += len;
        
        // Copy buffer onto line
        line = (char*)realloc(line, line_size);
        if (!line){
            fprintf(stderr, "Could not realloc %zu bytes for line.\n", line_size);
            free(line);
            return NULL;
        }
        strncat(line, buffer, len);
    } while(!(ptr = strchr(line, '\n')) && !feof(fp));

    *(line + line_size - 1) = '\0';  // Set null terminator
    return line;
}

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
