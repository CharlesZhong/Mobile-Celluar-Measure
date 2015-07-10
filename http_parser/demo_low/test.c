#include <stdio.h>
#include <jpeglib.h>
#include <jpegint.h>
#include <jasper/jasper.h>



int compress_image(char *data)
{
	struct jpeg_compress_struct jcs;
	struct jpeg_error_mgr jem;
	
	jcs.err = jpeg_std_error(&jem);
	jpeg_create_compress(&jcs);
	
	FILE *f = fopen("6.png", "wb");
	if (!f) {
		printf("save error!\n");
		return -1;
	}
	
	jpeg_stdio_dest(&jcs, f);
	
	jcs.image_width = 145;
	jcs.image_height = 106;
    jcs.input_components = 3;
	jcs.in_color_space = JCS_RGB;
	
	jpeg_set_defaults(&jcs); 
	jpeg_set_quality (&jcs, 80, true);
	
	jpeg_start_compress(&jcs, TRUE);
	JSAMPROW row_pointer[1];

	int row_stride =  jcs.image_width * 3;
	
	while (jcs.next_scanline < jcs.image_height) {
       row_pointer[0] = & data[jcs.next_scanline * row_stride];
       jpeg_write_scanlines(&jcs, row_pointer, 1);
    }

   jpeg_finish_compress(&jcs);
   jpeg_destroy_compress(&jcs);
   fclose(f);
   return 0;
}

int main()
{
    struct jpeg_decompress_struct cinfo;
	struct jpeg_error_mgr jerr;
	
	cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_decompress(&cinfo);
	
	
    FILE *fp = fopen("6.jpg", "rb");
	if (!fp) {
		printf("fopen error!\n");
		return  -1;
	}
	
	jpeg_stdio_src(&cinfo, fp);
	jpeg_read_header(&cinfo, TRUE);
	
	jpeg_start_decompress(&cinfo);
	
	JSAMPROW row_pointer[1];
	
	char *data = malloc(cinfo.image_width*cinfo.image_height*cinfo.num_components);
	if (!data) {
		printf("malloc error!\n");
		return -1;
	}
	while (cinfo.output_scanline < cinfo.output_height)
	{
		row_pointer[0] = &data[(cinfo.output_height - cinfo.output_scanline - 1)* cinfo.image_width* cinfo.num_components];
		jpeg_read_scanlines(&cinfo, row_pointer, 1);
	}
	jpeg_finish_decompress(&cinfo);
	jpeg_destroy_decompress(&cinfo);
	fclose(fp);
	
		
	compress_image(data);
	
    return 0;
}