from struct import *
from math import *
import cmath
import scipy
from numpy import *
from scipy.signal import *
import sys


linen=10000
outn=1500
lines=int(sys.argv[2])

fi=open(sys.argv[1]+".bin","rb")
fi.read(2*int(sys.argv[3]))

f2=open(sys.argv[1]+"mag.ppm","w")
f2.write("P5\n"+str(int(outn))+" "+str(int(lines/10))+"\n"+"255\n")

f3=open(sys.argv[1]+"real.ppm","w")
f3.write("P5\n"+str(int(outn))+" "+str(int(lines))+"\n"+"255\n")

line=zeros(int(linen),dtype=float)
linec=zeros(int(linen),dtype=complex)
linef=zeros(int(linen),dtype=complex)
lineout=zeros(int(outn),dtype=complex)
lineoutr=zeros(int(outn),dtype=float)
lppm=zeros(int(outn),dtype=float)
for i in  range(lines):
	print "ln",i,"/",lines
	aa=0x8000
	bb=0x8000
	cc=0x8000
	while((aa!=0x0000 or bb!=0x8000)):
		bb=aa
		aa=int(unpack("H",fi.read(2))[0]&0x8000)
	for j in  range(linen):
		#print i,j
		aaa=int(unpack("H",fi.read(2))[0])
		if(aaa&0x8000==0x8000):
			break
			#print "break"
			#snlss[j]=0
		else:
			line[j]=int(aaa&0x3fff)
			if(int(aaa&0x3fff)<0):
				print "aaa",aaa,aaa&0x3fff
			#print 1
		#print snlss[j]

	avg=sum(line)/len(line)
	print avg,min(line),max(line)
	for j in  range(linen):
		if(line[j]<0):
			#print "fuck",snlss[j]
			line[j]=avg
		line[j]-=avg
		if(j<4000):
			line[j]=0;
	for j in range(linen):
		linec[j]=complex(line[j],0)
	linef=fft.fftshift(fft.fft(line))
	lineout=linef[int(linen/2):int(linen/2)+int(outn)]
	lppm+=abs(lineout)
	lineoutr=real(lineout)
	#print lineout
	lineoutr=lineoutr-(sum(lineoutr)/outn)
	lineoutr=lineoutr/(0.1+max(max(lineoutr),-min(lineoutr)))
	lineoutr=lineoutr*127+128
	print "l",max(lineoutr),min(lineoutr)
	for j in range(outn):
		f3.write(pack("B",int(lineoutr[j])))
	if(i%10==9):
		lppm=255*abs(lppm)/max(abs(lppm))
		#lppm=255*sqrt(abs(lppm))/max(sqrt(abs(lppm)))
		for j in range(int(outn)):
			f2.write(pack("B",int(lppm[j])))
		lppm=zeros(int(outn),dtype=float)
	#for j in range(1,slen-1):
		#if(snlss[j]-snlss[j-1]>1000 and snlss[j]-snlss[j+1]>1000):
			#print "fuck!",snlss[j-1],snlss[j],snlss[j+1]
			#snlss[j]=(snlss[j+1]+snlss[j-1])/2.0
			#print "fucked",snlss[j-1],snlss[j],snlss[j+1]
			#print "fuck!",snlss[j-1],snlss[j],snlss[j+1]'''
	#snlssi=hilbert(snlss)
fi.close()
f2.close()
