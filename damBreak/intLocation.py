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
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def getloc(direc,files,tol,wall,if3d=False):
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

        if(if3d):
            cls = data[:,7] - 0.5
        else:
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

def getEvdata(fname):
    data = np.loadtxt(fname+'/vol.dat')
    t = data[:,0]
    Ev = np.abs(data[:,1])
    div1 = np.abs(data[:,2])
    div2 = data[:,3]
    
    return t,Ev,div1,div2

def main():
    hfiles = np.arange(0,70,2)
    vfiles = np.arange(1,78,2)
    tol = [1e-2,1e-3,1e-3]

    hwall, time1 = getloc('40X160/3',hfiles,tol[0],'h')
    vwall, time2 = getloc('40X160/3',vfiles,tol[0],'v')
    xh = time1
    yh = hwall
    xv = time2
    yv = vwall

    hwall, time1 = getloc('40X160/5',hfiles,tol[0],'h')
    vwall, time2 = getloc('40X160/5',vfiles,tol[0],'v')
    xh2 = time1
    yh2 = hwall
    xv2 = time2
    yv2 = vwall
    #print(yh)
    
    hwall, time1 = getloc('40X160/7',hfiles,tol[0],'h')
    vwall, time2 = getloc('40X160/7',vfiles,tol[0],'v')
    xh3 = time1
    yh3 = hwall
    xv3 = time2
    yv3 = vwall

    hwall, time1 = getloc('40X160/9',hfiles,tol[0],'h')
    vwall, time2 = getloc('40X160/9',vfiles,tol[0],'v')
    xh4 = time1
    yh4 = hwall
    xv4 = time2
    yv4 = vwall


    data = np.loadtxt('exp_front.dat',delimiter=' ')
    xh_exp = data[:,0]
    yh_exp = data[:,1]

    data = np.loadtxt('exp_height.dat',delimiter=' ')
    xv_exp = data[:,0]
    yv_exp = data[:,1]

    data = np.loadtxt('phasta.csv',delimiter=',')
    xh_phasta = data[:,0]
    yh_phasta = data[:,1]

    data = np.loadtxt('phasta_h.csv',delimiter=',')
    xv_phasta = data[:,0]
    yv_phasta = data[:,1]

    labels = ['$N=3$','$N=5$','$N=7$','$N=9$','Martin et al (1952)','Rodriguez et al (2013)']
    lines = [':','-.','--','--','','']
    marks = ['','','','','v','*']

    x = [xh,xh2,xh3,xh4,xh_exp,xh_phasta]#,x2,x3,xchiu,xg]
    y = [yh,yh2,yh3,yh4,yh_exp,yh_phasta]#,y2,y3,ychiu,yg]
        
    plotnow('horizontal_N','$t^*$','$x/L$',x,y,labels,linestyles=lines,markers=marks)

    x = [xv,xv2,xv3,xv4,xv_exp,xv_phasta]#,x2,x3,xchiu,xg]
    y = [yv,yv2,yv3,yv4,yv_exp,yv_phasta]#,y2,y3,ychiu,yg]    
    
    plotnow('vertical_N','$t^*$','$y/L$',x,y,labels,linestyles=lines,markers=marks)

    #plot different N
    hwall, time1 = getloc('40X160/5_P1',hfiles,tol[0],'h')
    vwall, time2 = getloc('40X160/5_P1',vfiles,tol[0],'v')
    xh = time1
    yh = hwall
    xv = time2
    yv = vwall

    hwall, time1 = getloc('40X160/5',hfiles,tol[0],'h')
    vwall, time2 = getloc('40X160/5',vfiles,tol[0],'v')
    xh2 = time1
    yh2 = hwall
    xv2 = time2
    yv2 = vwall
    #print(yh)
    
    #print(yh)

    labels = ['P1','P2','Martin et al (1952)','Rodriguez et al (2013)']
    lines = ['--','--','','','']
    marks = ['','','v','*','v']

    x = [xh,xh2,xh_exp,xh_phasta]#,x2,x3,xchiu,xg]
    y = [yh,yh2,yh_exp,yh_phasta]#,y2,y3,ychiu,yg]
        
    plotnow('horizontal_p','$t^*$','$x/L$',x,y,labels,linestyles=lines,markers=marks)

    x = [xv,xv2,xv_exp,xv_phasta]#,x2,x3,xchiu,xg]
    y = [yv,yv2,yv_exp,yv_phasta]#,y2,y3,ychiu,yg]    
    
    plotnow('vertical_p','$t^*$','$y/L$',x,y,labels,linestyles=lines,markers=marks)

    #2D vs 3D
    hfiles = np.arange(0,36,2)
    vfiles = np.arange(1,36,2)
    hwall, time1 = getloc('40X160/5',hfiles,tol[0],'h')
    vwall, time2 = getloc('40X160/5',vfiles,tol[0],'v')
    xh = time1
    yh = hwall
    xv = time2
    yv = vwall

    hwall, time1 = getloc('../damBreak3D',hfiles,tol[0],'h',if3d=True)
    vwall, time2 = getloc('../damBreak3D',vfiles,tol[0],'v',if3d=True)
    xh2 = time1
    yh2 = hwall
    xv2 = time2
    yv2 = vwall
    #print(yh)
    
    #print(yh)

    labels = ['2D','3D','Martin et al (1952)','Rodriguez et al (2013)']
    lines = [':','--','','','']
    marks = ['','','v','*','v']

    x = [xh,xh2,xh_exp,xh_phasta]#,x2,x3,xchiu,xg]
    y = [yh,yh2,yh_exp,yh_phasta]#,y2,y3,ychiu,yg]
        
    plotnow('horizontal_23','$t^*$','$x/L$',x,y,labels,linestyles=lines,markers=marks)

    x = [xv,xv2,xv_exp,xv_phasta]#,x2,x3,xchiu,xg]
    y = [yv,yv2,yv_exp,yv_phasta]#,y2,y3,ychiu,yg]    
    
    plotnow('vertical_23','$t^*$','$y/L$',x,y,labels,linestyles=lines,markers=marks)

    #VOl err plot
    t,Ev,d1,d2 = getEvdata('40X160/3')
    xdata = [t]
    ydata = [Ev]
    div = [d2]
    div1 = [d1]
    t,Ev,d1,d2 = getEvdata('40X160/5')
    xdata.append(t)
    ydata.append(Ev)
    div.append(d2)
    div1.append(d1)
    t,Ev,d1,d2 = getEvdata('40X160/7')
    xdata.append(t)
    ydata.append(Ev)
    div.append(d2)
    div1.append(d1)
    t,Ev,d1,d2 = getEvdata('40X160/9')
    xdata.append(t)
    ydata.append(Ev)
    div.append(d2)
    div1.append(d1)
    labels = ['$N=3$','$N=5$','$N=7$','$N=9$']
    lines = [':','-.','--','--']
    marks = ['','','','']

    plotnow('Ev','$t$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    plotnow('div','$t$','$E_{div}$',xdata,div,labels,linestyles=lines,markers=marks,ptype='semilogy')

    plotnow('div1','$t$','$E_{div}$',xdata,div1,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
