#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <algorithm>

#define MAXN 10000000

typedef int DType;

DType relax[MAXN];
int *x = relax;
int n;

void swap(int i, int j) {
    DType t = x[i];
    x[i] = x[j];
    x[j] = t;
}

int randint(int l, int u) {
    return l + (RAND_MAX*rand() + rand()) % (u - l + 1);
}

int intcomp(const void *x, const void *y) {
    int a = *(const int *)x;
    int b = *(const int *)y;
    return a - b;
}

void timedriver() {
    int i, k, algnum, mod, start, clicks;
    while (scanf("%d %d %d", &algnum, &n, &mod) != EOF) {
        if (mod <= 0)
            mod = 10*n;
        for (i = 0; i < n; i++)
            x[i] = randint(0, mod - 1);
        k = n/2;
        start = clock();
        switch (algnum) {
            case 11:
                qsort(x, n, sizeof(int), intcomp);
                break;
        }
    }
}