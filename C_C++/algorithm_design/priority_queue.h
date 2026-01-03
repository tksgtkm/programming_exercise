#include "item.h"

#define PQ_SIZE 1000

typedef struct {
    item_type q[PQ_SIZE+1];
    int n;
} priority_queue;

void pq_init(priority_queue *q);
int pq_parent(int n);
int pq_young_child(priority_queue *q, int i, int j);
void pq_swap(priority_queue *q, int i, int j);
void bubble_up(priority_queue *q, int p);
void bubble_down(priority_queue *q, int p);
void pq_insert(priority_queue *q, item_type x);
item_type extract_min(priority_queue *q);
int empty_pq(priority_queue *q);
void print_pq(priority_queue *q);
void make_heap(priority_queue *q, item_type s[], int n);
void make_heap1(priority_queue *q, item_type s[], int n);