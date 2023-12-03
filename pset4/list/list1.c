#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int numbers[3];
    
    for(int i=0;i<3;i++)
    {
        numbers[i]=get_int("Number: ");
    }
    
    for(int i=0;i<3;i++)
    {
        printf("You inputted: %i\n",numbers[i]);
    }
}