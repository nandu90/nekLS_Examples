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

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[]):
    default_cycler = (cycler(color=['k','b','r','g','k','k'])*\
                      cycler(linestyle=['-'])*cycler(marker=['']))
    plt.rc('lines',linewidth=1)
    plt.rc('axes',prop_cycle=default_cycler)
    fig = plt.figure(figsize=(10,5))
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
            ax.plot(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i],linewidth=1.5)
        elif(ptype=='semilogx'):
            ax.semilogx(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
        elif(ptype=='semilogy'):
            ax.semilogy(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
        else:
            ax.loglog(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
    
            
    ax.grid()
    ax.legend(loc='best',fontsize=12)
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def getloc(direc,files,tol):
    loc = []
    time = []

    for f in files:
        if(f+1 < 10):
            fname = direc+'rt.0000'+str(f+1)+'.dat'
        elif(f+1 >= 10 & f+1 < 100):
            fname = direc+'rt.000'+str(f+1)+'.dat'
        elif(f+1 >=100 & f+1 < 1000):
            fname = direc+'rt.00'+str(f+1)+'.dat'

        print(fname)
        with open(fname,'r') as fn:
            line = fn.readline()
            temp = line.split()
            time.append(float(temp[-1]))
                
        data = np.genfromtxt(fname,skip_header=1)
        y = data[:,1]-2.0
        cls = data[:,5]-0.5
        
        y = y[np.abs(cls) < 0.5-tol]
        cls = cls[np.abs(cls) < 0.5-tol]
    
        func = interpolate.interp1d(y,cls,fill_value="extrapolate",kind="linear")
        root = optimize.fsolve(func,np.mean(y))
        #print(fname,root)
        loc.append(root)

    loc = np.array(loc).reshape(-1)
    time = np.array(time).reshape(-1)
    return loc, time

def main():
    nosefiles = np.arange(0,50,2)
    neckfiles = np.arange(1,50,2)
    tol = 1e-2

    nose, time1 = getloc('',nosefiles,tol)
    neck, time2 = getloc('',neckfiles,tol)
    x1 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y1 = np.concatenate((nose,np.array([np.nan]),neck))

    nose, time1 = getloc('fine/',nosefiles,tol)
    neck, time2 = getloc('fine/',neckfiles,tol)
    x2 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y2 = np.concatenate((nose,np.array([np.nan]),neck))

    nose, time1 = getloc('finest/',nosefiles,tol)
    neck, time2 = getloc('finest/',neckfiles,tol)
    x3 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y3 = np.concatenate((nose,np.array([np.nan]),neck))

    data = np.loadtxt('chiu.csv',delimiter=',')
    xchiu = data[:,0]
    ychiu = data[:,1]

    data = np.loadtxt('guermond.csv',delimiter=',')
    xg = data[:,0]
    yg = data[:,1]

    x = [x1,x2,x3,xchiu,xg]
    y = [y1,y2,y3,ychiu,yg]
    labels = ['$25X100$','$50X200$','$100X400$','Chiu et al','Guermond et al']
    lines = ['--','--','--','','']
    marks = ['','','','v','o']
    
    plotnow('location','$t*$','$y$',x,y,labels,linestyles=lines,markers=marks)
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
