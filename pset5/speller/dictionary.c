#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <strings.h> // Include for strcasecmp
#include <stdbool.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Global variable for word count
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to obtain a hash value
    unsigned int index = hash(word);

    // Search the hash table at the location specified by the word's hash value
    node *cursor = table[index];
    while (cursor != NULL)
    {
        // Compare the word with the current node's word (case-insensitively)
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    // Return false if no word is found
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 0;
    int c;
    // Iterate through each character in the word
    while ((c = *word++))
    {
        hash = hash * 31 + tolower(c);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    // Create a buffer to store words
    char word[LENGTH + 1];

    // Read each word in the file
    while (fscanf(source, "%s", word) != EOF)
    {
        // Create a new node for each word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, word);
        new_node->next = NULL;

        // Hash the word to obtain a hash value
        unsigned int index = hash(word);

        // Insert node into hash table
        new_node->next = table[index];
        table[index] = new_node;

        // Increment word count
        word_count++;
    }

    // Close the dictionary file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Loop through each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        // Traverse the linked list in each bucket
        node *cursor = table[i];
        while (cursor != NULL)
        {
            // Keep track of the next node
            node *temp = cursor->next;
            // Free the current node
            free(cursor);
            // Move to the next node
            cursor = temp;
        }
    }
    return true;
}