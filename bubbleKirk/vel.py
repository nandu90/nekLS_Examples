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
    plt.close()
    return

def getVeldata(files):
    alldata = []
    for f in files:
        data = np.loadtxt(f)
        alldata.append(data)

    alldata = np.vstack(alldata)

    _, unique_indices = np.unique(alldata[:, 0], return_index=True)
    unique_data = alldata[np.sort(unique_indices)]

    t = unique_data[:,0]
    Ev = np.abs(unique_data[:,1])
    vel = unique_data[:,2]
    
    return t,Ev,vel

def main():
    L = 0.005 #(Bubble Dia in m)
    g = 9.81  #(m/s^2)
    U = math.sqrt(g*L)
    
    files = ['stats.dat','stats2.dat','stats3.dat']
    
    t1,Ev1,vel1 = getVeldata(files)

    t = [t1 * L/U]
    vel = [vel1 * U * 1000]
    
    labels = ['']
    lines = ['--','-.','--','--']
    marks = ['','','','']

    #plotnow('vel','$t$','$v_y$',t,vel,labels,linestyles=lines,markers=marks)
    plotnow('vel','$t (s)$','$v_y (mm/s)$',t,vel,labels,linestyles=lines,markers=marks)
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
