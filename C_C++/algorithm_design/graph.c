#include <stdio.h>
#include <stdlib.h>

#include "queue.h"
#include "graph.h"

void initialize_graph(graph *g, bool directed) {
    int i;

    g->nvertices = 0;
    g->nedges = 0;
    g->directed = directed;

    for (i = 1; i <= MAXV; i++) {
        g->degree[i] = 0;
    }

    for (i = 1; i <= MAXV; i++) {
        g->edges[i] = _NULL;
    }
}

void insert_edge(graph *g, int x, int y, bool directed) {
    edgenode *p;

    p = malloc(sizeof(edgenode));

    p->weight = _NULL;
    p->y = y;
    p->next = g->edges[x];

    g->edges[x] = p;

    g->degree[x]++;

    if (directed == FALSE) {
        insert_edge(g, y, x, TRUE);
    } else {
        g->nedges++;
    }
}

void read_graph(graph *g, bool directed) {
    int i;
    int m;
    int x, y;

    initialize_graph(g, directed);

    scanf("%d %d", &(g->nvertices), &m);

    for (i = 1; i <= m; i++) {
        scanf("%d %d", &x, &y);
        insert_edge(g, x, y, directed);
    }
}

void delete_graph(graph *g, int x, int y, bool directed) {
    int i;
    edgenode *p, *p_back;

    p = g->edges[x];
    p_back = _NULL;

    while (p != _NULL) {
        if (p->y == y) {
            g->degree[x]--;
            if (p_back != _NULL) {
                p_back->next = p->next;
            } else {
                g->edges[x] = p->next;
            }
            free(p);
            if (directed == FALSE) {
                delete_graph(g, x, y, TRUE);
            } else {
                g->nedges--;
            }
            return;
        } else {
            p = p->next;
        }
    }
    printf("Warning: deletion(%d, %d) not found in g\n", x, y);
}

void print_graph(graph *g) {
    int i;
    edgenode *p;

    for (i = 1; i <= g->nvertices; i++) {
        printf("%d: ", i);
        p = g->edges[i];
        while (p != _NULL) {
            printf(" %d", p->y);
            p = p->next;
        }
        printf("\n");
    }
}