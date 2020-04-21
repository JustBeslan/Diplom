//---------------------------------------------------------------------------
//  VoiceSec module. FFT transform. 
//  10.2002
//
//  author email viman@pisem.net
//
//---------------------------------------------------------------------------

#include <vcl.h>
#include "fft.h"
#pragma hdrstop
#define WINDOW_RECTANGLE	0
#define WINDOW_HAMMING	1
#define WINDOW_BLACKMAN	2
#define WINDOW_BARTLETT	3
#define WINDOW_TRIANGLE	3
#define WINDOW_HANNING	4

#define MATH_PI	3.141592653589793


inline int	Round(double x) { return (int)(x+0.5); }
inline long double	sqr(long double x) { return x*x; }

int FFTSize;
#ifdef __cplusplus
extern "C" {
#endif
__declspec( dllexport )
void FFTC(Cmplx *X,int FFTSize)
{
	int	N, M, i, j, L, LE, LE2, ip, k, s;
	Cmplx t,z;
	RealData	UR, UI, SR, SI, TR, TI;

	N = FFTSize;
	M = Round(log(N)/log(2));
	// Bit-reverse
	i = 0;
	for (s=0;s<N-1;s++) {
		if (s<i) {
			t = *(X+i); *(X+i) = *(X+s); *(X+s) = t;
		}
		k = N >> 1;
		while (i&k) k >>= 1;
		i += k;
		k <<= 1;
		while (k<N) {
			i -= k;
			k <<= 1;
		}
	}
	// First pass
	for (i=0;i<N;i+=2) {
		t = *(X+i);
		(X+i)->Re = t.Re + (X+i+1)->Re;
		(X+i)->Im = t.Im + (X+i+1)->Im;
		(X+i+1)->Re = t.Re - (X+i+1)->Re;
		(X+i+1)->Im = t.Im - (X+i+1)->Im;
	}
	// Second pass
	for (i=0;i<N;i+=4) {
		t = *(X+i);
		(X+i)->Re = t.Re + (X+i+2)->Re;
		(X+i)->Im = t.Im + (X+i+2)->Im;
		(X+i+2)->Re = t.Re - (X+i+2)->Re;
		(X+i+2)->Im = t.Im - (X+i+2)->Im;
		t = *(X+i+1);
		z = *(X+i+3);
		(X+i+1)->Re = t.Re + z.Im;
		(X+i+1)->Im = t.Im - z.Re;
		(X+i+3)->Re = t.Re - z.Im;
		(X+i+3)->Im = t.Im + z.Re;
	}
	// Last passes
	for (L=3;L<=M;L++) {
		LE = 1 << L;
		LE2 = LE >> 1;
		UR = 1; UI = 0;
		SR = cos(MATH_PI/LE2);
		SI =	-sin(MATH_PI/LE2);
		for (j=0;j<LE2;j++) {
			for (i=j;i<N;i+=LE) {
				ip = i + LE2;
				TR = (X+ip)->Re*UR - (X+ip)->Im*UI;
				TI = (X+ip)->Re*UI + (X+ip)->Im*UR;
				(X+ip)->Re = (X+i)->Re - TR;
				(X+ip)->Im = (X+i)->Im - TI;
				(X+i)->Re = (X+i)->Re + TR;
				(X+i)->Im = (X+i)->Im + TI;
			}
			TR = UR;
			UR = TR*SR - UI*SI;
			UI = TR*SI + UI*SR;
		}
	}
}
}
#ifdef __cplusplus

#endif

#ifdef __cplusplus
extern "C" {
#endif
__declspec( dllexport )void
FFTR(Cmplx *X) {
	int	N, ND2, ND4;
	int	i, im, ip2, ipm, ip;
	RealData	UR, UI, SR, SI, TR, TI;
    FFTSize=256;
	// Separate even and odd points
	N = FFTSize;
	ND2 = N>>1;
	ND4 = ND2>>1;
	for (i=0;i<ND2;i++) {
		(X+i)->Re = (X+(i<<1))->Re;
		(X+i)->Im = (X+(i<<1)+1)->Re;
	}
	// Calculate N/2 point FFT
	FFTSize = ND2;
	FFTC(X,FFTSize);
	FFTSize = N;
	// Even/odd frequency domain decomposition
	for (i=1;i<ND4;i++) {
		im = ND2 - i;
		ip2 = i + ND2;
		ipm = im + ND2;
		(X+ipm)->Re = (X+ip2)->Re = ((X+i)->Im + (X+im)->Im)*0.5;
		(X+ip2)->Im = ((X+i)->Re - (X+im)->Re)*(-0.5);
		(X+ipm)->Im =  - (X+ip2)->Im;
		(X+im)->Re = (X+i)->Re = ((X+i)->Re + (X+im)->Re)*0.5;
		(X+i)->Im = ((X+i)->Im - (X+im)->Im)*0.5;
		(X+im)->Im = - (X+i)->Im;
	}
	(X+N*3/4)->Re = (X+ND4)->Im;
	(X+ND2)->Re = X->Im;
	(X+ND2+ND4)->Im = (X+ND2)->Im = (X+ND4)->Im = X->Im = 0;
	// Complete the last FFT stage
	// First step: calculate X[0] and X[N/2]
	TR = (X+ND2)->Re;
	TI = (X+ND2)->Im;
	(X+ND2)->Re = X->Re - TR;
	(X+ND2)->Im = X->Im - TI;
	X->Re = X->Re + TR;
	X->Im = X->Im + TI;
	// Other steps
	UR = SR = cos(MATH_PI/ND2);
	UI = SI = -sin(MATH_PI/ND2);
	ip = ND2+1;
	for (i=1;i<ND2;i++,ip++) {
		TR = (X+ip)->Re*UR - (X+ip)->Im*UI;
		TI = (X+ip)->Re*UI + (X+ip)->Im*UR;
		(X+ip)->Re = (X+i)->Re - TR;
		(X+ip)->Im = (X+i)->Im - TI;
		(X+i)->Re = (X+i)->Re + TR;
		(X+i)->Im = (X+i)->Im + TI;
		(X+i)->Re = (X+i)->Re + (X+ip)->Re*UR - (X+ip)->Im*UI;
		(X+i)->Im = (X+i)->Im + (X+ip)->Re*UI + (X+ip)->Im*UR;
		TR = UR;
		UR = TR*SR - UI*SI;
		UI = TR*SI + UI*SR;
	}
}}
#ifdef __cplusplus

#endif


//---------------------------------------------------------------------------
int WINAPI DllEntryPoint(HINSTANCE hinst, unsigned long reason, void*)
{
    return 1;
}
//---------------------------------------------------------------------------



