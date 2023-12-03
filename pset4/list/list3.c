#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>

typedef struct node
{
    int number;
    struct node *next;
}node;

int main(void)
{
    node *first = NULL;
    
    while(true){
        int number = get_int("Number: ");
        
        if(number== INT_MAX)
            break;
        
        node *setNode = malloc(sizeof(node));
        
        if(!setNode)
            return 1;
            
        setNode -> number = number;
        setNode -> next = NULL;
        
        if(!first)
        {
            first = setNode;
        }else{
            node *ptr = first;
            for(;ptr->next != NULL; ptr=ptr->next);
            ptr->next=setNode;
        }
    }
    
    for(node *ptr = first;ptr != NULL; ptr = ptr->next)
    {
        printf("You inputted: %i\n",ptr->number);
    }
}