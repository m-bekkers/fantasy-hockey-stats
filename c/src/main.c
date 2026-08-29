#include <stdio.h>
#include <stdlib.h>

#include "ldfile.h"

int main() {
    
    char *skaters_file = "skaters.csv";
    char *skaters_dir = "/home/mbekkers/working/fantasy-hockey-stats/data";

    FILE *result = open_file(skaters_file, skaters_dir);

    return 0;
}