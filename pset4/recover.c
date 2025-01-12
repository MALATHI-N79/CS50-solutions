#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

 int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
     if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];
     // Initialize file counter and file pointer
    int file_counter = 0;
    FILE *img = NULL;

    // Filename array
    char filename[8];

    // While there's still data left to read from the memory card
      while (fread(buffer, 1, 512, card) == 512)
    {
        // Check if the block indicates the start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If already processing a JPEG, close the previous file
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new JPEG file
            sprintf(filename, "%03i.jpg", file_counter);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create file.\n");
                return 1;
            }

            file_counter++;
        }

        // If a JPEG file is currently open, write the block to it
        if (img != NULL)
        {
            fwrite(buffer, 1, 512, img);
        }
    }

    // Close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);
    return 0;

}