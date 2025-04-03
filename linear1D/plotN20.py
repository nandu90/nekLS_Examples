from cycler import cycler
import math
import numpy as np
import os
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[],xlim=[],ylim=[]):
    default_cycler = (cycler(color=['k','b','r','g','m'])*\
                      cycler(linestyle=['-'])*cycler(marker=['']))
    plt.rc('lines',linewidth=1)
    plt.rc('axes',prop_cycle=default_cycler)
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)  

    ax.set_xlabel(xlabel,fontsize=15)
    ax.set_ylabel(ylabel,fontsize=15)
    ax.tick_params(axis='both',labelsize=12)

    # if(len(linestyles) == 0):
    #     linestyles = ['-']*len(x)
    #     markers = ['']*len(x)

    if(xlim != []):
        ax.set_xlim([xlim[0],xlim[1]])
        
    if(ylim != []):
        ax.set_ylim([ylim[0],ylim[1]])

    print(linestyles)
    print(len(x))

    for i in range(len(y)):
        if(ptype=='line'):
            ax.plot(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i],linewidth=1.5)
        elif(ptype=='semilogx'):
            ax.semilogx(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
        elif(ptype=='semilogy'):
            ax.semilogy(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
        else:
            ax.loglog(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
    
            
    ax.grid()
    ax.legend(loc='best',fontsize=8)
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def getexact(x,exact):
    for i in range(x.shape[0]):
        exact[i] = 0.0
        if(x[i] >= 0.35 and x[i] <= 0.55):
            exact[i] = 1.0
        elif(x[i] > 0.7 and x[i] < 0.9):
            exact[i] = math.sqrt(1.0 - ((x[i]-0.8)/0.1)**2.0)
        elif(x[i] > 0.08 and x[i] <= 0.15):
            exact[i] = (1./0.0049)*x[i]**2. - (0.16/0.0049)*x[i] + 0.0064/0.0049
        elif(x[i] > 0.15 and x[i] <= 0.22):
            exact[i] = (1./0.0049)*x[i]**2. - (0.44/0.0049)*x[i] + 0.0484/0.0049
    
    return

def main():
    
    data = np.loadtxt('t1_N20.dat',skiprows=1)
    x = data[:,0]
    exact = data[:,5]
    avm = data[:,6]
    svv001 = data[:,7]
    svv01 = data[:,8]
    svv1 = data[:,9]

    data = np.loadtxt('N2/t1_N20.dat',skiprows=1)
    x = data[:,0]
    svv001N = data[:,7]
    svv01N = data[:,8]
    svv1N = data[:,9]
    
    getexact(x,exact)

    xdata = [x,x,x,x,x]
    ydata = [exact,svv01,svv01N,avm]
    
    labels=['Exact','SVV-$N/4$','SVV-$N/2$','AVM']
    lines = [':','--','--','-.','-']
    marks = ['','','','','']
    plotnow('t1_N20','$x$','$u$',xdata,ydata,labels,linestyles=lines,markers=marks)
    plotnow('t1_N20_zoom','$x$','$u$',xdata,ydata,labels,linestyles=lines,markers=marks,xlim=[0.1,0.5],ylim=[0.8,1.1])

    #t100
    data = np.loadtxt('t100_N20.dat',skiprows=1)
    x = data[:,0]
    avm = data[:,6]
    svv001 = data[:,7]
    svv01 = data[:,8]
    svv1 = data[:,9]

    data = np.loadtxt('N2/t100_N20.dat',skiprows=1)
    x = data[:,0]
    svv001N = data[:,7]
    svv01N = data[:,8]
    svv1N = data[:,9]
    
    getexact(x,exact)

    xdata = [x,x,x,x,x]
    ydata = [exact,svv01,svv01N,avm]
    plotnow('t100_N20','$x$','$u$',xdata,ydata,labels,linestyles=lines,markers=marks)
    plotnow('t100_N20_zoom','$x$','$u$',xdata,ydata,labels,linestyles=lines,markers=marks,xlim=[0.1,0.5],ylim=[0.8,1.1])
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
