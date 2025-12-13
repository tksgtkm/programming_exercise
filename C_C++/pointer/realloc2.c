#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int *ip = malloc(10 * sizeof *ip);

    int *new_ip = realloc(ip, 100 * sizeof *new_ip);

    printf("ip size: %p\n", ip);
    printf("new_ip size: %p\n", new_ip);

    ip = new_ip;

    free(ip);

    size_t old_size = 10 * sizeof * ip;
    size_t new_size = 10 * old_size;
    ip = malloc(old_size);
    if (!ip)
        exit(1);
    
    new_ip = malloc(new_size);
    memmove(new_ip, ip, old_size);
    free(ip);
    ip = new_ip;

    free(ip);

    return 0;
}