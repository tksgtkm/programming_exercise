MAKEFILE = Makefile

SOURCES = list.c binary_tree.c sorting.c priority_queue.c random.c \
		queue.c

OBJECTS = list.o binary_tree.o sorting.o priority_queue.o random.o \
		queue.o

BINARIES = list binary_tree sorting

INCLUDES = bool.h item.h list.h priority_queue.h queue.h random.h tree.h

CC = gcc
CFLAGS = -ggdb
LFLAGS = -lm

make: $(BINARIES)

$(OBJECTS):		$(INCLUDES)

$(OBJECTS):		$(MAKEFILE)

all:	$(BINARIES)

sorting: random.o queue.o priority_queue.o sorting.o
	$(CC) -o $@ random.o queue.o priority_queue.o sorting.o $(LFLAGS)

tree: binary_tree.o
	$(CC) -o $@ binary_tree.o $(LFLAGS)

lint:
	lint -h $(SOURCES)
	
clean:
	rm -f core *.o a.out $(BINARIES)
	rm -f ./tests/*.o