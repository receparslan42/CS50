#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>

int main(void)
{
    int *numbers = NULL;
    int size=0;
    while(true)
    {
        int number = get_int("Number: ");
        
        if(number == INT_MAX)
        {
            break;
        }else
        {
            size++;
            numbers= realloc(numbers,sizeof(int)*size);
            numbers[size-1]=number;
        }
    }
    
    for(int i=0;i<size;i++)
    {
        printf("You inputted: %i\n",numbers[i]);
    }
    free(numbers);
}