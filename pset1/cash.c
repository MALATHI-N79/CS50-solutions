#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int arr[4] = {1, 5, 10, 25};
    int ans[100];
    int m = sizeof(arr) / sizeof(arr[0]);

    // Prompt the user for the pyramid's height
    int n;
    do
    {
        n = get_int("Change owed: ");
    }
    while (n < 0);

    int k = 0;
    for (int i = m - 1; i >= 0; i--)
    {
        while (n >= arr[i])
        {
            n -= arr[i];
            ans[k++] = arr[i];
        }
    }

    printf("Coins used:\n");
    for (int j = 0; j < k; j++)
    {
        printf("%d ", ans[j]);
    }
    printf("\n");
    printf("The minimum number of coins is %d\n", k);
    printf("The coins are: ");
    for (int i = 0; i < k; i++)
    {
        printf("%d ", ans[i]);
    }
    printf("\n");
}