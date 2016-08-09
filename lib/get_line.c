#include "pc.h"

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
