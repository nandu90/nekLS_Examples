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

def getloc(direc,files,tol,wall):
    loc = []
    time = []

    for f in files:
        if(f+1 < 10):
            fname = direc+'/dam.0000'+str(f+1)+'.dat'
        elif(f+1 >= 10 and f+1 < 100):
            fname = direc+'/dam.000'+str(f+1)+'.dat'
        elif(f+1 >=100 and f+1 < 1000):
            fname = direc+'/dam.00'+str(f+1)+'.dat'
        elif(f+1 >=1000 and f+1 < 10000):
            fname = direc+'/dam.0'+str(f+1)+'.dat'

        print(fname)
        with open(fname,'r') as fn:
            line = fn.readline()
            temp = line.split()
            time.append(float(temp[-1]))
                
        data = np.genfromtxt(fname,skip_header=1)
        if(wall == 'h'):
            y = data[:,0]
        else:
            y = data[:,1]
        cls = data[:,5]-0.5

        if(wall=='h'):
            y = np.flip(y)
            cls = np.flip(cls)
            #print(y,cls)
            #raise SystemExit(1)
        
        tol2 = tol
        y = y[np.abs(cls) < 0.5-tol2]
        cls = cls[np.abs(cls) < 0.5-tol2]

        if(wall=='h'): #otherwise i get erroneous value
            y=y[:20]
            cls=cls[:20]
    
        func = interpolate.interp1d(y,cls,fill_value="extrapolate",kind="linear")
        root = optimize.fsolve(func,np.mean(y))
        print(fname,root)
        loc.append(root)

    loc = np.array(loc).reshape(-1)
    time = np.array(time).reshape(-1)
    return loc, time

def main():
    hfiles = np.arange(0,90,2)
    vfiles = np.arange(1,90,2)
    tol = [1e-3,1e-4,1e-3]

    hwall, time1 = getloc('25X100',hfiles,tol[0],'h')
    vwall, time2 = getloc('25X100',vfiles,tol[0],'v')
    xh = time1
    yh = hwall
    xv = time2
    yv = vwall

    hfiles = np.arange(0,170,2)
    vfiles = np.arange(1,170,2)
    hwall, time1 = getloc('50X200',hfiles,tol[0],'h')
    vwall, time2 = getloc('50X200',vfiles,tol[0],'v')
    xh2 = time1
    yh2 = hwall
    xv2 = time2
    yv2 = vwall
    #print(yh)
    
    hfiles = np.arange(0,148,2)
    vfiles = np.arange(1,148,2)
    hwall, time1 = getloc('.',hfiles,tol[1],'h')
    vwall, time2 = getloc('.',vfiles,tol[0],'v')
    xh3 = time1
    yh3 = hwall
    xv3 = time2
    yv3 = vwall
    #print(yh)

    data = np.loadtxt('exp_front.dat',delimiter=' ')
    xh_exp = data[:,0]
    yh_exp = data[:,1]

    data = np.loadtxt('exp_height.dat',delimiter=' ')
    xv_exp = data[:,0]
    yv_exp = data[:,1]

    labels = ['25X100','50X200','100X400','Martin et al (1952)']
    lines = ['-','--','--','','']
    marks = ['.','','','v','o']

    x = [xh,xh2,xh3,xh_exp]#,x2,x3,xchiu,xg]
    y = [yh,yh2,yh3,yh_exp]#,y2,y3,ychiu,yg]
        
    plotnow('horizontal','$t*$','Surge front location $(x/a)$',x,y,labels,linestyles=lines,markers=marks)

    x = [xv,xv2,xv3,xv_exp]#,x2,x3,xchiu,xg]
    y = [yv,yv2,yv3,yv_exp]#,y2,y3,ychiu,yg]    
    
    plotnow('vertical','$t*$','Column height $(y/a)$',x,y,labels,linestyles=lines,markers=marks)
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
