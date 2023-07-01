#include "clusters.h"
#include <stdio.h>
#include <time.h>

int main(void) {
    int *board;
    int testsize = 50;
    board = (int *)malloc(sizeof(int) * testsize * testsize);
    srand(time(NULL));

    for (float p1 = 0; p1 <= 1 + 1e-3; p1 += 0.05) {
        int all = 0;
        int total = 0;
        for (int i = 0; i < 50; i++) {
            initialize_board(testsize, p1, board);
            struct set_of_clusters *sos;
            sos = find_clusters(testsize, board);

            all += all_cluster_size(testsize, sos);
            total += sos->num_of_clusters;
        }
        printf("%.5f\t", p1);
        printf("%f\n", (float)all / total);
    }

    return 0;
}