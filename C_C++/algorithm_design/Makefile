all: list

OPTS = -g -Wall -Wno-pointer-sign

list: list.c list.h bool.h item.h
		gcc -o list $(OPTS) list.c

clean:
	rm -f list