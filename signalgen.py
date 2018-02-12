import struct
from numpy import *
from math import *
bw=4e7
sp=5e7
spt=1.0/sp
st=1e-6
k=bw/st
prf=1e5
offset=st
rt=1.0/prf
tlt=0.01
sps=int(tlt*sp)
def gen(t):
	par=pi*k*pow(t,2)
	return complex(cos(par),sin(par))
def gen2(t):
	par=pi*-k*pow(t,2)
	return complex(cos(par),sin(par))
def streamgen(tt):
	ttt=tt%rt
	num=int(tt/rt)
	if(ttt<st):
		if(num%10==0):
			return gen2(ttt-st/2.0)
		else:
			return gen(ttt-st/2.0)
	else:
		return complex(0,0)

		
out="/media/gym/2T/out2.complex16s"
fp=open(out,'wb')
ft=0
while(ft<sps):
	ft+=1
	sg=streamgen(ft/sp-offset)
	sg=sg*pow(2,15)*0.9
	r=int(real(sg))
	i=int(imag(sg))
	fp.write(struct.pack('hh',r,i))
	if(ft%1000000==0):
		fp.flush()
fp.flush()
fp.close()
