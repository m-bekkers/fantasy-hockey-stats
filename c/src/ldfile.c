#include <stdio.h>
#include <stdlib.h>

#include "ldfile.h"

FILE* open_file(char *filename, char *dir) {

    // Create pointer to store our file pointer in
    FILE *ptr = NULL;

    // Normalize filename and dir and concatenate them into a path
    char *tmp = filename;
    while (*tmp) {
        printf("%c\n", *tmp);
        tmp++;
    }

    return ptr;

}