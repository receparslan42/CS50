#include <stdio.h>
int main(){
    double change;
    int counter = 0,cent;

    do{
        printf("Please enter the change :");
        scanf("%lf",&change);
    }while(change <= 0);

    //Dolar to Cent
    cent = change*100;

    //Count
    counter+= cent/25;
    cent%=25;
    counter+= cent/10;
    cent%=10;
    counter+= cent/5;
    cent%=5;
    counter+= cent/1;

    //Print
    printf("%i \n",counter);
}
