#include <stdio.h>
#include <stdlib.h>

int main() {
    int *pi = calloc(5, sizeof(int));
    *pi = 5;
    printf("pi: %d\n", *pi);
    free(*pi);
    int *pi2 = malloc(5 * sizeof(int));
    memset(pi2, 0, 5*sizeof(int));
    *pi2 = 7;
    printf("pi2: %d\n", *pi2);
    free(pi2);
}