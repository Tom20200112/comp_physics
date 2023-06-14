#include <stdio.h>
#include <stdlib.h>

struct set_of_clusters {
    int num_of_clusters;
    int **clusters;
};

void initialize_board(int N, float p, int *board) {
    // srand(time(NULL));
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            int random = rand() % 10000;
            board[i * N + j] = ((float)random / 10000 <= p ? 1 : 0);
            // printf("%f\n",(float)random/10000);
        }
    }
}

void printboard(int N, int *board) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            printf("%d ", board[i * N + j]);
            if (j % N == N - 1) {
                printf("\n");
            }
        }
    }
}

int isnear_red(int N, int j, int k, int *board) {
    if (j == 0) {
        if (k == 0) {
            if (board[(j + 1) * N + k] == 1 || board[j * N + k + 1] == 1) {
                return 1;
            }
        } else if (k == N - 1) {
            if (board[(j + 1) * N + k] == 1 || board[j * N + k - 1] == 1) {
                return 1;
            }
        } else {
            if (board[(j + 1) * N + k] == 1 || board[j * N + k + 1] == 1 || board[j * N + k - 1] == 1) {
                return 1;
            }
        }
    } else if (j == N - 1) {
        if (k == 0) {
            if (board[(j - 1) * N + k] == 1 || board[j * N + k + 1] == 1) {
                return 1;
            }
        } else if (k == N - 1) {
            if (board[(j - 1) * N + k] == 1 || board[j * N + k - 1] == 1) {
                return 1;
            }
        } else {
            if (board[(j - 1) * N + k] == 1 || board[j * N + k - 1] == 1 || board[j * N + k + 1] == 1) {
                return 1;
            }
        }
    } else if (k == 0) {
        if (board[j * N + k + 1] == 1 || board[(j + 1) * N + k] == 1 || board[(j - 1) * N + k] == 1) {
            return 1;
        }
    } else if (k == N - 1) {
        if (board[j * N + k - 1] == 1 || board[(j + 1) * N + k] == 1 || board[(j - 1) * N + k] == 1) {
            return 1;
        }
    } else {
        if (board[(j + 1) * N + k] == 1 || board[(j - 1) * N + k] == 1 || board[j * N + k + 1] == 1 || board[j * N + k - 1] == 1) {
            return 1;
        }
    }

    return 0;
}

int percolation(int N, int *board) {
    int *shadowboard;
    shadowboard = (int *)malloc(sizeof(int) * N * N);

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            shadowboard[i * N + j] = 0;
        }
    }

    // 先看竖直方向是否percolate
    for (int i = 0; i < N; i++) {
        if (board[i] == 1) {
            shadowboard[i] = 1;
        }
    }

    int ifchange;

    do {
        ifchange = 0;
        // 从上到下从左到右扫描
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, j, k, shadowboard) && board[j * N + k]) {
                    if (shadowboard[j * N + k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[j * N + k] = 1;
                }
            }
        }
        // 从上到下从右到左扫描
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, j, N - 1 - k, shadowboard) && board[j * N + N - 1 - k]) {
                    if (shadowboard[j * N + N - 1 - k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[j * N + N - 1 - k] = 1;
                }
            }
        }
        // 从下到上从右到左扫描
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, N - 1 - j, N - 1 - k, shadowboard) && board[(N - 1 - j) * N + N - 1 - k]) {
                    if (shadowboard[(N - 1 - j) * N + N - 1 - k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[(N - 1 - j) * N + N - 1 - k] = 1;
                }
            }
        }
        // 从下到上从左到右扫描
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, N - 1 - j, k, shadowboard) && board[(N - 1 - j) * N + k]) {
                    if (shadowboard[(N - 1 - j) * N + k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[(N - 1 - j) * N + k] = 1;
                }
            }
        }

        for (int j = 0; j < N; j++) {
            if (board[(N - 1) * N + j] == 1 && shadowboard[(N - 1) * N + j] == 1) {
                return 1;
            }
        }
        // printf("\n");
        // printboard(N,shadowboard);
    } while (ifchange);
    // printf("\n");
    // printboard(N,shadowboard);

    // 清除shadowboard
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            shadowboard[i * N + j] = 0;
        }
    }

    // 再看水平方向是否percolate
    for (int i = 0; i < N; i++) {
        if (board[i * N] == 1) {
            shadowboard[i * N] = 1;
        }
    }

    do {
        // 从上到下从左到右扫描
        ifchange = 0;
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, j, k, shadowboard) && board[j * N + k]) {
                    if (shadowboard[j * N + k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[j * N + k] = 1;
                }
            }
        }
        // 从上到下从右到左扫描
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, j, N - 1 - k, shadowboard) && board[j * N + N - 1 - k]) {
                    if (shadowboard[j * N + N - 1 - k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[j * N + N - 1 - k] = 1;
                }
            }
        }
        // 从下到上从右到左扫描
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, N - 1 - j, N - 1 - k, shadowboard) && board[(N - 1 - j) * N + N - 1 - k]) {
                    if (shadowboard[(N - 1 - j) * N + N - 1 - k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[(N - 1 - j) * N + N - 1 - k] = 1;
                }
            }
        }
        // 从下到上从左到右扫描
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                if (isnear_red(N, N - 1 - j, k, shadowboard) && board[(N - 1 - j) * N + k]) {
                    if (shadowboard[(N - 1 - j) * N + k] == 0) {
                        ifchange = 1;
                    }
                    shadowboard[(N - 1 - j) * N + k] = 1;
                }
            }
        }

        for (int j = 0; j < N; j++) {
            if (board[j * N + N - 1] == 1 && shadowboard[j * N + N - 1] == 1) {
                return 1;
            }
        }
        // printf("\n");
        // printboard(N,shadowboard);
    } while (ifchange);
    // printf("\n");
    // printboard(N,shadowboard);

    return 0;
}

int *copyboard(int N, int *board) {
    int *board_copy;
    board_copy = (int *)malloc(sizeof(int) * N * N);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            board_copy[i * N + j] = board[i * N + j];
        }
    }

    return board_copy;
}

void minusboard(int N, int *board1, int *board2) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            board1[i * N + j] = board1[i * N + j] - board2[i * N + j];
        }
    }
}

int notblank(int N, int *board) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (board[i * N + j]) {
                return 1;
            }
        }
    }

    return 0;
}

struct set_of_clusters *find_clusters(int N, int *board) {
    int **clusters;
    clusters = (int **)malloc(sizeof(int *) * N * N / 2);

    int *shadowboard;
    shadowboard = (int *)malloc(sizeof(int) * N * N);

    int num_of_clusters = 0;

    while (notblank(N, board)) {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                shadowboard[i * N + j] = 0;
            }
        }

        for (int i = 0; i < N; i++) {
            int flag = 0;
            for (int j = 0; j < N; j++) {
                if (board[i * N + j] == 1) {
                    shadowboard[i * N + j] = 1;
                    flag = 1;
                    break;
                }
            }

            if (flag) {
                break;
            }
        }

        int ifchange;

        do {
            ifchange = 0;
            // 从上到下从左到右扫描
            for (int j = 0; j < N; ++j) {
                for (int k = 0; k < N; ++k) {
                    if (isnear_red(N, j, k, shadowboard) && board[j * N + k]) {
                        if (shadowboard[j * N + k] == 0) {
                            ifchange = 1;
                        }
                        shadowboard[j * N + k] = 1;
                    }
                }
            }
            // 从上到下从右到左扫描
            for (int j = 0; j < N; ++j) {
                for (int k = 0; k < N; ++k) {
                    if (isnear_red(N, j, N - 1 - k, shadowboard) && board[j * N + N - 1 - k]) {
                        if (shadowboard[j * N + N - 1 - k] == 0) {
                            ifchange = 1;
                        }
                        shadowboard[j * N + N - 1 - k] = 1;
                    }
                }
            }
            // 从下到上从右到左扫描
            for (int j = 0; j < N; ++j) {
                for (int k = 0; k < N; ++k) {
                    if (isnear_red(N, N - 1 - j, N - 1 - k, shadowboard) && board[(N - 1 - j) * N + N - 1 - k]) {
                        if (shadowboard[(N - 1 - j) * N + N - 1 - k] == 0) {
                            ifchange = 1;
                        }
                        shadowboard[(N - 1 - j) * N + N - 1 - k] = 1;
                    }
                }
            }
            // 从下到上从左到右扫描
            for (int j = 0; j < N; ++j) {
                for (int k = 0; k < N; ++k) {
                    if (isnear_red(N, N - 1 - j, k, shadowboard) && board[(N - 1 - j) * N + k]) {
                        if (shadowboard[(N - 1 - j) * N + k] == 0) {
                            ifchange = 1;
                        }
                        shadowboard[(N - 1 - j) * N + k] = 1;
                    }
                }
            }
            // printf("\n");
            // printboard(N,shadowboard);
        } while (ifchange);
        // printf("\n");
        // printboard(N,shadowboard);
        int *shadowboard_copy = copyboard(N, shadowboard);
        clusters[num_of_clusters] = shadowboard_copy;
        num_of_clusters++;
        minusboard(N, board, shadowboard);
    }
    struct set_of_clusters *sos;
    sos = (struct set_of_clusters *)malloc(sizeof(struct set_of_clusters));
    sos->clusters = clusters;
    sos->num_of_clusters = num_of_clusters;

    return sos;
}

int calculate_size(int N, int *board) {
    int sum = 0;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            sum += board[i * N + j];
        }
    }

    return sum;
}

int all_cluster_size(int N, struct set_of_clusters *sos) {
    int sum = 0;

    for (int i = 0; i < sos->num_of_clusters; i++) {
        sum += calculate_size(N, sos->clusters[i]);
    }

    return sum;
}