from numpy import *
from math import *
from scipy.misc import imsave
import scipy
import time
import cmath
from struct import *
from scipy.signal import *
v=0.095
h=0.15
lmin=0.0001
l=1.5
dx=0.02*v
x=1000*dx
dl=0.002
st=512/5e5
c=340
bw=3e5
k=-bw/st
sp=5e5
freq=4e4
pwr=100
tm=1e-2
slen=4000
dt=1/sp
tshift=st/2
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
snls=zeros(int(sp*st),dtype=complex)

for i in  range(len(snls)):
	snls[i]=signalr(i/sp,0)
snlr=zeros([int(x/dx),int(slen)],dtype=complex)
snl2=zeros([int(x/dx),int(slen)],dtype=complex)
#snl3=zeros([int(x/dx),int(slen)],dtype=complex)
def PointTarget(rxx,t,px,py):
	rr=sqrt(pow(h,2)+pow(px,2)+pow(rxx-py,2))
	tos=2*rr/c
	return signalr(t-tos,-2*pi*tos*freq)/pow(rr,4)
		
snlss=zeros(int(slen),dtype=float)
snlssi=zeros(int(slen),dtype=float)
for i in  range(len(snlr)):
	for j in  range(slen):
		#print i,j
		snlss[j]=float(unpack("H",fi.read(2))[0])
		#print snlss[j]
	avg=sum(snlss)/len(snlss)
	#print avg
	for j in  range(slen):
		snlss[j]-=avg
	snlssi=hilbert(snlss)
	for j in  range(slen):
		#snlssi
		tt=j/sp
		snlr[i][j]=dc(tt,complex(snlss[j],snlssi[j]))
		#print snlr[i][j]
		#print j
imsave("test.bmp",real(snlr));
imsave("testa.bmp",abs(snlr));
print time.time()-stp
print "2"
for i in range(len(snlr)):
	snl2[i]=convolve(snlr[i],flipud(conjugate(snls)),'same')
imsave("test2.bmp",real(snl2));
print time.time()-stp
print "3"
snl3=fft.fftshift(fft.fft(snl2,axis=0),axes=0)
imsave("test3.bmp",real(snl3));
print time.time()-stp
print "4"
def rcmc(ll,fr):
	a=-(2*c*fr*sqrt(((2*freq+c*fr)*(2*freq-c*fr)*(pow(h,2)+pow(ll,2)))/4))/(-pow(c,2)*pow(fr,2)+4*pow(freq,2))
	rrr=sqrt(pow(ll,2)+pow(h,2)+pow(a,2))
	return rrr
def r2ti(r):
	return 2*r/(c*dt)
snl4=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(snl4)):
	for j in range(len(snl4[i])):
		try:
			if(tm*sp>int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))+tshift*sp) and int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))+tshift*sp)>=0):
				snl4[i][j]=snl3[i][int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))+tshift*sp)]
		except:
			print "matherr"
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

fi.close()
