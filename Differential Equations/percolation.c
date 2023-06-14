#include "clusters.h"
#include <stdio.h>
#include <time.h>

int main(void) {
    int *board;
    int testsize = 20;
    board = (int *)malloc(sizeof(int) * testsize * testsize);

    srand(time(NULL));
    for (float p1 = 0; p1 < 1; p1 += 0.01) {
        int total_percolation = 0;
        for (int i = 0; i < 1000; i++) {
            initialize_board(testsize, p1, board);
            if (percolation(testsize, board)) {
                total_percolation++;
            }
        }
        printf("%.5f\t", p1);
        printf("%d\n", total_percolation);
    }

    return 0;
}