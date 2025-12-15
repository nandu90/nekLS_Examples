from cycler import cycler
import math
import numpy as np
import os
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.ticker import MaxNLocator

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[],ylim=[],xlim=[],xint=False):
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
    

    if(xint):
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.grid()
    ax.legend(loc='best',fontsize=12)
    fig.savefig(fname+'.pdf',\
                bbox_inches='tight',dpi=100)
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)

    plt.close()
    return

def main():
    dt = 1.25e-4
    data = np.loadtxt('coarse/3/vol.dat')
    t4 = data[:,0] * dt
    thick4 = data[:,2]
    pos4 = data[:,4]

    data = np.loadtxt('coarse/4/vol.dat')
    t5 = data[:,0] * dt
    thick5 = data[:,2]
    pos5 = data[:,4]

    data = np.loadtxt('coarse/5/vol.dat')
    t6 = data[:,0] * dt
    thick6 = data[:,2]
    pos6 = data[:,4]

    labels=['$N=3$','$N=4$','$N=5$']
    lines = ['-','-','-','--','--','--']
    marks = ['','','','.','.','.']

    xdata = [t4,t5,t6]
    ydata = [thick4,thick5,thick6]
    plotnow('thickness25','$t$','$l_{avg}/l_0$',xdata,ydata,labels,linestyles=lines,markers=marks,xint=True,ylim=[])

    xdata = [t4,t5,t6]
    ydata = [pos4,pos5,pos6]
    plotnow('positivity25','$t$','$\psi_{L\\infty}$',xdata,ydata,labels,linestyles=lines,markers=marks,xint=True,ylim=[])

    data = np.loadtxt('fine/3/vol.dat')
    t4 = data[:,0] * dt
    thick4 = data[:,2]
    pos4 = data[:,4]

    data = np.loadtxt('fine/4/vol.dat')
    t5 = data[:,0] * dt
    thick5 = data[:,2]
    pos5 = data[:,4]

    data = np.loadtxt('fine/5/vol.dat')
    t6 = data[:,0] * dt
    thick6 = data[:,2]
    pos6 = data[:,4]

    labels=['$N=3$','$N=4$','$N=5$']
    lines = ['-','-','-','--','--','--']
    marks = ['','','','.','.','.']

    xdata = [t4,t5,t6]
    ydata = [thick4,thick5,thick6]
    plotnow('thickness50','$t$','$l_{avg}/l_0$',xdata,ydata,labels,linestyles=lines,markers=marks,xint=True,ylim=[])

    xdata = [t4,t5,t6]
    ydata = [pos4,pos5,pos6]
    plotnow('positivity50','$t$','$\\psi_{L\\infty}$',xdata,ydata,labels,linestyles=lines,markers=marks,xint=True,ylim=[])

    data = np.loadtxt('finest/3/vol.dat')
    t4 = data[:,0] * dt
    thick4 = data[:,2]
    pos4 = data[:,4]

    data = np.loadtxt('finest/4/vol.dat')
    t5 = data[:,0] * dt
    thick5 = data[:,2]
    pos5 = data[:,4]

    data = np.loadtxt('finest/5/vol.dat')
    t6 = data[:,0] * dt
    thick6 = data[:,2]
    pos6 = data[:,4]

    labels=['$N=3$','$N=4$','$N=5$']
    lines = ['-','-','-','--','--','--']
    marks = ['','','','.','.','.']

    xdata = [t4,t5,t6]
    ydata = [thick4,thick5,thick6]
    plotnow('thickness100','$t$','$l_{avg}/l_0$',xdata,ydata,labels,linestyles=lines,markers=marks,xint=True,ylim=[])

    xdata = [t4,t5,t6]
    ydata = [pos4,pos5,pos6]
    plotnow('positivity100','$t$','$\\psi_{L\\infty}$',xdata,ydata,labels,linestyles=lines,markers=marks,xint=True,ylim=[])
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
