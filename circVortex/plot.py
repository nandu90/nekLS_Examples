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

def getLineData(fname):
    data = np.loadtxt(fname+'/cv.00001.dat',skiprows=1)
    x = data[:,0]
    y = data[:,5]
    phi = data[:,6]
    
    return x,y,phi

def main():
    N = np.array((4,5,6))
    Er_128 = np.array((8.7769329283669381E-009,4.7423302294376554E-009,2.9479452796370447E-009))
    Es_128 = np.array((3.5249995053713375E-004,2.4097717249581824E-004,1.4962677002915682E-004))
    Ev_128 = np.array((4.2868897061620243E-009,2.5060440029688482E-009,4.7702495642924611E-010))

    Er_64 = np.array((8.5876557641958333E-008,4.4462492512397774E-008,2.8885071966793394E-008))
    Es_64 = np.array((3.0213114116032862E-003,1.6153760004603223E-003,1.3645774844588490E-003))
    Ev_64 = np.array((2.5884522223026723E-007,3.9422789419883107E-007,6.8912272345514569E-008))

    Er_32 = np.array((1.0530922893464049E-006,5.0744552814151018E-007,3.8717101656700176E-007))
    Es_32 = np.array((1.4106612138485590E-002,7.6611509723752318E-003,7.9830726548595302E-003))
    Ev_32 = np.array((1.4347943853203036E-005,4.8379391817553345E-006,1.1175368061744553E-006))

    labels=['$H=1/32$','$H=1/64$','$H=1/128$']
    lines = [':','-.','--','--','-']
    marks = ['.','.','.','','']
    xdata = [N,N,N]
    
    ydata = [Er_32,Er_64,Er_128]
    plotnow('Er','$N$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)

    ydata = [Es_32,Es_64,Es_128]
    plotnow('Es','$N$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)
    
    ydata = [Ev_32,Ev_64,Ev_128]
    plotnow('Ev','$N$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)

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
    
    #Line plot across y=0.75
    x4,psi4,phi4 = getLineData('128/4') 
    x5,psi5,phi5 = getLineData('128/5') 
    x6,psi6,phi6 = getLineData('128/6') 

    data = np.loadtxt('128/6/cv.00001.dat',skiprows=1)
    xini = data[:,0]
    yini = data[:,4]

    xdata = [x4,x5,x6,xini]
    ydata = [psi4,psi5,psi6,yini]
    marks = ['','','','']
    labels=['$N=4$','$N=5$','$N=6$','Initial']
    lines = ['-.','-.','-.',':','-']
    plotnow('psi','$x$','$\\psi$',xdata,ydata,labels,linestyles=lines,markers=marks,xlim=[0.25,0.75])

    xdata = [x4,x5,x6,xini]
    exact = np.sqrt((xini-0.5)**2) - 0.15
    ydata = [phi4,phi5,phi6,exact]
    marks = ['','','','']
    
    labels=['$N=4$','$N=5$','$N=6$','Exact']
    lines = ['-.','-.','-.',':','-']
    plotnow('phi','$x$','$\\phi$',xdata,ydata,labels,linestyles=lines,markers=marks,ylim=[-0.1,0.1],xlim=[0.25,0.75])
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
