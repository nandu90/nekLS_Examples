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

def main():
    #it looks like gravity is omitted, so Fr is infinite

    #non-dimensionalize w.r.t liquid properties
    Ul = 1.0  #Non-dimensional velocity scale (injector inlet velocity)
    Dl = 1.0  #non-dimensional length scale (injector dia)
    Rel = 5000 #given

    nul = 1/Rel
    rhol = 1.0   #ref density
    mul = rhol * nul

    rhoratio = 0.1           #rhog/rhol
    rhog = rhoratio * rhol

    nuratio = 1/0.7          #nug/nul
    muratio = nuratio * rhoratio   #mug/mul
    mug = muratio * mul

    Wel = 500 #given

    q = 1./5.                #g/l
    Ug = math.sqrt(q * Ul**2.0 / rhoratio) #non-dimensional gas velocity at inlet

    print("Inlet injector velocity", Ul)
    print("Inlet cross-flow velocity",Ug)
    print("Reynolds number", Rel)
    print("Weber number",Wel)
    print("rhog/rhol",rhoratio)
    print("mug/mul",muratio)

    #Jet inlet
    r = np.linspace(0,0.5,1000)
    Umax = Ul/0.817
    u = Umax * (1 - 2*r/Dl)**(1./7.0)
    xdata = [r]
    ydata = [u]
    labels = ['Jet Inlet']
    lines = ['-']
    marks = ['']

    plotnow('Uinj','$r$','$U$',xdata,ydata,labels,linestyles=lines,markers=marks)

    #cross flow
    y = np.linspace(0,10,1000)
    Uinf = 1.414
    y0 = 0.5
    a = 0.3
    uin = Uinf * 0.5 * (1 + np.tanh((y-y0)/a))

    xdata = [y]
    ydata = [uin]
    labels = ['Cross-flow']
    plotnow('Ucf','$U$','$y$',ydata,xdata,labels,linestyles=lines,markers=marks)


    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
