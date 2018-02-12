from numpy import *
from math import *
from scipy.misc import imsave
import os
import struct
import scipy
import time
sp=5e7
spt=(1.0/sp)
prf=1e5
st=1e-6
rt=(1.0/prf)
psps=int(rt*sp)
fn="./00002.bin"
fp=open(fn,"rb")
lns=int(floor(os.path.getsize(fn)/(4*psps)))
signal=zeros([lns,psps],dtype=complex)
print lns,psps
for i in range(lns):
	for j in range(psps):
		[re,im]=struct.unpack("hh",fp.read(4))
		re=re/(pow(2,15)*0.9)
		im=im/(pow(2,15)*0.9)
		signal[i][j]=complex(re,im)
save("test.npy",signal);
imsave("testread.bmp",real(signal));


