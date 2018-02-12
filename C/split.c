#include<stdio.h>
#include<math.h>
#include<complex.h>
#include<stdlib.h>
#include<stdint.h>
#include"paraments.h"
#include"correlation.c"
#define nums 1000
int main(int argc,char *argv[]){
	int offt=0;
	if(argc!=3)
		return 0;
	offt=atoi(argv[2]);
	FILE* fp=fopen(argv[1],"rb");
	if(fp==NULL){
		printf("File doesn't exist");
		return 0;
	}
	
	int psps=(int)floor(sp*rt);
	int i=0;
	fseek(fp, 0L, SEEK_END);  
    int filesize = ftell(fp);
	int fsps=(int)floor(filesize/4);
	fseek(fp,offt*4,SEEK_SET);
	char filenames[nums][50];
	FILE* fps[nums];
	for(i=0;i<nums;i++){
		sprintf(filenames[i],"../signals/%05d.bin",i);
		fps[i]=fopen(filenames[i],"wb");
		if(fps[i]==NULL){
			printf("Create file faild\n");
			return 0;
		}
	}
	long j=0;
	__int16_t *buffer=malloc(4*psps);
	for(j=0;j<floor((fsps-offt)/psps);j++){
			fread(buffer,4,psps,fp);
		if(j%10!=0){
			fwrite(buffer,4,psps,fps[j%nums]);
		}
	}
	printf("ok\n");
	for(i=0;i<nums;i++){
		fclose(fps[i]);
	}
	fclose(fp);
	free(buffer);
	return 0;
}
	
	
		
	 
	
