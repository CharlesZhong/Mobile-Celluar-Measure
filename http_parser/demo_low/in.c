#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include "image.h"
#include "jp2tools.h"
#include "in.h"

t_qp_bool MaxUncompressedImageRatio = 500;
t_qp_bool ConvertToGrayscale = QP_FALSE;
t_qp_bool AllowLookCh = QP_FALSE;


int WeiBoJpgWidth = 440;
int WeiBoJpgDAR = 1;
int WeiBoQuality = 75;

int ImageQuality[4] = { 30, 25, 25, 20 };
int ImageQualityHigh[4] = { 10,10,15,10 };
int ImageQualityLow[4] = { 10, 15, 15, 10 };


#ifdef JP2K
int JP2ImageQuality[4] = { 10, 15, 15, 10 };

t_qp_bool ProcessJP2, ForceOutputNoJP2, ProcessToJP2, AnnounceJP2Capability, JP2OutRequiresExpCap;
int JP2Colorspace_cfg;
t_color_space JP2Colorspace;	// 0=RGB 1=YUV
int JP2Upsampler_cfg;
t_upsampler JP2Upsampler;	// upsampler method: 0-linear, 1-lanczos
int JP2BitResYA[8] = { 6, 4, 7, 5, 8, 6, 8, 6 };	// 4x qualities 2 components: YA YA YA YA
int JP2BitResRGBA[16] = { 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8 };	// 4x qualities 4 components: RGBA RGBA RGBA RGBA
int JP2BitResYUVA[16] = { 6, 5, 5, 4, 7, 6, 6, 5, 8, 7, 7, 6, 8, 8, 8, 6 };	// 4x qualities 4 components: YUVA YUVA YUVA YUVA
int JP2CSamplingYA[32] = {0, 0, 1, 1,  0, 0, 1, 1, \
							0, 0, 1, 1,  0, 0, 1, 1, \
							0, 0, 1, 1,  0, 0, 2, 2, \
							0, 0, 1, 1,  0, 0, 2, 2 };	// 4x qualities 2 components 4 settings: YxYyYwYh AxAyAwAh YxYyYwYh AxAyAwAh YxYyYwYh AxAyAwAh YxYyYwYh AxAyAwAh
int JP2CSamplingRGBA[64] = { 0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1, \
							0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1, \
							0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1, \
							0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1 };	// 4x qualities 4 components 4 settings: RxRyRwRh GxGyGwGh BxByBwBh AxAyAwAh ... (4 times)
int JP2CSamplingYUVA[64] = { 0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1,  0, 0, 1, 1, \
							0, 0, 1, 1,  0, 0, 1, 2,  0, 0, 2, 1,  0, 0, 1, 1, \
							0, 0, 1, 1,  0, 0, 2, 2,  0, 0, 2, 1,  0, 0, 2, 2, \
							0, 0, 1, 1,  0, 0, 2, 2,  0, 0, 2, 2,  0, 0, 2, 2 };	// 4x qualities 4 components 4 settings: YxYyYwYh UxUyUwUh VxVyVwVh AxAyAwAh ... (4 times)
#endif


void image_init()
{
#ifdef JP2K
		ProcessJP2 = QP_FALSE;
		ForceOutputNoJP2 = QP_FALSE;
		ProcessToJP2 = QP_FALSE;
		AnnounceJP2Capability = QP_FALSE;
		JP2OutRequiresExpCap = QP_FALSE;
		JP2Colorspace_cfg = 1;	// defaults to YUV
		JP2Upsampler_cfg = 0; 	// defaults to linear

		switch (JP2Colorspace_cfg) {
			case 1:
				JP2Colorspace = CENC_YUV;
				break;
			case 0:
				JP2Colorspace = CENC_RGB;
				break;
			default:
				error_log_printf ("Configuration error: Invalid JP2Colorspace value: %d\n", JP2Colorspace_cfg);
				return;
				break;
		}
	
		switch (JP2Upsampler_cfg) {
			case 0:
				JP2Upsampler = UPS_LINEAR;
				break;
			case 1:
				JP2Upsampler = UPS_LANCZOS;
				break;
			default:
				error_log_printf ("Configuration error: Invalid JP2Upsampler value: %d\n", JP2Upsampler_cfg);
				break;
		}
	
#endif
}



/* get position in quality tables according to the image size */
int getImgSizeCategory (int width, int height)
{
	int imgcat;
	long i = width * height;
	
	if (i < 5000)
		imgcat = 0;
	else if ((i < 50000)|| (width < 150) || (height < 150))
		imgcat = 1;
	else if (i < 250000)
		imgcat = 2;
	else imgcat = 3;

	return (imgcat);
}

#ifdef JP2K

/* return a pointer to a array[4] with the bit lenght for JP2K YA components */
const int *getJP2KBitLenYA (int width, int height)
{
	int imgcat;

	imgcat = getImgSizeCategory (width, height);

	return (JP2BitResYA + (2 * imgcat));
}

/* return a pointer to a array[4] with the bit lenght for JP2K RGBA components */
const int *getJP2KBitLenRGBA (int width, int height)
{
	int imgcat;

	imgcat = getImgSizeCategory (width, height);

	return (JP2BitResRGBA + (4 * imgcat));
}

/* return a pointer to a array[4] with the bit lenght for JP2K YUVA components */
const int *getJP2KBitLenYUVA (int width, int height)
{
	int imgcat;

	imgcat = getImgSizeCategory (width, height);

	return (JP2BitResYUVA + (4 * imgcat));
}

/* return a pointer to a array[8] with the components' sampling parameters JP2K YA components */
const int *getJP2KCSamplingYA (int width, int height)
{
	int imgcat;

	imgcat = getImgSizeCategory (width, height);

	return (JP2CSamplingYA + (8 * imgcat));
}

/* return a pointer to a array[16] with the components' sampling parameters JP2K RGBA components */
const int *getJP2KCSamplingRGBA (int width, int height)
{
	int imgcat;

	imgcat = getImgSizeCategory (width, height);

	return (JP2CSamplingRGBA + (16 * imgcat));
}

/* return a pointer to a array[16] with the components' sampling parameters JP2K YUVA components */
const int *getJP2KCSamplingYUVA (int width, int height)
{
	int imgcat;

	imgcat = getImgSizeCategory (width, height);

	return (JP2CSamplingYUVA + (16 * imgcat));
}

/*
 * Fills in the values of JP2ImageQuality according to image dimensions. 
 * Returns index used to get the values ranging from 0 (smallest images)
 * to 3 (largest images).
 */
int getJP2ImageQuality (int width, int height)
{
	int imgcat;
	
	imgcat = getImgSizeCategory (width, height);
	return (JP2ImageQuality [imgcat]);
}

#endif

/*
 * Fills in the values of ImageQuality according to image dimensions. 
 * Returns index used to get the values ranging from 0 (smallest images)
 * to 3 (largest images).
 */
int getImageQuality (int width, int height)
{
	int imgcat;
	
	imgcat = getImgSizeCategory (width, height);
	return (ImageQuality [imgcat]);
}

void debug_log_printf(const char *fmt, ...)
{
}

void debug_log_puts(const char *fmt, ...)
{
}


void error_log_printf(const char *fmt, ...)
{
}
