#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include "image.h"
#include "jp2tools.h"
#include "in.h"




int main(int argc, char **argv)
{
	char c = 0;
	char *filename = NULL;
	char *dst = NULL;
	while( (c = getopt(argc, argv, "f:o:")) != -1)
	{
		switch(c)	
		{
			case 'f':
				filename = optarg;
				break;
			case 'o':
				dst = optarg;
				break;
		}
	}
	if (!filename)
		return -1;
	if (!dst)
		dst = "test.jpg";
	
    image_init();
	FILE *fp_in = fopen(filename, "r");
	if (!fp_in)
		return -1;
	//
	fseek(fp_in, 0, SEEK_END);
	ZP_DATASIZE_TYPE file_len1 = ftell(fp_in);
	fseek(fp_in, 0, SEEK_SET);

	char *buf1 = malloc(file_len1);
	if (!buf1)
		return -1;
	fread(buf1, file_len1, 1, fp_in);
	char *out_buf1 = NULL;
	ZP_DATASIZE_TYPE out_len1 = 0;
	compress_image(buf1, file_len1, &out_buf1, &out_len1, 1);
	printf("high: out_len: %ld   src_len: %ld\n", out_len1, file_len1);

	FILE *fp_out1 = fopen("test_high.jpeg", "w");
	fwrite(out_buf1, out_len1, 1, fp_out1);

	///////////////
	fseek(fp_in, 0, SEEK_END);
	ZP_DATASIZE_TYPE file_len2 = ftell(fp_in);
	fseek(fp_in, 0, SEEK_SET);

	char *buf2 = malloc(file_len2);
	if (!buf2)
		return -1;
	fread(buf2, file_len2, 1, fp_in);
	char *out_buf2 = NULL;
	ZP_DATASIZE_TYPE out_len2 = 0;
	compress_image(buf2, file_len2, &out_buf2, &out_len2,2);
	printf("median out_len: %ld   src_len: %ld\n", out_len2, file_len2);


	FILE *fp_out2 = fopen("test_median.jpg", "w");
	fwrite(out_buf2, out_len2, 1, fp_out2);

	/////
	fseek(fp_in, 0, SEEK_END);
	ZP_DATASIZE_TYPE file_len3 = ftell(fp_in);
	fseek(fp_in, 0, SEEK_SET);

	char *buf3 = malloc(file_len3);
	if (!buf3)
		return -1;
	fread(buf3, file_len3, 1, fp_in);
	char *out_buf3 = NULL;
	ZP_DATASIZE_TYPE out_len3 = 0;
	compress_image(buf3, file_len3, &out_buf3, &out_len3,3);
	printf("low out_len: %ld   src_len: %ld\n", out_len3, file_len3);


	FILE *fp_out3 = fopen("test_low.jpg", "w");
	fwrite(out_buf3, out_len3, 1, fp_out3);




	return 0;
	
}
