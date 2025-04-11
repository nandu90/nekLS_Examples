from cycler import cycler
import math
import numpy as np
import os
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[]):
    default_cycler = (cycler(color=['#0072B2','#D55E00','#009E73','#CC0000','#990099'])*\
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
    
            
    ax.grid()
    ax.legend(loc='best',fontsize=12)
    fig.savefig(fname+'.pdf',\
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

def getdata(case,t=1):
    if(t==1):
        tname = 'zale.00001.dat'
    else:
        tname = 'zale.00002.dat'

    data = np.loadtxt(case+'/'+tname,skiprows=1)
    x = data[:,0]
    exact = data[:,5][(np.abs(x) > 0.3) & (np.abs(x) < 0.7)]
    svv = data[:,7][(np.abs(x) > 0.3) & (np.abs(x) < 0.7)]
    x = data[:,0][(np.abs(x) > 0.3) & (np.abs(x) < 0.7)]
    return x,exact,svv

def main():
    #Area error calculations:
    N = np.array((3,4,5))

    Er20 = np.array((3.8336451882897021E-005,1.3046976905905837E-005,6.4350543768281857E-006))
    Er40 = np.array((3.8251585267462453E-006,1.6753718760792068E-006,4.2768784513284135E-007))
    Er80 = np.array((2.7422907016687852E-007,1.3836894183082771E-007,7.3752096535824653E-008))

    lines = ['-','-','-']
    labels = ['20X20','40X40','80X80']
    marks = ['.','.','.']
    xdata = [N,N,N]
    
    ydata = [Er20,Er40,Er80]
    plotnow('relErr','$N$','$E_r(\\phi)$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
