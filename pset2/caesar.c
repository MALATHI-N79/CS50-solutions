// Program to take in a key and a plaintext to convert it to ciphertext
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// taking in command line argument
int main(int argc, string argv[])
{
    // if no command line argument presented, return error and exit
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0, length = strlen(argv[1]); i <= length; i++)
    {
        // to keep key strictly numeric
        if (isalpha(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    // convert argv string to decimal
    int k = atoi(argv[1]);
    if (k < 0)
    {
        // if negative numbers, exit
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        string plain = get_string("Plaintext:");
        printf("ciphertext: ");
        for (int i = 0; i < strlen(plain); i++)
        {
            char c = plain[i];
            // checking for upper and lower case letters to maintain the format
            if (isupper(c))
            {
                char newC = (((c - 65) + k) % 26 + 65);
                printf("%c", newC);
            }
            else if (islower(c))
            {
                char newC = (((c - 97) + k) % 26 + 97);
                printf("%c", newC);
            }
            // printing extra characters as it is.
            else
            {
                printf("%c", c);
            }
        }
        printf("\n");
        return 0;
    }
}