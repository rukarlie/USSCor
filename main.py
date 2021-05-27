import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import krogh_interpolate

tbl=[]
with open('capture-10_55.csv','r') as f:
    for l in f:
        tbl.append(l)

xup=[]
xdn=[]
ups=[]
dns=[]

for i in range(1,len(tbl)):
    xup.append(float(tbl[i].split(',')[1]))
    ups.append(float(tbl[i].split(',')[2]))
    xdn.append(float(tbl[i].split(',')[4]))
    dns.append(float(tbl[i].split(',')[5]))

n_pulses = 10
fd=8000/1850
td_us=1/8

corr_ud=np.array(np.correlate(np.array(ups), np.array(dns),'full'))
corr_ua = np.array(np.correlate(np.array(ups), np.array(ups),'full'))
refs = [500*np.sin(i*2*np.pi/fd) for i in range(int(n_pulses*fd))]
corr_ur=np.array(np.correlate(np.array(ups), np.array(refs),'full'))
corr_dr=np.array(np.correlate(np.array(dns), np.array(refs),'full'))
fig, axs = plt.subplots(3, 2)

axs[0][0].plot(xup,ups,xdn,dns,range(int(n_pulses*fd)), refs)
axs[0][0].grid(True)
axs[1][0].plot(range(-len(xup)+1,len(xdn),1),corr_ud, range(-len(xup)+1,len(xdn),1),corr_ua)
axs[1][0].grid(True)
axs[2][0].plot(range(-len(refs)+1,len(xup),1),corr_ur,range(-len(refs)+1,len(xdn),1),corr_dr)
axs[2][0].grid(True)

diftof = np.argmax(corr_ud)-len(xup)+1
tofup =  np.argmax(corr_ur)-len(refs)+1
tofdn =  np.argmax(corr_dr)-len(refs)+1


diftof_us = diftof*td_us
tofup_us= tofup*td_us
tofdn_us = tofdn*td_us

maxpoints_ud = [corr_ud[np.argmax(corr_ud)-1], corr_ud[np.argmax(corr_ud)], corr_ud[np.argmax(corr_ud)+1]]
x_itr = np.linspace(-1, 1, num=1000)
interpolate = krogh_interpolate([-1, 0, 1], maxpoints_ud , x_itr)


axs[0][1].plot([-1, 0, 1], maxpoints_ud,x_itr, interpolate )
axs[0][1].grid(True)
print(x_itr[np.argmax(interpolate)])

diftof_us+= 2*td_us/1000 * x_itr[np.argmax(interpolate)]
#print(diftof_us)

maxpoints_ur = [corr_ur[np.argmax(corr_ur)-1], corr_ur[np.argmax(corr_ur)], corr_ur[np.argmax(corr_ur)+1]]
#x_itr = np.linspace(-1, 1, num=1000)
interpolate2 = krogh_interpolate([-1, 0, 1], maxpoints_ur , x_itr)
axs[1][1].plot([-1, 0, 1], maxpoints_ur,x_itr, interpolate2 )
axs[1][1].grid(True)
tofup_us+= 2*td_us/1000 * x_itr[np.argmax(interpolate2)]
print(tofup_us)

Ts=20e-6
f=[i/Ts for i in range(len(dns))]
axs[2][1].plot(f, list(map(lambda n,m: np.sqrt(n**2+m**2), np.fft.fft(dns).imag, np.fft.fft(dns).real)))
axs[2][1].grid(True)
axs[2][1].set_ylabel('FFT')


fig.tight_layout()
plt.show()