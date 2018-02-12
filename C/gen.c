#include<stdio.h>
#include<math.h>
#include<complex.h>
#include<stdlib.h>
#include<stdint.h>
#include"paraments.h"
#define tlt 1.0
#define sps (int)floor(tlt*sp)
double complex gen(double t){
	return cexp(2*PI*k*(0+I)*pow(t,2));
}
double complex gen2(double t){
	return cexp(2*PI*(-k)*(0+I)*pow(t,2));
}
double complex streamgen(double tt){
	double ttt=fmod(tt,rt);
	int num=(int)floor(tt/rt);
	if(ttt<st){
		ttt=ttt-st/2;
		if(num%10==0)
			return gen2(ttt)*(alpha+beta*cos(2*PI*ttt/st));//hamming window
		else
			return gen(ttt)*(alpha+beta*cos(2*PI*ttt/st));
	}else
		return (0+0*I);
}
int size=1000000;
int main(int argc,char* argv[]){
	__int16_t *buffer=malloc(sizeof(__int16_t)*2*size);
	FILE* fp;
	fp=fopen(argv[1],"wb");
	double ii=0;
	double rr=0;
	complex double sg;
	long ft;
	for(ft=0;ft<sps;ft++){
		sg=streamgen(ft/sp-offset);
		rr=creal(sg);
		ii=cimag(sg);
		buffer[(ft%size)*2]=round(0.9*rr*pow(2,15));
		buffer[(ft%size)*2+1]=round(0.9*ii*pow(2,15));
		//printf("%d ",buffer[(2*ft)%size+1]);
		if(ft%size==size-1){
			fwrite(buffer,2*sizeof(__int16_t),size,fp);
		}
	}
	//fwrite(buffer,(ft%size)*2,1,fp);
	free(buffer);
	fclose(fp);
	//printf("%d",(int)sps);
	return 0;
}


