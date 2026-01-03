all: list tree

OPTS = -g -Wall -Wno-pointer-sign

list: list.c list.h bool.h item.h
		gcc -o list $(OPTS) list.c

tree: binary_tree.c tree.h item.h bool.h
		gcc -o tree $(OPTS) binary_tree.c

clean:
	rm -f list