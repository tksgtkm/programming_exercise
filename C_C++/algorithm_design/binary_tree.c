#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

#include "bool.h"
#include "tree.h"

tree *parent;

tree *init_tree() {
    return NULL;
}

bool empty_tree(tree *t) {
    if (t == NULL) {
        return TRUE;
    }
    return FALSE;
}

tree *search_tree(tree *l, item_type x) {
    if (l == NULL) {
        return NULL;
    }

    if (l->item == x) {
        return l;
    }

    if (x < l->item) {
        return search_tree(l->left, x);
    } else {
        return search_tree(l->right, x);
    }
}

void insert_tree(tree **l, item_type x, tree *parent) {
    tree *p;

    if (*l == NULL) {
        p = malloc(sizeof(tree));
        p->item = x;
        p->left = p->right = NULL;
        p->parent = parent;
        *l = p;
        return;
    }

    if (x < (*l)->item) {
        insert_tree(&((*l)->left), x, *l);
    } else {
        insert_tree(&((*l)->right), x, *l);
    }
}

void print_tree(tree *l) {
    if (l != NULL) {
        print_tree(l->left);
        printf("%d ", l->item);
        print_tree(l->right);
    }
}

tree *successor_descendant(tree *t) {
    tree *succ;

    if (t->right == NULL) {
        return NULL;
    }

    succ = t->right;
    while (succ->left != NULL) {
        succ = succ->left;
    }

    return succ;
}

tree *find_minimum(tree *t) {
    tree *min;

    if (t == NULL) {
        return NULL;
    }

    min = t;
    while (min->left != NULL) {
        min = min->left;
    }
    return min;
}

tree *predecessor_descendant(tree *t) {
    tree *pred;

    if (t->left == NULL) {
        return NULL;
    }

    pred = t->left;
    while (pred->right != NULL) {
        pred = pred->right;
    }

    return pred;
}

tree *delete_tree(tree *t, item_type x) {
    tree *d;
    tree *p;
    item_type new_key;
    tree *child;
    tree *search_tree();

    d = search_tree(t, x);

    if (d == NULL) {
        printf("Warning: key to be deleted %d is not in tree.\n", x);
        return t;
    }

    if (d->parent == NULL) {
        if ((d->left == NULL) && (d->right == NULL)) {
            free(d);
            return NULL;
        }

        if (d->left != NULL) {
            p = predecessor_descendant(d);
        } else {
            p = successor_descendant(d);
        }
    } else {
        if ((d->left == NULL) || (d->right == NULL)) {
            if (d->left != NULL) {
                child = d->left;
            } else {
                child = d->right;
            }

            if ((d->parent)->left == d) {
                d->parent->left = child;
            } else {
                d->parent->right = child;
            }

            if (child != NULL) {
                child->parent = d->parent;
            }
            free(d);
            return t;
        } else {
            p = successor_descendant(d);
        }
    }

    new_key = p->item;
    delete_tree(t, p->item);
    d->item = new_key;
    return t;
}

int main() {
    char c;
    item_type d;
    tree *l;
    tree *tmp;
    tree *search_tree();
    void insert_tree();

    l = init_tree();

    while (scanf("%c", &c) != EOF) {
        if (tolower(c) == 'p') {
            print_tree(l);
            printf("\n");
        }

        if (tolower(c) == 'i') {
            scanf("%d", &d);
            printf("new item: %d\n", d);
            insert_tree(&l, d, NULL);
        }

        if (tolower(c) == 's') {
            scanf("%d", &d);
            tmp = search_tree(l, d);
            if (tmp == NULL) {
                printf("item %d not found\n", d);
            } else {
                printf("item %d found\n", d);
            }
        }

        if (tolower(c) == 'd') {
            scanf("%d", &d);
            printf(" deleting item %d\n", d);
            l = delete_tree(l, d);
            print_tree(l);
            printf("\n");
        }
    }

    return 0;
}