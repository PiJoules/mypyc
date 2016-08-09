#ifndef FILE_H
#define FILE_H

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
 * Free functions
 */
File* open(char* filename);
FileIterator* File_get_iterator(File* file_obj);
char* FileIterator_next(FileIterator* iterator);
void File_close(File* file);

#endif
