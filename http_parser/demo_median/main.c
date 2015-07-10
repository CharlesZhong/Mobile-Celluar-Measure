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
	fseek(fp_in, 0, SEEK_END);
	ZP_DATASIZE_TYPE file_len = ftell(fp_in);
	fseek(fp_in, 0, SEEK_SET);

	char *buf = malloc(file_len);
	if (!buf)
		return -1;
	fread(buf, file_len, 1, fp_in);
	char *out_buf = NULL;
	ZP_DATASIZE_TYPE out_len = 0;
	compress_image(buf, file_len, &out_buf, &out_len);
	printf("out_len: %ld   src_len: %ld\n", out_len, file_len);


	FILE *fp_out = fopen(dst, "w");
	fwrite(out_buf, out_len, 1, fp_out);
	return 0;
	
}
