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
    ax.legend(loc='best',fontsize=12,ncol=3)
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    fig.savefig(fname+'.pdf',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def getrmsdata(fname,t,rms):
    data = np.loadtxt(fname+'/rms.dat')
    t.append(data[:,0])
    rms.append(data[:,1])
    print("Mean velocity for "+fname+" = %.4e" % (np.mean(data[:,1])))
    return

def getcurvdata(fname,t,e1,e2):
    data = np.loadtxt(fname+'/rms.dat')
    t.append(data[:,0])
    e1.append(data[:,2])
    e2.append(data[:,3])
    return

def getCadata(fname,t,Ca):
    data = np.loadtxt(fname+'/rms.dat')
    t.append(data[:,0])
    Ca.append(data[:,4])
    print("Mean Ca for "+fname+" = %.4e" % (np.mean(data[:,4])))
    
    return

def main():

    t = []
    rms = []

    getrmsdata('H0.1/3',t,rms)
    getrmsdata('H0.1/5',t,rms)
    getrmsdata('H0.1/7',t,rms)
    getrmsdata('H0.1/9',t,rms)

    labels = ['$N=3$','$N=5$','$N=7$','$N=9$']
    lines = ['-','-','-','-','-']
    marks = ['','','','','']
        
    plotnow('H0.1','$t$','$v_{rms}$',t,rms,labels,linestyles=lines,markers=marks,ptype='semilogy')

    t = []
    rms = []

    getrmsdata('N7/20',t,rms)
    getrmsdata('H0.1/7',t,rms)
    getrmsdata('N7/80',t,rms)

    labels = ['$H=0.2$','$H=0.1$','$H=0.05$']
    lines = ['-','-','-','-','-']
    marks = ['','','','','']
        
    plotnow('N','$t$','$v_{rms}$',t,rms,labels,linestyles=lines,markers=marks,ptype='semilogy')

    t = []
    e1 = []
    e2 = []

    getcurvdata('H0.1/3',t,e1,e2)
    getcurvdata('H0.1/5',t,e1,e2)
    getcurvdata('H0.1/7',t,e1,e2)
    getcurvdata('H0.1/9',t,e1,e2)
    
    labels = ['$N=3$','$N=5$','$N=7$','$N=9$']
    lines = ['-','-','-','-','-']
    marks = ['','','','','']
        
    plotnow('curv1','$t$','$e_{L2}$',t,e1,labels,linestyles=lines,markers=marks,ptype='semilogy')
    plotnow('curv2','$t$','$e_{L2}$',t,e2,labels,linestyles=lines,markers=marks,ptype='semilogy')


    t = []
    rms = []

    getrmsdata('xi0.25/3',t,rms)
    getrmsdata('xi0.25/5',t,rms)
    getrmsdata('xi0.25/7',t,rms)
    getrmsdata('xi0.25/9',t,rms)

    labels = ['$N=3$','$N=5$','$N=7$','$N=9$']
    lines = ['-','-','-','-','-']
    marks = ['','','','','']
        
    plotnow('xi','$t$','$v_{rms}$',t,rms,labels,linestyles=lines,markers=marks,ptype='semilogy')

    t = []
    Ca = []
    getCadata('H0.1/3',t,Ca)
    getCadata('H0.1/5',t,Ca)
    getCadata('H0.1/7',t,Ca)
    getCadata('H0.1/9',t,Ca)
    
    labels = ['$N=3$','$N=5$','$N=7$','$N=9$']
    lines = ['-','-','-','-','-']
    marks = ['','','','','']
    plotnow('Ca','$t$','$Ca$',t,Ca,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    t = []
    Ca = []

    getCadata('N7/20',t,Ca)
    getCadata('H0.1/7',t,Ca)
    getCadata('N7/80',t,Ca)

    labels = ['$H=0.2$','$H=0.1$','$H=0.05$']
    lines = ['-','-','-','-','-']
    marks = ['','','','','']
        
    plotnow('Ca_N','$t$','$Ca$',t,Ca,labels,linestyles=lines,markers=marks,ptype='semilogy')

    t = []
    rms = []

    getrmsdata('La/10',t,rms)
    getrmsdata('La/1e2',t,rms)
    getrmsdata('La/1e3',t,rms)
    getrmsdata('La/1e4',t,rms)
    getrmsdata('La/1e5',t,rms)
    
    labels = ['$La=10$','$La=10^2$','$La=10^3$','$La=10^4$','$La=10^5$']
    lines = ['-','-','-','-','-','-']
    marks = ['','','','','','']
        
    plotnow('La','$t$','$v_{rms}$',t,rms,labels,linestyles=lines,markers=marks,ptype='semilogy')
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
