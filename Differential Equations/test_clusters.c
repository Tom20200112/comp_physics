#include "clusters.h"
#include <stdio.h>
#include <time.h>

int main(void) {
    int *board;
    int testsize = 5;
    board = (int *)malloc(sizeof(int) * testsize * testsize);
    float p1 = 0.4;
    srand(time(NULL));

    initialize_board(testsize, p1, board);

    printf("The generated board is:\n");
    printboard(testsize, board);
    printf("\n");

    struct set_of_clusters *sos;

    sos = find_clusters(testsize, board);

    printf("The clusters are:\n");

    for (int i = 0; i < sos->num_of_clusters; i++) {
        printboard(testsize, sos->clusters[i]);
        printf("\n");
    }

    return 0;
}