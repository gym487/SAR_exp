from numpy import *
from math import *
from scipy.misc import imsave
import scipy
from scipy import signal
import time
h=100
lmin=100
l=800
x=500
dx=0.05
dl=0.5
k=1e8
c=3e8
bw=2e7
st=bw/k
sp=1.5e7
freq=1e9
pwr=100
tm=2e-5
slen=tm*sp
dt=1/sp
v=1
sst=dx/v
sp2=1e5
dtt=1/sp2

def signalr(t,par):
	tt=pi*k*pow((t%st)-st/2,2)
	#print t
	return complex(cos(tt+par),sin(tt+par))
print slen
print "1"
stp=time.time()
snls=zeros(int(sp*st),dtype=complex)
for i in  range(len(snls)):
	snls[i]=signalr(i*dt,0)
rx=zeros(int(sst*sp),dtype=complex)
tx=zeros(int(sst*sp),dtype=complex)
mix=zeros(int(sst*sp),dtype=complex)
mixx=zeros(int(sst*sp2),dtype=complex)
mixx2=zeros(int(sst*sp2),dtype=complex)
def r2i(r):
	return 2*r*sp2/(c)
snlr=zeros([int(x/dx),len(mixx)],dtype=complex)
#snl2=zeros([int(x/dx),int(slen)],dtype=complex)
#snl3=zeros([int(x/dx),int(slen)],dtype=complex)
def PointTarget(i,t,px,py):
	tt=sst*i+t
	x=i*dx+t*v
	rr=sqrt(pow(h,2)+pow(px,2)+pow(x-py,2))
	tos=2*rr/c
	return signalr(tt-tos,-2*pi*tos*freq)/pow(rr,4)

def i2r(i):
	return i*c/(2*k*sst)
print str(len(mixx))+"to"+str(len(snlr[1]))
for i in  range(len(snlr)):
	for j in  range(len(mixx)):
		mixx[j]=(PointTarget(i,j*dtt,lmin+l/2,x/2)+PointTarget(i,j*dtt,lmin+l/2,x/2+100)+PointTarget(i,j*dtt,lmin+l/2+100,x/2))*conjugate(signalr(i*sst+j*dtt,0))
		#mixx2[j]=signalr(sst*i+j*dtt,0)
		#print mixx[j]
	mixx=fft.fftshift(fft.fft(mixx))
	for j in range(len(mixx)):
		ph=-pi*pow((j-len(mixx)/2)*sp2/len(mixx),2)/k
		mixx[j]=mixx[j]*complex(cos(ph),sin(ph))
	snlr[i]=fft.ifft(fft.ifftshift(mixx))
	print "i:"+str(i)
		#print j
imsave("test.bmp",real(snlr));
print time.time()-stp
print "2"
#for i in range(len(snlr)):
#	snl2[i]=convolve(snlr[i],flipud(conjugate(snls)),'same')
#imsave("test2.bmp",real(snl2));
print time.time()-stp
print "3"
snl3=fft.fftshift(fft.fft(snlr,axis=0),axes=0)## range doppler
imsave("test3.bmp",real(snl3));
print time.time()-stp
print "4"
def rcmc(ll,fr):
	if(((2*freq+c*fr)*(2*freq-c*fr)*(pow(h,2)+pow(ll,2)))>0):
		a=-(2*c*fr*sqrt(((2*freq+c*fr)*(2*freq-c*fr)*(pow(h,2)+pow(ll,2)))/4))/(-pow(c,2)*pow(fr,2)+4*pow(freq,2))
		rrr=sqrt(pow(ll,2)+pow(h,2)+pow(a,2))
		return rrr
	else:
		return (-1)

snl4=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(snl4)):
	for j in range(len(snl4[i])):
		#print i,j,j*dl+lmin,(i*dx/x-0.5)/dx
		if(len(snl3[i])>int(r2i(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))) and int(r2i(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx)))>=0):
			snl4[i][j]=snl3[i][int(r2i(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx)))]
imsave("test4.bmp",real(snl4));
print time.time()-stp
print "5"
snl5=fft.ifft(fft.ifftshift(snl4,axes=0),axis=0)
imsave("test5.bmp",real(snl5));
print time.time()-stp
print "6"
filt=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(filt)):
	for j in range(len(filt[i])):
		rrr=sqrt(pow(j*dl+lmin,2)+pow(h,2)+pow((i*dx)-x/2,2))
		tos=2*rrr/c
		par=-tos*2*pi*freq
		filt[i][j]=complex(cos(par),sin(par))
imsave("filt.bmp",real(filt));
snl6=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(snl6[0])):
	snl6[:,i]=convolve(snl5[:,i],flipud(conjugate(filt[:,i])),'same')
imsave("test6.bmp",abs(snl6));
print time.time()-stp
print "m"
mapp=zeros([int(x/dx),int(l/dl)],dtype=float)
mapp[int((x/2)/dx)][int((l/2)/dl)]=1
mapp[int((x/2)/dx)][int((l/2+100)/dl)]=1
mapp[int((x/2+100)/dx)][int((l/2)/dl)]=1
imsave("mapp.bmp",mapp);
print time.time()-stp
