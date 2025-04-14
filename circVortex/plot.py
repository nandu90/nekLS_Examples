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

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[],ylim=[]):
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
    

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

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

def getdata(dname,dt):
    
    tname = dname+'/vol.dat'

    data = np.loadtxt(tname)
    t = data[:,0]*dt
    Ev = np.abs(data[:,2])
    return t,Ev

def main():
    # N = 'N7'
    # xdata = []
    # ydata = []

    # x,exact,svv = getdata()
    # xdata.append(x)
    # ydata.append(exact)
    # xdata.append(x)
    # ydata.append(svv)
    
    # labels=['Initial','Final']
    # lines = [':','-.','--','--','-']
    # marks = ['','','','','']
    # plotnow('N'+N,'$x$','$\\psi$',xdata,ydata,labels,linestyles=lines,markers=marks)

    N = np.array((4,5,6))
    Er_128 = np.array((9.0121430053904573E-009,4.7573261079374876E-009,2.9125131521457678E-009))
    Es_128 = np.array((4.8170952421264479E-004,2.4951990365227537E-004,1.4472237085229599E-004))
    Ev_128 = np.array((1.8639063125270838E-008,4.9469422876139218E-009,5.7849675525883943E-009))

    Er_64 = np.array((8.5201681940413822E-008,4.3788294347666601E-008,2.6348497535847811E-008))
    Es_64 = np.array((2.9877655209546300E-003,1.6103351667657384E-003,1.0848257634261406E-003))
    Ev_64 = np.array((6.1842269765526696E-007,5.4557613089345600E-009,7.2716413122847481E-008))

    Er_32 = np.array((1.0030471134678740E-006,4.9284616208161504E-007,2.9803326075091964E-007))
    Es_32 = np.array((1.2155240362058421E-002,8.9270407813271807E-003,6.6675553538042146E-003))
    Ev_32 = np.array((1.4096861216194850E-005,2.2878931738791608E-006,1.2639558339703356E-006))

    labels=['$H=1/32$','$H=1/64$','$H=1/128$']
    lines = [':','-.','--','--','-']
    marks = ['.','.','.','','']
    xdata = [N,N,N]
    
    ydata = [Er_32,Er_64,Er_128]
    plotnow('Er','$N$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')

    ydata = [Es_32,Es_64,Es_128]
    plotnow('Es','$N$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    ydata = [Ev_32,Ev_64,Ev_128]
    plotnow('Ev','$N$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')

    #plot Ev v/s time error
    t32, E32 = getdata('32/6',8e-4)
    t64, E64 = getdata('64/6',4e-4)
    t128, E128 = getdata('128/6',2e-4)

    xdata = [t32,t64,t128]
    ydata = [E32,E64,E128]
    marks = ['','','','','']
    
    plotnow('Ev_6','$t$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',ylim=[1e-14,1e-4])

    t32, E32 = getdata('32/5',8e-4)
    t64, E64 = getdata('64/5',4e-4)
    t128, E128 = getdata('128/5',2e-4)

    xdata = [t32,t64,t128]
    ydata = [E32,E64,E128]
    marks = ['','','','','']
    
    plotnow('Ev_5','$t$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',ylim=[1e-14,1e-4])

    t32, E32 = getdata('32/4',8e-4)
    t64, E64 = getdata('64/4',4e-4)
    t128, E128 = getdata('128/4',2e-4)

    xdata = [t32,t64,t128]
    ydata = [E32,E64,E128]
    marks = ['','','','','']
    
    plotnow('Ev_4','$t$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',ylim=[1e-14,1e-4])
    
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
