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

void insertion_sort(item_type s[], int n) {
    int i, j;

    for (i = 1; i < n; i++) {
        j = i;
        while ((j > 0) && (s[j] < s[j - 1])) {
            swap(&s[j], &s[j - 1]);
            j = j - 1;
        }
    }
}

void selection_sort(item_type s[], int n) {
    int i, j;
    int min;

    for (i = 0; i < n; i++) {
        min = i;
        for (j = i + 1; j < n; j++) {
            if (s[j] < s[min]) {
                min = j;
            }
        }
        swap(&s[i], &s[min]);
    }
}

int partition(item_type s[], int l, int h) {
    int i;
    int p;
    int firsthigh;

    p = h;
    firsthigh = l;
    for (i = l; i < h; i++) {
        if (s[i] < s[p]) {
            swap(&s[i], &s[firsthigh]);
            firsthigh++;
        }
    }
    swap(&s[p], &s[firsthigh]);

    return firsthigh;
}

void quicksort(item_type s[], int l, int h) {
    int p;

    if ((h - l) > 0) {
        p = partition(s, l, h);
        quicksort(s, l, p - 1);
        quicksort(s, p + 1, h);
    }
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

void merge(item_type s[], int low, int middle, int high) {
    int i;
    queue buffer1, buffer2;

    init_queue(&buffer1);
    init_queue(&buffer2);

    for (i = low; i <= middle; i++) {
        enqueue(&buffer1, s[i]);
    }

    for (i = middle + 1; i <= high; i++) {
        enqueue(&buffer2, s[i]);
    }

    i = low;
    while (!(empty_queue(&buffer1) || empty_queue(&buffer2))) {
        if (headq(&buffer1) <= headq(&buffer2)) {
            s[i++] = dequeue(&buffer1);
        } else {
            s[i++] = dequeue(&buffer2);
        }
    }

    while (!empty_queue(&buffer1)) {
        s[i++] = dequeue(&buffer1);
    }

    while (!empty_queue(&buffer2)) {
        s[i++] = dequeue(&buffer2);
    }
}

void mergesort_(item_type s[], int low, int high) {
    int i;
    int middle;

    if (low < high) {
        middle = (low + high) / 2;
        mergesort_(s, low, middle);
        mergesort_(s, middle + 1, high);

        merge(s, low, middle, high);
    }
}

int main() {
    int s[NELEM + 2];
    int n;
    int i, j;

    /* ---------- */
    for (i = 0; i < NELEM; i++) {
        s[i] = NELEM - i;
    }
    random_permutation(s, NELEM);

    insertion_sort(s, NELEM);

    printf("\n\nInsertion sort: \n");
    for (i = 0; i < NELEM; i++) {
        printf("%d ", s[i]);
    }

    /* ---------- */
    for (i = 0; i < NELEM; i++) {
        s[i] = NELEM - i;
    }
    random_permutation(s, NELEM);

    selection_sort(s, NELEM);

    printf("\n\nSelection sort: \n");
    for (i = 0; i < NELEM; i++) {
        printf("%d ", s[i]);
    }

    /* ---------- */
    for (i = 0; i < NELEM; i++) {
        s[i] = NELEM - i;
    }
    random_permutation(s, NELEM);

    quicksort(s, 0, NELEM - 1);

    printf("\n\nQuick sort: \n");
    for (i = 0; i < NELEM; i++) {
        printf("%d ", s[i]);
    }

    /* ---------- */
    for (i = 0; i < NELEM; i++) {
        s[i] = NELEM - i;
    }
    random_permutation(s, NELEM);

    heapsort_(s, NELEM);

    printf("\n\nHeapsort: \n");
    for (i = 0; i < NELEM; i++) {
        printf("%d ", s[i]);
    }

    /* ---------- */
    for (i = 0; i < NELEM; i++) {
        s[i] = NELEM - i;
    }
    random_permutation(s, NELEM);

    mergesort_(s, 0, NELEM - 1);
    printf("\n\nMergesort: \n");
    for (i = 0; i < NELEM; i++) {
        printf("%d ", s[i]);
    }

    /* ---------- */
    printf("\n");

    printf("\n");

    printf("Binary Search: \n");
    for (i = 0; i < NELEM; i++) {
        s[i] = 2 * (NELEM - i);
    }
    random_permutation(s, NELEM);

    heapsort_(s, NELEM);
    for (i = 2; i < 2 * NELEM + 1; i += 2) {
        printf("%d found in %d\n", i, binary_search(s, i, 0, NELEM - 1));
    }

    return 0;
}