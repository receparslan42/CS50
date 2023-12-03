#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    double n;
    
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }else{
        for(int i =0;i<strlen(argv[1]);i++){
            if(isdigit(argv[1][i]) == 0 && argv[1][i] != '.'){
                printf("n, the resize factor, must be an integer.\n");
                return 1;
            }    
        }
        n=atof(argv[1]);
        if(n > 100 || n < 0){
            printf("n, the resize factor, must satisfy 0 < n <=100.\n");
            return 1;
        }
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    int infilepadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    int oldWidth = bi.biWidth;
    int oldHeight = bi.biHeight;
    bi.biWidth = bi.biWidth*n;
    bi.biHeight = bi.biHeight*n;
    
    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    bi.biSizeImage = ((sizeof(RGBTRIPLE)*bi.biWidth)+padding)*abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage+sizeof(BITMAPFILEHEADER)+sizeof(BITMAPINFOHEADER);
    

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    int m = 0,check=0;
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // temporary storage
            RGBTRIPLE triple;
            
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            
            if(n > 1 ){
                if(check==0){
                    
                    // read RGB triple from infile
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                }
            }else{
                fread(&triple, sizeof(RGBTRIPLE),1 , inptr);
                fseek(inptr, sizeof(RGBTRIPLE)*(oldWidth/bi.biWidth-1),SEEK_CUR);
            }
            
            // write RGB triple to outfile
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr); 
            
            if(check < n-1 ){
                check++;
            }else{
                check=0;
            }
        }
        
        // skip over padding, if any
        fseek(inptr, infilepadding, SEEK_CUR);

        // then add it back (to demonstrate how)
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }
        
        if(n > 1){
             if(m<n-1){
                 fseek(inptr, -(bi.biWidth/n*sizeof(RGBTRIPLE)+infilepadding), SEEK_CUR);
                 m++;
             }else{
                 m=0;
             }
        }else{
            fseek(inptr, (sizeof(RGBTRIPLE)*oldWidth+infilepadding)*(oldHeight/bi.biHeight-1), SEEK_CUR);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
