#include <stdio.h>

int main() {
    int num = 5; 
    int *pi = &num;
    printf("Address of num: %ld Value: %d\n", &num, num);
    printf("Address of pi: %ld num address Value: %ld Value: %d\n", &pi, pi, *pi);

    *pi = 200;
    printf("Value of num: %d\n", num);
    printf("Value of pi: %d\n", *pi);
}