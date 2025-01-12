#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int compute(string word)
{
    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int scores = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        if (isupper(word[i]))
            scores += points[word[i] - 'A'];
        else if (islower(word[i]))
            scores += points[word[i] - 'a'];
    }
    return scores;
}

int main(void)
{
    string player1, player2;

    player1 = get_string("Player 1: \n");
    player2 = get_string("Player 2: \n");

    int score1 = compute(player1);
    int score2 = compute(player2);
    if (score1 > score2)
        printf("Player 1 wins!\n");
    else if (score2 > score1)
        printf("Player 2 wins!\n");
    else
        printf("Tie\n");
}