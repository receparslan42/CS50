#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int shift(char c);

int main(int argc, string argv[]){

    int keywordLenght;

    //Check usage
    if(argc==2){
        keywordLenght = strlen(argv[1]);

        for(int i=0; i < keywordLenght; i++){
            if(isalpha(argv[1][i]) == 0){
                printf("Usage: ./Vigenere keyword\n");
                return 1;
            }
        }
    }else{
        printf("Usage: ./Vigenere keyword\n");
        return 1;
    }

    //Define values
    string plainText = get_string("plaintext: ");
    int plainTextLenght = strlen(plainText);
    char cipherText[plainTextLenght+1];

    for(int i=0,l=0;i<plainTextLenght;i++){
        //Check end of the key
        if(l == keywordLenght){
            l = 0;
        }

        //Check digit for alphabet
        if(isalpha(plainText[i]) != 0){
            //Check if letter lowercase or uppercase 
            if(islower(plainText[i]) != 0){
                cipherText[i] = (plainText[i]%97+shift(argv[1][l]))%26+97;
            }else{
                cipherText[i] = (plainText[i]%65+shift(argv[1][l]))%26+65;
            }
            //Increase key
            l++;
        }else{
            cipherText[i]=plainText[i];
        }
    }
    // Print cipher text
    printf("ciphertext: ");

    for(int i=0;i<plainTextLenght;i++){
        printf("%c",cipherText[i]);
    }

    printf("\n");
}

//ASCII to decimal
int shift(char c){
    if(islower(c) != 0){
        return c%97;
    }else{
        return c%65;
    }
}
