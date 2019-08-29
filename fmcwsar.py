from math import *
from numpy import *
from scipy.misc import imsave
import scipy
import time
import cmath
from struct import *
from scipy.signal import *
import sys
indata=load(sys.argv[1])
v=5
h=100
lmin=1
l=350
dx=0.001*v
dl=0.2
c=3e8
freq=5.8e9
slen=indata.shape[1]
x=len(indata)*dx
fi=open("test.bin","rb")
def signalr(t,pha):
	tt=pi*k*pow(t-st/2,2)
	#print t
	return complex(cos(tt+pha),sin(tt+pha))*(0<=t and t<st)
def dc(tt,a):
	return a*cmath.exp(-2*pi*1j*freq*tt)

print slen
print "1"
stp=time.time()
snlr=zeros([int(x/dx),int(slen)],dtype=complex)
snl2=zeros([int(x/dx),int(slen)],dtype=complex)
#snl3=zeros([int(x/dx),int(slen)],dtype=complex)
def PointTarget(rxx,t,px,py):
	rr=sqrt(pow(h,2)+pow(px,2)+pow(rxx-py,2))
	tos=2*rr/c
	return signalr(t-tos,-2*pi*tos*freq)/pow(rr,4)

print time.time()-stp
print "3"
snl3=fft.fftshift(fft.fft(indata,axis=0),axes=0)
for i in range(len(snl3)/2-100,len(snl3)/2+100):
	snl3[i]=zeros(snl3.shape[1],complex)
imsave(sys.argv[1]+"test3.bmp",abs(snl3));
print time.time()-stp
print "4"
def rcmc(ll,fr):
	a=-(2*c*fr*sqrt(((2*freq+c*fr)*(2*freq-c*fr)*(pow(h,2)+pow(ll,2)))/4))/(-pow(c,2)*pow(fr,2)+4*pow(freq,2))
	rrr=sqrt(pow(ll,2)+pow(h,2)+pow(a,2))
	return rrr
def r2ti(r):
	return r/0.25
snl4=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(snl4)):
	for j in range(len(snl4[i])):
		try:
			if(snl3.shape[1]>int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))) and int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx)))>=0):
				snl4[i][j]=snl3[i][int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx)))]
				#print "ok"
		except:
			aaaaaaaa=0
			#print "matherr"
imsave(sys.argv[1]+"test4.bmp",abs(snl4));
print time.time()-stp
print "5"
snl5=fft.ifft(fft.ifftshift(snl4,axes=0),axis=0)
imsave(sys.argv[1]+"test5.bmp",real(snl5));
print time.time()-stp
print "6"
filt=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(filt)):
	for j in range(len(filt[i])):
		rrr=sqrt(pow(j*dl+lmin,2)+pow(h,2)+pow((i*dx)-x/2,2))
		tos=2*rrr/c
		par=tos*2*pi*freq
		filt[i][j]=complex(cos(par),sin(par))
imsave(sys.argv[1]+"filt.bmp",real(filt));
snl6=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(snl6[0])):
	snl6[:,i]=convolve(snl5[:,i],flipud(conjugate(filt[:,i])),'same')
imsave(sys.argv[1]+"test6.bmp",abs(snl6));
print time.time()-stp

fi.close()
snl7=zeros([int(snl6.shape[0]/40),snl6.shape[1]],dtype=float)
for i in range(snl6.shape[0]):
	snl7[int(i/40)]+=abs(snl6[i])

imsave(sys.argv[1]+"test7.bmp",sqrt(snl7));