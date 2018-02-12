int correlation(double complex *f,int sizef,double complex *h,int sizeh,double complex *out,int size){//size must >sizef-sizeh and sizef>=sizeh
	if(sizef<sizeh||size<sizef-sizeh)
		return -1;
	int i;
	for(i=0;i<=sizef-sizeh;i++){
		int j;
		for(j=0;j<sizeh;j++){	
			out[i]=f[i+j]*conj(h[j])+out[i];
		}
	}
	return 0;
}
