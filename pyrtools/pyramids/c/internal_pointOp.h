#ifdef _WIN32
#define LIBRARY_API __declspec(dllexport)
#else
#define LIBRARY_API 
#endif

LIBRARY_API  void internal_pointop(double *im, double *res, int size, double *lut, 
		      int lutsize, double origin, double increment, 
		      int warnings);
