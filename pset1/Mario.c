#include<stdio.h>
#include<cs50.h>

int main(){
    int height;

    //Get height
    do{
        height=get_int("Please enter a number from 1 to 8:");
    }while(height < 1 || height > 8);

    //Print built
    for(int i = height; i > 0 ; i--){

        for(int k = i-1;k > 0; k--)
            printf(" ");

        for(int l = 0; l < height -i+1 ; l++)
            printf("#");

        printf("\n");
    }
}