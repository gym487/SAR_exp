#include<stdio.h>
#include<math.h>
#include<complex.h>
#include<stdlib.h>
#include<stdint.h>
#include"paraments.h"
#include"correlation.c"
#define tlt 1e-2
double complex gen(double t){
	return cexp(2*PI*k*(0+I)*pow(t,2));
}
double complex gen2(double t){
	return cexp(2*PI*(-k)*(0+I)*pow(t,2));
}
double complex sgen(double tt){
	double ttt=fmod(tt,rt);
	int num=(int)floor(tt/rt);
	if(ttt<st){
		ttt=ttt-st/2;
		if(num%10==0)
			return gen2(ttt)*(alpha+beta*cos(2*PI*ttt/st));//hamming window
		else
			return (0+0*I);
	}else
		return (0+0*I);
}
int main(int argc,char *argv[]){
	long offt=0;
	if(argc<2) return 0;
	if(argc==3)
		offt=atoi(argv[2]);
	int sps=(int)floor(tlt*sp);
	int spss=sps-(int)floor(sp*10*rt);
	double complex *sig=malloc(sizeof(double complex)*sps);
	double complex *filt=malloc(sizeof(double complex)*spss);
	double complex *corr=malloc(sizeof(double complex)*(sps-spss+1));
	__int16_t *buffer=malloc(sizeof(__int16_t)*2*sps);
	long i;
	FILE* fp=fopen(argv[1],"rb");
	if(fp==NULL){
		printf("File doesn't exist");
		return 0;
	}
	fseek(fp,offt*4,SEEK_SET);
	fread(buffer,sps,2*sizeof(__int16_t),fp);
	fclose(fp);
	for(i=0;i<sps;i++){
		sig[i]=((double)buffer[2*i])/pow(2,15)+(((double)buffer[2*i+1])/pow(2,15))*I;
		//printf("%f ",((double)buffer[2*i])/pow(2,15));
	}
	for(i=0;i<spss;i++){
		filt[i]=sgen((i+offt)/sp);	
	}
	correlation(sig,sps,filt,spss,corr,(sps-spss+1));
	double max=0;
	int maxindex=0;
	for(i=0;i<(sps-spss+1);i++){
		if(cabs(corr[i]/spss)>max){
			max=cabs(corr[i])/spss;
			maxindex=i;
		}	
	}
	printf("%d,%f\n%f\n%f",maxindex,max,maxindex/sp,offset+st/2);
	free(sig);
	free(filt);
	free(corr);
	return 0;
}
	
