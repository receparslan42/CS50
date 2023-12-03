#include <stdio.h>
#include <cs50.h>

int main(){
    long int cardNumber;
    int cardNumberArray[17],digitsNumber=0,sum=0,check=0;

    do{
        cardNumber = get_long("Please enter the card number :");
    }while(cardNumber <= 0);

    //Make Array
    for(;cardNumber > 0;cardNumber/=10){
        cardNumberArray[digitsNumber]=cardNumber%10;
        digitsNumber++;
    }

    //VISA=1, AMEX=2, MASTERCARD=3
    if(digitsNumber == 13){
        if(cardNumberArray[15] == 4){
            //VISA
            check=1;
        }
    }else if(digitsNumber == 15){
        if(cardNumberArray[14] == 3){
            if(cardNumberArray[13] == 4 || cardNumberArray[13] == 7){
                //AMEX
                check=2;
            }
        }
    }else if(digitsNumber == 16){
        if(cardNumberArray[15] == 4){
            //VISA
            check=1;
        }else if(cardNumberArray[15] == 5){
            if(cardNumberArray[14] == 1 || cardNumberArray[14] == 2 || cardNumberArray[14] == 3 || cardNumberArray[14] == 4 || cardNumberArray[14] == 5){
                //MASTERCARD
                check=3;
            }
        }
    }

    if(check == 1 || check == 2 ||check == 3){
        //Sum digits
        for(int i=0;i<=digitsNumber-1;i++){
            if(i%2 == 0){
                sum+=cardNumberArray[i];
            }else{
                if(cardNumberArray[i]*2 >=10){
                    sum+=cardNumberArray[i]*2/10;
                    sum+=cardNumberArray[i]*2%10;
                }else{
                    sum+=cardNumberArray[i]*2;
                }
            }
        }

        //Check Luhn logaritma
        if(sum%10==0){
            if(check == 2)
                printf("AMEX\n");
            else if(check == 1)
                printf("VISA\n");
            else
                printf("MASTERCARD\n");
        }else{
            printf("INVALID\n");
        }
    }else{
        printf("INVALID\n");
    }
}