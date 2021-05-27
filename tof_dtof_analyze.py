import matplotlib.pyplot as plt
import numpy as np

# \brief This function parses waveform file and collect data in dictionary
# \param    path            string, path to waveform file
# \return   data_dict       dictionary, collected data from file    
def wvfr_parse(path):

    tbl=[]
    with open(path,'r') as f:
        for l in f:
            tbl.append(l)

    data_dict = {}

    for l in tbl:
        if l.split(',')[1] in data_dict:
            data_dict[l.split(',')[1]].append(float(l.split(',')[2]))
        else:
            try:
                data_dict[l.split(',')[1]]=[float(l.split(',')[2])]
                #break
            except:
                #print(l.split(',')[1])
                continue

    return data_dict            
            
def normalize_fxn(seq):
    #Нормировка по размаху и смещает среднее значение в ноль
    return list(map(lambda n: (n-np.median(seq))/(np.max(seq)-np.min(seq)),seq))

def usr_cor_fxn(s2,s1):
    ln1=len(s1)
    ln2=len(s2)
    zro_m1 = [0]*ln2
    zro_m2 = [0]*ln1
    f_s1 = s1.copy()
    #f_s2 = s2.copy()
    f_s2 = zro_m2.copy()
    f_s2.extend(s2.copy())
    f_s2.extend(zro_m2.copy())
    p=0
    sp=0
    corr=[]
    for j in range(1,ln1+ln2):
        p=0
        sp=0
        for i in range(ln1):
            p=f_s1[i]*f_s2[i+j]
            sp+=p
        corr.append(sp)
    
    return corr



           

data_dict = wvfr_parse('waveforms2.csv')
keys = list(data_dict.keys())

'''
#Plot all waveforms
fig, axs = plt.subplots(len(keys))
n_p=0
for k in keys:
    axs[n_p].plot(data_dict[k])
    axs[n_p].grid(True)
    axs[n_p].set_ylabel(k)
    n_p+=1

fig.tight_layout()
plt.show()
'''
d_tof=[]
volume=[]

for i in range(len(data_dict[keys[2]])):
    d_tof.append(data_dict[keys[2]][i]-data_dict[keys[1]][i])



fig, axs = plt.subplots(3)

#axs.plot(x, d_tof,x , data_dict[keys[0]])
#axs.plot(np.array(np.correlate(np.array(data_dict[keys[2]]), np.array(data_dict[keys[1]]),'full')))
#axs.plot(x,np.array(data_dict[keys[2]]),x,np.array(data_dict[keys[1]]), range(-len(d_tof)+1,len(d_tof)),np.array(np.correlate(np.array(data_dict[keys[2]]), np.array(data_dict[keys[1]]),'full')))

td = 1e-2  #10ms 
Ts = td*len(d_tof)
fd = 1/td
x=[i*td for i in range(len(d_tof))]
tau = [i*td for i in range(-len(d_tof)+1,len(d_tof))]
f = [i/Ts for i in range(len(d_tof))]


DNS_norm=normalize_fxn(data_dict[keys[2]])
UPS_norm=normalize_fxn(data_dict[keys[1]])
corr_norm = np.correlate(np.array(DNS_norm), np.array(UPS_norm), 'full')
corr_usr = usr_cor_fxn(DNS_norm, UPS_norm)
axs[0].plot(x, DNS_norm, x, UPS_norm)
axs[1].plot(tau,corr_norm,tau,corr_usr)
axs[2].plot(f,np.fft.fft(DNS_norm).real)
axs[0].grid(True)
axs[1].grid(True)
axs[2].grid(True)
axs[0].set_ylabel('TOFs')
axs[1].set_ylabel('Corr')
axs[2].set_ylabel('FFT')
fig.tight_layout()
plt.show()




