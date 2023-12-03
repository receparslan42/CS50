#include <stdio.h>
#include <cs50.h>

int main(){
    int height;

    //Get height
    do{
        height = get_int("Please enter a number from 1 to 8 :");
    }while(height < 1 || height > 8);

    for(int i = 1; i <= height; i++){
        for(int k = height-i; k > 0; k--)
            printf(" ");

        for(int k = 0; k < i; k++)
            printf("#");

        printf(" ");

        for(int k = 0; k < i; k++)
            printf("#");

        printf("\n");
    }
}