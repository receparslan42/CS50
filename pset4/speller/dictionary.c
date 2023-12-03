// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}node;

int sizeOfDictionary = 0;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
        hashtable[i] = malloc(sizeof(node));
        if(hashtable[i] == NULL){
            return 1;
        }
        hashtable[i] ->word[0] = 'a'+i;
        hashtable[i] ->next = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        bool check = true;
        for(int i = 0; word[i] != '\0'; i++)
        {
            word[i] = tolower(word[i]);
        }
        if(check)
        {
            sizeOfDictionary++;
            node *newNode = malloc(sizeof(node));
            if(!newNode)
                return 1;
                
            int i=0;
            for(; word[i] != '\0'; i++)
            {
                newNode -> word[i] = word[i];
            }
            newNode -> word[i] ='\0';
            newNode -> next = hashtable[word[0]%96-1]->next;
            
            hashtable[word[0]%96-1]->next = newNode;
        }
    }
    
    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
      return sizeOfDictionary;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    char word2[strlen(word)+1];
    
    for(int i=0; i<= strlen(word);i++){
        word2[i]= tolower(word[i]);
    }
    
    for(node *ptr = hashtable[word2[0]%96-1]->next;ptr != NULL; ptr = ptr->next)
    {
        if(strcmp(word2,ptr->word)==0)
        {
            return true;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    
    int counter =0;for(int i=0; i<26; i++){
        node *cursor = hashtable[i];
        while(cursor != NULL){
            node *temp= cursor;
            cursor = cursor ->next;
            free(temp);
        }
    }
    return true;
}
