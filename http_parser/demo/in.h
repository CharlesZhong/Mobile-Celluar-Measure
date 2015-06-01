#ifndef _IN_H_
#define _IN_H_


#define t_qp_bool int
#define QP_TRUE 1
#define QP_FALSE 0

extern t_qp_bool MaxUncompressedImageRatio;
extern t_qp_bool ConvertToGrayscale;
extern t_qp_bool AllowLookCh;

extern int WeiBoJpgWidth;
extern int WeiBoJpgDAR;
extern int WeiBoQuality;



#ifdef JP2K
extern t_qp_bool ProcessJP2, ForceOutputNoJP2, ProcessToJP2, AnnounceJP2Capability, JP2OutRequiresExpCap;
extern int JP2Colorspace_cfg;
extern t_color_space JP2Colorspace;	// 0=RGB 1=YUV
extern int JP2Upsampler_cfg;
extern t_upsampler JP2Upsampler;	// upsampler method: 0-linear, 1-lanczos
extern int JP2BitResYA[8];	// 4x qualities 2 components: YA YA YA YA
extern int JP2BitResRGBA[16];	// 4x qualities 4 components: RGBA RGBA RGBA RGBA
extern int JP2BitResYUVA[16];	// 4x qualities 4 components: YUVA YUVA YUVA YUVA
extern int JP2CSamplingYA[32];	// 4x qualities 2 components 4 settings: YxYyYwYh AxAyAwAh YxYyYwYh AxAyAwAh YxYyYwYh AxAyAwAh YxYyYwYh AxAyAwAh
extern int JP2CSamplingRGBA[64];	// 4x qualities 4 components 4 settings: RxRyRwRh GxGyGwGh BxByBwBh AxAyAwAh ... (4 times)
extern int JP2CSamplingYUVA[64];	// 4x qualities 4 components 4 settings: YxYyYwYh UxUyUwUh VxVyVwVh AxAyAwAh ... (4 times)
#endif


void debug_log_printf(const char *fmt, ...);
void debug_log_puts(const char *fmt, ...);

void error_log_printf(const char *fmt, ...);

void image_init();

extern int getImageQuality (int width, int height);
extern int getJP2ImageQuality (int width, int height);

const int *getJP2KBitLenYA (int width, int height);
const int *getJP2KBitLenRGBA (int width, int height);
const int *getJP2KBitLenYUVA (int width, int height);
const int *getJP2KCSamplingYA (int width, int height);
const int *getJP2KCSamplingRGBA (int width, int height);
const int *getJP2KCSamplingYUVA (int width, int height);



#endif
