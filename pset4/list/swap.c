#include <stdio.h>
#include <stdlib.h>

void swap();
int main(void)
{
    int n=1;
    int a[n];
    a[0]=1;
    a[1]=2;
}
void swap(int *a, int *b)
{
    int tmp = *a;
    *a=*b;
    *b=tmp;
}