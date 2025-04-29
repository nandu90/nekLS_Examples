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
    fig.savefig(fname+'.pdf',\
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
        
        tol2 = tol
        if((direc == 'finest/') & (f == files[-1])):
            tol2 = 1e-2
        y = y[np.abs(cls) < 0.5-tol2]
        cls = cls[np.abs(cls) < 0.5-tol2]
    
        func = interpolate.interp1d(y,cls,fill_value="extrapolate",kind="linear")
        root = optimize.fsolve(func,np.mean(y))
        #print(fname,root)
        loc.append(root)

    loc = np.array(loc).reshape(-1)
    time = np.array(time).reshape(-1)
    return loc, time

def geterr(fname):
    data = np.loadtxt(fname+'vol.dat')
    t = data[:,0]*1.25e-4
    err = np.abs(data[:,1])
    return t,err

def main():
    nosefiles = np.arange(0,50,2)
    neckfiles = np.arange(1,50,2)
    tol = [1e-1,1e-2,1e-2]

    nose, time1 = getloc('coarse/',nosefiles,tol[0])
    neck, time2 = getloc('coarse/',neckfiles,tol[0])
    x1 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y1 = np.concatenate((nose,np.array([np.nan]),neck))

    nose, time1 = getloc('fine/',nosefiles,tol[1])
    neck, time2 = getloc('fine/',neckfiles,tol[1])
    x2 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y2 = np.concatenate((nose,np.array([np.nan]),neck))

    nose, time1 = getloc('finest/',nosefiles,tol[2])
    neck, time2 = getloc('finest/',neckfiles,tol[2])
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
    labels = ['$H=1/25$','$H=1/50$','$H=1/100$','Chiu et al','Guermond et al']
    lines = [':','-.','--','','']
    marks = ['','','','v','o']
    
    plotnow('location','$t$','$y$',x,y,labels,linestyles=lines,markers=marks)


    #plot location for N
    nose, time1 = getloc('fine/3/',nosefiles,tol[0])
    neck, time2 = getloc('fine/3/',neckfiles,tol[0])
    x1 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y1 = np.concatenate((nose,np.array([np.nan]),neck))

    nose, time1 = getloc('fine/',nosefiles,tol[1])
    neck, time2 = getloc('fine/',neckfiles,tol[1])
    x2 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y2 = np.concatenate((nose,np.array([np.nan]),neck))

    nose, time1 = getloc('fine/5/',nosefiles,tol[2])
    neck, time2 = getloc('fine/5/',neckfiles,tol[2])
    x3 = np.concatenate((time1,np.array([np.amax(time1)]),time2))
    y3 = np.concatenate((nose,np.array([np.nan]),neck))
    x = [x1,x2,x3,xchiu,xg]
    y = [y1,y2,y3,ychiu,yg]
    labels = ['$N3$','$N4$','$N5$','Chiu et al','Guermond et al']
    lines = [':','-.','--','','']
    marks = ['','','','v','o']
    
    plotnow('location_N','$t$','$y$',x,y,labels,linestyles=lines,markers=marks)

    

    #plot vol err
    t1,e1 = geterr('coarse/')
    t2,e2 = geterr('fine/')
    t3,e3 = geterr('finest/')
    labels = ['$H=1/25$','$H=1/50$','$H=1/100$']
    lines = [':','-.','--','','']
    marks = ['','','']
    x = [t1,t2,t3]
    y = [e1,e2,e3]
    plotnow('Ev','$t$','$|E_v|$',x,y,labels,linestyles=lines,markers=marks,ptype='semilogy')

    t1,e1 = geterr('fine/3/')
    t2,e2 = geterr('fine/')
    t3,e3 = geterr('fine/5/')
    labels = ['$N3$','$N4$','$N5$']
    lines = [':','-.','--','','']
    marks = ['','','']
    x = [t1,t2,t3]
    y = [e1,e2,e3]
    plotnow('Ev_N','$t$','$|E_v|$',x,y,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
