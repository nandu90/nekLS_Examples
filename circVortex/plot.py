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
    E1_128 = np.array((3.4973664109247179E-003,2.7353058105014636E-003,2.2753839592227045E-003))
    Er_128 = np.array((9.1881452266445588E-009,4.9906052288788767E-009,3.0500675716882824E-009))
    Es_128 = np.array((3.3918146579391757E-004,2.3724319588755286E-004,1.2934452098195266E-004))
    Ev_128 = np.array((1.4289965520301566E-008,1.8191496372769275E-009,1.8752644581514245E-010))

    E1_64 = np.array((8.3160647181998119E-003,6.4891829748837671E-003,5.4095683269066840E-003))
    Er_64 = np.array((8.7409629260343270E-008,4.7363879034529375E-008,2.9009616983009505E-008))
    Es_64 = np.array((2.3257916570713095E-003,1.7416216307658387E-003,1.1894996964210906E-003))
    Ev_64 = np.array((3.6222280459454887E-007,4.3471158529305004E-007,6.5791595603375606E-008))

    E1_32 = np.array((2.6204994042541275E-002,1.8314957454482944E-002,1.9083500639948937E-002))
    Er_32 = np.array((1.0998024947555822E-006,5.3447799499468713E-007,4.0896428947879292E-007))
    Es_32 = np.array((1.2722918046146130E-002,7.1881650346862537E-003,7.4791870068928916E-003))
    Ev_32 = np.array((3.2924414880027399E-005,2.1497539642158136E-005,2.0018750009341009E-006))

    labels=['$H=1/32$','$H=1/64$','$H=1/128$','$H=1/32$ (Salami)','$H=1/64$ (Salami)','$H=1/128$ (Salami)']
    lines = ['-','-','-','--','--','--']
    marks = ['.','.','.','.','.','.']

    N_Salami = np.array((2,3,4,5))
		#Table 7 from Salami et al
    E1_32Salami = np.array((7.96e-3,7.91e-3,5.50e-3,3.22e-3))
    E1_64Salami = np.array((2.51e-3,1.29e-3,1.05e-3,7.46e-4))
    E1_128Salami = np.array((8.10e-4,6.72e-4,3.75e-4,2.64e-4))
    
    xdata = [N,N,N,N_Salami,N_Salami,N_Salami]
    ydata = [E1_32,E1_64,E1_128,E1_32Salami,E1_64Salami,E1_128Salami]
    plotnow('E1','$N$','$E_1$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)

    xdata = [N,N,N]
    ydata = [Er_32,Er_64,Er_128]
    plotnow('Er','$N$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)

    N_Salami = np.array((2,3,4))
    r = 0.15
    fac = 2 * 2 * math.pi * r
    Es_64Salami = np.array((1e-2,4.82e-3,3.72e-3)) * fac
    Es_128Salami = np.array((3.04e-3,2.33e-3,1.21e-3)) * fac
    
    labels=['$H=1/32$','$H=1/64$','$H=1/128$','$H=1/64$ (Salami)','$H=1/128$ (Salami)']
    xdata = [N,N,N,N_Salami,N_Salami]
    ydata = [Es_32,Es_64,Es_128,Es_64Salami,Es_128Salami]
    plotnow('Es','$N$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)
    
    Ev_64Salami = np.array((3.41e-6,3.16e-5,8.03e-6))
    Ev_128Salami = np.array((6.12e-7,1.62e-6,1.39e-6))
    xdata = [N,N,N,N_Salami,N_Salami]
    ydata = [Ev_32,Ev_64,Ev_128,Ev_64Salami,Ev_128Salami]
    plotnow('Ev','$N$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)

    #h-convergence plots
    H = np.array((1/32, 1/64, 1/128))
    Er_4 = np.array((Er_32[0], Er_64[0], Er_128[0]))
    Es_4 = np.array((Es_32[0], Es_64[0], Es_128[0]))
    Ev_4 = np.array((Ev_32[0], Ev_64[0], Ev_128[0]))

    Er_5 = np.array((Er_32[1], Er_64[1], Er_128[1]))
    Es_5 = np.array((Es_32[1], Es_64[1], Es_128[1]))
    Ev_5 = np.array((Ev_32[1], Ev_64[1], Ev_128[1]))
    
    Er_6 = np.array((Er_32[2], Er_64[2], Er_128[2]))
    Es_6 = np.array((Es_32[2], Es_64[2], Es_128[2]))
    Ev_6 = np.array((Ev_32[2], Ev_64[2], Ev_128[2]))

    #Salami et al: https://doi.org/10.1016/j.jcp.2021.110376 (Table 6)
    H_salami = np.array((1/64, 1/128))
    Es4_salami = np.array((3.72e-3, 1.21e-3))
    Ev4_salami = np.array((8.03e-6, 1.39e-6))


    labels=['$N=4$','$N=5$','$N=6$','Salami et al (N=4)']
    lines = [':','-.','--','--','-']
    marks = ['.','.','.','','']
    xdata = [H,H,H]
    
    ydata = [Er_4,Er_5,Er_6]
    plotnow('h-Er','$H$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog')

    xdata.append(H_salami)
    ydata = [Es_4,Es_5,Es_6,Es4_salami]
    plotnow('h-Es','$H$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog')
    
    ydata = [Ev_4,Ev_5,Ev_6,Ev4_salami]
    plotnow('h-Ev','$H$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog')

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
		#128 mesh
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

		#64 mesh
    x4,psi4,phi4 = getLineData('64/4') 
    x5,psi5,phi5 = getLineData('64/5') 
    x6,psi6,phi6 = getLineData('64/6') 

    data = np.loadtxt('64/6/cv.00001.dat',skiprows=1)
    xini = data[:,0]
    yini = data[:,4]

    xdata = [x4,x5,x6,xini]
    ydata = [psi4,psi5,psi6,yini]
    marks = ['','','','']
    labels=['$N=4$','$N=5$','$N=6$','Initial']
    lines = ['-.','-.','-.',':','-']
    plotnow('psi64','$x$','$\\psi$',xdata,ydata,labels,linestyles=lines,markers=marks,xlim=[0.25,0.75])

    xdata = [x4,x5,x6,xini]
    exact = np.sqrt((xini-0.5)**2) - 0.15
    ydata = [phi4,phi5,phi6,exact]
    marks = ['','','','']
    
    labels=['$N=4$','$N=5$','$N=6$','Exact']
    lines = ['-.','-.','-.',':','-']
    plotnow('phi64','$x$','$\\phi$',xdata,ydata,labels,linestyles=lines,markers=marks,ylim=[-0.1,0.1],xlim=[0.25,0.75])

		#32 mesh
    x4,psi4,phi4 = getLineData('32/4') 
    x5,psi5,phi5 = getLineData('32/5') 
    x6,psi6,phi6 = getLineData('32/6') 

    data = np.loadtxt('32/6/cv.00001.dat',skiprows=1)
    xini = data[:,0]
    yini = data[:,4]

    xdata = [x4,x5,x6,xini]
    ydata = [psi4,psi5,psi6,yini]
    marks = ['','','','']
    labels=['$N=4$','$N=5$','$N=6$','Initial']
    lines = ['-.','-.','-.',':','-']
    plotnow('psi32','$x$','$\\psi$',xdata,ydata,labels,linestyles=lines,markers=marks,xlim=[0.25,0.75])

    xdata = [x4,x5,x6,xini]
    exact = np.sqrt((xini-0.5)**2) - 0.15
    ydata = [phi4,phi5,phi6,exact]
    marks = ['','','','']
    
    labels=['$N=4$','$N=5$','$N=6$','Exact']
    lines = ['-.','-.','-.',':','-']
    plotnow('phi32','$x$','$\\phi$',xdata,ydata,labels,linestyles=lines,markers=marks,ylim=[-0.1,0.1],xlim=[0.25,0.75])
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
