#ifndef LDFILE_H
#define LDFILE_H

#include <stdlib.h>

/**
 * @brief Find a file given a filename and directory.
 *
 * Opens the passed file.
 * 
 * @param filename char* to the name of the target file
 * @param dir char* to filename's directory
 * @return FILE pointer to the open file
 */
FILE *open_file(char *filename, char *dir);

#endif