#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "bool.h"
#include "priority_queue.h"
#include "queue.h"
#include "random.h"

#define NELEM 100
#define LESS_THAN -1
#define EQUAL_TO 0
#define GREATER_THAN 1

bool compare(item_type a, item_type b) {
    if (a < b) {
        return LESS_THAN;
    }

    if (a > b) {
        return GREATER_THAN;
    }

    return EQUAL_TO;
}

void heapsort_(item_type s[], int n) {
    int i;
    priority_queue q;

    make_heap(&q, s, n);

    for (i = 0; i < n; i++) {
        s[i] = extract_min(&q);
    }
}

int binary_search(item_type s[], item_type key, int low, int high) {
    int middle;

    if (low > high) {
        return -1;
    }

    middle = (low + high) / 2;

    if (s[middle] == key) {
        return middle;
    }

    if (s[middle] > key) {
        return binary_search(s, key, low, middle - 1);
    } else {
        return binary_search(s, key, middle + 1, high);
    }
}

int main() {
    int s[NELEM + 2];
    int n;
    int i, j;

    for (i = 0; i < NELEM; i++) {
        s[i] = NELEM - i;
    }
    random_permutation(s, NELEM);

    heapsort_(s, NELEM);

    printf("\n\nHEAP sort: \n");
    for (i = 0; i < NELEM; i++) {
        printf("%d ", s[i]);
    }

    printf("\n");

    heapsort_(s, NELEM);
    for (i = 2; i < 2 * NELEM + 1; i += 2) {
        printf("%d found in %d\n", i, binary_search(s, i, 0, NELEM - 1));
    }

    return 0;
}