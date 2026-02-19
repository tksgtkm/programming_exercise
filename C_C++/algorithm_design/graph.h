#include "bool.h"

#define MAXV    100

#define _NULL   0

#define TREE    0
#define BACK    1
#define CROSS   2
#define FORWARD 3

typedef struct edgenode {
    int y;
    int weight;
    struct edgenode *next;
} edgenode;

typedef struct {
    edgenode *edges[MAXV+1];
    int degree[MAXV+1];
    int nvertices;
    int nedges;
    int directed;
} graph;

void process_vertex_early(int v);
void process_vertex_late(int v);
void process_edge(int x, int y);

void initialize_graph(graph *g, bool directed);
void read_graph(graph *g, bool directed);
void print_graph(graph *g);