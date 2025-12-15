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

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[],xint = False):
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
    N = np.array((3,4,5,6,7,8))

    Er20 = np.array((1.5622667060554893E-002,1.0295866339090508E-002,8.1305066693647572E-003,4.1250978306675984E-003,3.8735127026275230E-003,1.6799977878459696E-003))
    Er40 = np.array((6.7613078076865750E-003,4.8691256855800695E-003,2.8054083301948876E-003,1.8624861381534256E-003,1.3483934274665433E-003,1.3150465417566775E-003))
    Er80 = np.array((1.8575455407547725E-003,2.0170633100616469E-003,1.9230770443349186E-003,9.8103718581560545E-004,5.8153019177473923E-004,5.1162757004411679E-004))

    Er3 = np.array((Er20[0],Er40[0],Er80[0]))
    Er5 = np.array((Er20[2],Er40[2],Er80[2]))
    Er7 = np.array((Er20[4],Er40[4],Er80[4]))
    Er8 = np.array((Er20[5],Er40[5],Er80[5]))

    lines = ['-','-','-']
    labels = ['$H=1/5$','$H=1/10$','$H=1/20$']
    marks = ['.','.','.']
    xdata = [N,N,N]
    ydata = [Er20,Er40,Er80]
    plotnow('relErr','$N$','$E_r(\\phi)$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)


    lines = ['-','-','-','-']
    labels = ['$N=3$','$N=5$','$N=7$']
    marks = ['.','.','.','.']
    H = np.array((20,40,80))
    xdata = [H,H,H]
    ydata = [Er3,Er5,Er7]
    plotnow('relErrH','$1/H$','$E_r(\\phi)$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog')
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
