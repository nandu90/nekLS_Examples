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
    default_cycler = (cycler(color=['#0072B2','#D55E00','#009E73','#CC0000'])*\
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
    #ax.legend(loc='best',fontsize=12)
    # fig.savefig(fname+'.pdf',\
    #             bbox_inches='tight',dpi=100)
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def main():

    xdata = []
    ydata = []
    t = []

    for x in range(4):
        fname = 'species.0000'+str(x+1)+'.dat'

        with open(fname,"r") as f:
            first_line = f.readline().strip()
            last_entry = first_line.split()[-1]
            t.append(float(last_entry)*5.0)

        data = np.loadtxt(fname,skiprows=1)
        xdata.append(data[:,1])
        ydata.append(data[:,-1])

    data = np.loadtxt('t0.csv',delimiter=',')
    xdata.append(data[:,0])
    ydata.append(data[:,1])
        
    data = np.loadtxt('t05.csv',delimiter=',')
    xdata.append(data[:,0])
    ydata.append(data[:,1])

    data = np.loadtxt('t2.csv',delimiter=',')
    xdata.append(data[:,0])
    ydata.append(data[:,1])

    data = np.loadtxt('t8.csv',delimiter=',')
    xdata.append(data[:,0])
    ydata.append(data[:,1])

    labels = [f"t={x:.3f}s" for x in t]
    labels.append('OF')
    labels.append('OF')
    labels.append('OF')
    labels.append('OF')

    lines = ['-','-','-','-','','','','']
    marks = ['','','','','o','s','^','D']

    plotnow('c','$y (cm)$','$c$',xdata,ydata,labels,linestyles=lines,markers=marks)

    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
