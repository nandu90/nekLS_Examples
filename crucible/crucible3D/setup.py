from cycler import cycler
import math
import numpy as np
import os
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
from scipy.optimize import curve_fit

def plotnow(fname,title,xlabel,ylabel,x,y,labels,lstyles,mrks,ptype='line',lims=False):
    default_cycler = (cycler(color=['b'])*\
                      cycler(linestyle=['-'])*cycler(marker=['']))
    plt.rc('lines',linewidth=1)
    plt.rc('axes',prop_cycle=default_cycler)
    fig = plt.figure(figsize=(10,4))
    if(lims):
        fig = plt.figure(figsize=(3,5))
    ax = fig.add_subplot(111)  

    ax.set_xlabel(xlabel,fontsize=15)
    ax.set_ylabel(ylabel,fontsize=15)
    ax.tick_params(axis='both',labelsize=12)

    for i in range(len(y)):
        if(ptype=='line'):
            ax.plot(x[i],y[i],label=labels[i],linestyle=lstyles[i],marker=mrks[i],linewidth = 1.5)
        elif(ptype=='semilogx'):
            ax.semilogx(x[i],y[i],label=labels[i],linestyle=lstyles[i],marker=mrks[i],linewidth=1.5)
        elif(ptype=='semilogy'):
            ax.semilogy(x[i],y[i],label=labels[i],linestyle=lstyles[i],marker=mrks[i])
        else:
            ax.loglog(x[i],y[i],label=labels[i],linestyle=lstyles[i],marker=mrks[i])

    ax.grid()
    #ax.set_title(title,fontsize=15)
    if(lims):
        ax.set_ylim([0.0,3.0])
    ax.legend(loc='best',fontsize=12,ncol=2)
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def main():
    L = 1.397e-3 #Bubble effective dia
    g = 9.81
    rhol = 970.0
    rhog = 1.1839 
    rhoratio = rhol/rhog
    mul = 1.0
    nug = 1.562e-5
    mug = nug * rhog
    gamma = 0.0216
    nul = mul/rhol
    nug = mug/rhog
    flowrate = 10 /60 *1e-6 # m^3/s
    areaInlet = math.pi*(L/2)**2.0
    U = flowrate/areaInlet
    muratio = mul/mug
    nuratio = nul/nug

    print("Density ratio = ",rhol/rhog)
    print("Dynamic Viscosity ratio = ",mul/mug)
    print("Kinematic Viscosity of heavy fluid =",nul)
    print("Kinematic Viscosity of air =",nug)
    print("Kinematic Viscosity ratio = ",nul/nug)
    

    print("Characteristic Velocity = ",U)

    Re = rhol*U*L/mul
    print("Reynolds Number, based on water =",Re)

    print("Reg based on mug/mul/Re = ", 1.0/(mug/mul/Re))
    print("Reg based on nug/nul/Re = ", 1.0/(nug/nul/Re))

    Reg = rhog*U*L/mug
    print("Reynolds Number, based on air =",Reg)

    Fr = U**2/g/L
    print("Froude Number =",Fr)
    print("sqrt of Froude Number = ",math.sqrt(Fr))

    We = rhol*U**2*L/gamma
    print("Weber Number =",We)


    #Based on Fr=1
    L = 1e-3
    U = math.sqrt(g*L)

    print("Fr = 1: U= ",U)
    
    Re = rhol*U*L/mul
    print("Fr = 1; Re = ",Re)

    We = rhol*U**2*L/gamma
    print("Fr = 1; We = ",We)

    
    #inlet profile
    x = np.linspace(-1,1,100,endpoint=True)
    y = 0.5*(np.tanh(1.5*np.pi*(np.abs(x)-0.4)))-0.5
    y = y*0.05*0.1*1000
    
    plotnow('inlet','','$x (mm)$','$v (mm/s)$',[x],[y],[''],['-'],[''])
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
