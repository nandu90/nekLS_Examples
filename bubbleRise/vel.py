from cycler import cycler
import math
import numpy as np
import os
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.linalg import lstsq
from scipy.optimize import curve_fit
from scipy import stats
from scipy import optimize
import scipy.interpolate as interpolate

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[],ylim=[],xlim=[]):
    default_cycler = (cycler(color=['#0072B2','#D55E00','#009E73','#CC0000','#990099'])*\
                      cycler(linestyle=['-'])*cycler(marker=['']))
    plt.rc('lines',linewidth=1)
    plt.rc('axes',prop_cycle=default_cycler)
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)  

    ax.set_xlabel(xlabel,fontsize=15)
    ax.set_ylabel(ylabel,fontsize=15)
    ax.tick_params(axis='both',labelsize=12)

    if(ylim != []):
        ax.set_ylim(ylim[0],ylim[1])

    if(xlim != []):
        ax.set_xlim(xlim[0],xlim[1])

    # if(len(linestyles) == 0):
    #     linestyles = ['-']*len(x)
    #     markers = ['']*len(x)

    print(linestyles)
    print(len(x))

    for i in range(len(y)):
        if(ptype=='line'):
            ax.plot(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i],linewidth=2.0)
        elif(ptype=='semilogx'):
            ax.semilogx(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i],linewidth=2.0)
        elif(ptype=='semilogy'):
            ax.semilogy(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i],linewidth=2.0)
        else:
            ax.loglog(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i],linewidth=2.0)
    

    #ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.grid()
    ax.legend(loc='best',fontsize=12)

    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    fig.savefig(fname+'.pdf',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def getdata(files):
    trimmed_data = []
    for i,f in enumerate(files):
        data = np.loadtxt(f)
        
        if(i > 0):
            t_start = data[0,0]

            prev = trimmed_data[-1]
            trimmed_data[-1] = prev[prev[:,0] < t_start]

        trimmed_data.append(data)

    alldata = np.vstack(trimmed_data)

    t = alldata[:,0]
    v = alldata[:,1]
    
    return t,v

def main():    
    #Eo29
    files = ['vel1.dat','vel2.dat','vel3.dat','vel4.dat','vel5.dat']
    t1,vel1 = getdata('Eo29/'+ item for item in files)
    files = ['vol1.dat','vol2.dat','vol3.dat','vol4.dat','vol5.dat']
    t11,vol1 = getdata('Eo29/'+ item for item in files)
    
    #Eo200
    # files = ['vel1.dat','vel2.dat']
    # t2,vel2 = getdata('Eo200/'+ item for item in files)
    # files = ['vol1.dat','vol2.dat']
    # t21,vol2 = getdata('Eo200/'+ item for item in files)

    #Dodd
    # files = ['Dodd/vol.dat']
    # t3, vol3 = getdata(files)
    # vol3 = np.abs(vol3)

    labels = ['Ga=2.316; Eo=29','Ga=70.7;   Eo=200','Dodd']
    lines = ['--','--','-.','--']
    marks = ['','','','']

    t = [t1]
    vel = [vel1]

    plotnow('vel','$t$','$w$',t,vel,labels,linestyles=lines,markers=marks)

    t = [t11]#,t3]
    vol = [vol1]#,vol3]

    plotnow('vol','$t$','$|E_v|$',t,vol,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
