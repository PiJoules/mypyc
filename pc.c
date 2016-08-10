#include "pc.h"


/**
 * Lexer stuff
 * The lexer will contain a stream of words read from the file.
 */
typedef struct Lexer Lexer;
struct Lexer {

};

typedef struct List List;
struct List {
    size_t length;
    size_t buffer_lenth;  // Internal buffer size
    void* data;
};


/**
 * Create and initialize list.
 */
List* List_new(){
    List* list = (List*)malloc(sizeof(List));
    if (!list){
        fprintf(stderr, "Could not malloc %zu bytes for List of tokens.\n", sizeof(List));
        return NULL;
    }

    return list;
}

void List_append(List* self, void* item){
    
}


/**
 * Split a string into array of strings.
 */
List* split_string(const char* str, const char* delim){
    // Copy string
    size_t len = strlen(str);
    char* str_cpy = (char*)malloc(len);
    if (!str_cpy){
        fprintf(stderr, "Could not malloc %zu bytes to copy string '%s'.\n", len, str);
        return NULL;
    }
    strncpy(str_cpy, str, len);

    // Get first token
    char* token;
    while ((token = strtok(str_cpy, delim))){
        
    }

    free(str_cpy);
    return tokens;
}

/* End of lexer stuff */


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
