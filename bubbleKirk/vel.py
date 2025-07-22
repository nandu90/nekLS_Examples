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
    default_cycler = (cycler(color=['#0072B2','#D55E00','#D55E00','#D55E00','#990099'])*\
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
    for i,f in enumerate(files):
        data = np.loadtxt(f)

        if(i > 0):
            t_start = data[0,0]

            prev = alldata[-1]
            alldata[-1] = prev[prev[:,0] < t_start]
            
        alldata.append(data)

    alldata = np.vstack(alldata)

    t = alldata[:,0]
    Ev = np.abs(alldata[:,1])
    vel = alldata[:,2]
    
    return t,Ev,vel

def main():
    L = 0.005 #(Bubble Dia in m)
    g = 9.81  #(m/s^2)
    U = math.sqrt(g*L)
    
    files = ['stats1.dat','stats2.dat','stats3.dat','stats4.dat','stats5.dat','stats6.dat','stats7.dat','stats8.dat','stats9.dat','stats10.dat','stats11.dat','stats12.dat','stats13.dat']
    
    t1,Ev1,vel1 = getVeldata(files)
    t1 = t1 
    vel1 = vel1 * U *1000

    texp = t1
    velexp = np.ones(t1.shape) * 228.69 #mm/s
    velexp1 = velexp + 42.10 #mm/s
    velexp2 = velexp - 42.10 #mm/s
    
    
    t = [t1, texp, texp, texp]
    vel = [vel1, velexp, velexp1, velexp2]
    
    labels = ['Nek5k','TAMU exp ($228.69 \\pm 42.10$)','','']
    lines = ['--','-.',':',':']
    marks = ['','','','']

    plotnow('vel','$t (s)$','$v_y (mm/s)$',t,vel,labels,linestyles=lines,markers=marks)

    t = [t1 * U/L] #non-dimensional
    Ev = [np.abs(Ev1)]
    labels=['']

    plotnow('Ev','$t*$','$\|E_v\|$',t,Ev,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
