#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
 
int main(int argc, char *argv[])
{
    //ensure proper usage
    if(argc!=2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }
    
    // open input file (forensic image)
    FILE *inptr = fopen(argv[1], "r");
    if(inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }
    
    //set outfile pointer to NULL
    FILE *outptr = NULL;
    
    //create an array of 512 elements to store 512 bytes from the memory card
    BYTE buffer[512];
    
    //string to hold a filename
    char filename[8];
    
    //count amount of jpeg files found
    int jpegcounter=0;
    
    while(fread(buffer, sizeof(BYTE),512,inptr)==512)
    {
        // checks if start of img in buffer
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            // if start of img and first image i.e. jpegcounter ==0
            // then begins writing a new image
            if (jpegcounter == 0)
            {
                sprintf(filename, "%03i.jpg", jpegcounter);
                outptr = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, outptr);
                jpegcounter += 1;
            }
            // if start of img but not first image then
            // closes the image and begins writing new image
            else if (jpegcounter > 0)
            {
                fclose(outptr);
                sprintf(filename, "%03i.jpg", jpegcounter);
                outptr = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, outptr);
                jpegcounter += 1;
            }
        }
        // if not start of new img
        // then it keeps on writing the image
        else if (jpegcounter > 0)
        {
            fwrite(&buffer, sizeof(BYTE), 512, outptr);
        }
    }
    
    // Close file
    fclose(inptr);
    fclose(outptr);
}