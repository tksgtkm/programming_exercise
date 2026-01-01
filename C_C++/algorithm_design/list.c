#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

#include "list.h"
#include "bool.h"

list *init_list() {
    return NULL;
}

bool empty_list(list *l) {
    if (l == NULL) {
        return TRUE;
    } else {
        return FALSE;
    }
}

list *search_list(list *l, item_type x) {
    if (l == NULL) {
        return NULL;
    }

    if (l->item == x) {
        return l;
    } else {
        return search_list(l->next, x);
    }
}

list *item_ahead(list *l, list *x) {
    if ((l == NULL) || (l->next == NULL)) {
        return NULL;
    }

    if (l->next == x) {
        return l;
    } else {
        return item_ahead(l->next, x);
    }
}

void insert_list(list **l, item_type x) {
    list *p;

    p = malloc(sizeof(list));
    p->item = x;
    p->next = *l;
    *l = p;
}

void print_list(list *l) {
    while (l != NULL) {
        printf("%d ", l->item);
        l = l->next;
    }
    printf("\n");
}

void delete_list(list **l, list **x) {
    list *p;
    list *pred;

    p = *l;
    pred = item_ahead(*l, *x);

    if (pred == NULL) {
        *l = p->next;
    } else {
        pred->next = (*x)->next;
    }
    free(*x);
}

int main() {
    char c;
    item_type d;
    list *l;
    list *tmp;
    
    l = init_list();

    while (scanf("%c", &c) != EOF) {
        if (tolower(c) == 'p') {
            print_list(l);
        }

        if (tolower(c) == 'i') {
            scanf("%d", &d);
            printf("new item: %d\n", d);
            insert_list(&l, d);
        }

        if (tolower(c) == 's') {
            scanf("%d", &d);
            tmp = search_list(l, d);
            if (tmp == NULL) {
                printf("item %d not found\n", d);
            } else {
                printf("item %d found\n", d);
            }
        }

        if (tolower(c) == 'd') {
            scanf("%d", &d);
            tmp = search_list(l, d);
            if (tmp == NULL) {
                printf("item to delete %d not found\n", d);
            } else {
                delete_list(&l, &tmp);
                printf("item %d dlete\n", d);
            }
        }
    }

    return 0;
}