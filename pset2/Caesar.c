#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[]){

    //Check usage
    if(argc==2){
        int lenght = strlen(argv[1]);
        for(int i=0; i < lenght; i++){
            if(isdigit(argv[1][i]) == 0){
                printf("Usage: ./caesar key\n");
                    return 1;
            }
        }
    }else{
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //Define variable
    string plainText=get_string("plaintext: ");
    int key = atoi(argv[1]);
    int lenght = strlen(plainText);
    char cipherText[lenght+1];

    //Caesar password
    for(int i=0;i<lenght;i++){
        if(isalpha(plainText[i]) != 0){
            if(islower(plainText[i]) != 0){
                cipherText[i]=(plainText[i]%97+key)%26+97;
            }else{
                cipherText[i]=(plainText[i]%65+key)%26+65;
            }
        }else{
            cipherText[i]=plainText[i];
        }
    }

    //Print cipher text
    printf("ciphertext: ");

    for(int i=0;i<lenght;i++)
        printf("%c",cipherText[i]);

    printf("\n");
}