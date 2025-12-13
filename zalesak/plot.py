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
from matplotlib.ticker import LogLocator, NullFormatter

COLORS=['#0072B2','#D55E00','#009E73','#CC0000','#990099']

C2 = '#990099'
C3 = '#0072B2'
C4 = '#D55E00'
C5 = '#009E73'
C7 = '#CC0000'

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[],xint=False,colors=[],leg=True,xticks=[],yticks=[],grid=True,printleg=False):
    if(colors==[]):
        default_cycler = (cycler(color=COLORS)*cycler(linestyle=['-'])*cycler(marker=['']))
    else:
        default_cycler = (cycler(color=colors)*cycler(linestyle=['-'])*cycler(marker=['']))

    plt.rc('lines',linewidth=1)
    plt.rc('axes',prop_cycle=default_cycler)
    fig = plt.figure(figsize=(8,5))
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
        print(x[i])
        print(y[i])
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

    if(grid):
        ax.grid()
    if(leg):
        legend = ax.legend(loc='best',fontsize=12)

    # if(xticks !=[]):
    #     ax.set_xticks(xticks)
    #     ax.set_xticklabels(str(v) for v in xticks)

    if(yticks!=[]):
        ax.set_yscale('log')
        ax.set_yticks(yticks)
        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=range(2,9)))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.tick_params(axis='both', which='minor', length=4, width=0.8)

    fig.savefig(fname+'.pdf',\
                bbox_inches='tight',dpi=100)
    fig.savefig(fname+'.png',\
                bbox_inches='tight',dpi=100)
    plt.close(fig)

    if(printleg):
        fig_legend = plt.figure(figsize=(4, 5))

        fig_legend.legend(
            handles=legend.legendHandles,
            labels=[t.get_text() for t in legend.get_texts()],
            loc='center'
        )
        
        fig_legend.gca().axis('off')
        

        fig_legend.savefig("legend_only.png", dpi=100, bbox_inches='tight')
        fig_legend.savefig("legend_only.pdf", dpi=100, bbox_inches='tight')
        plt.close(fig_legend)
    
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

def getdata(case,t=1):
    if(t==1):
        tname = 'zale.00001.dat'
    else:
        tname = 'zale.00002.dat'

    data = np.loadtxt(case+'/'+tname,skiprows=1)
    x = data[:,0]
    exact = data[:,5][(np.abs(x) > 0.3) & (np.abs(x) < 0.7)]
    svv = data[:,7][(np.abs(x) > 0.3) & (np.abs(x) < 0.7)]
    x = data[:,0][(np.abs(x) > 0.3) & (np.abs(x) < 0.7)]
    return x,exact,svv

def main():
    #Calculate the perimeter of the disk
    r = 0.15
    circum = 2*math.pi*r
    
    theta = math.asin(0.025/r)
    sector_angle = 2*math.pi - 2*theta
    sector = (sector_angle/(2*math.pi)) * circum

    side = abs(math.sqrt(r**2 - 0.025**2)) + 0.85-0.75

    total = side*2 + 0.025*2 + sector
    print("perimeter", total)
    
    N = 'N5'
    xdata = []
    ydata = []

    x,exact,svv = getdata(N+'/0.5')
    xdata.append(x)
    ydata.append(exact)
    xdata.append(x)
    ydata.append(svv)

    x,exact,svv = getdata(N+'/1')
    xdata.append(x)
    ydata.append(svv)

    x,exact,svv = getdata(N+'/1.5')
    xdata.append(x)
    ydata.append(svv)
    
    labels=['Initial','$\\xi=0.5/N$','$\\xi=1/N$','$\\xi=1.5/N$']
    lines = [':','-.','--','--','-']
    marks = ['','','','','']
    plotnow('t2_'+N,'$x$','$\\psi$',xdata,ydata,labels,linestyles=lines,markers=marks)

    xdata = []
    ydata = []

    x,exact,svv = getdata(N+'/0.5',t=100)
    xdata.append(x)
    ydata.append(exact)
    xdata.append(x)
    ydata.append(svv)

    x,exact,svv = getdata(N+'/1',t=100)
    xdata.append(x)
    ydata.append(svv)

    x,exact,svv = getdata(N+'/1.5',t=100)
    xdata.append(x)
    ydata.append(svv)
    
    plotnow('t20_'+N,'$x$','$\\psi$',xdata,ydata,labels,linestyles=lines,markers=marks)


    #Errors for 50X50 grid
    N = np.array((3,5,7,9))

    Er1 = np.array((8.3130566705629697E-002,3.4974836452832760E-002,1.5512210263916176E-002,8.7796087584110644E-003))
    Er2 = np.array((0.34824456505488383,0.16034332757664410,7.9564941840439857E-002,4.8781233538905767E-002))
    Es1 = np.array((1.4116554015712525E-002,3.4178854021710877E-003,3.6872816120792762E-004,3.2773514374618358E-004))
    Evol1 = np.array((3.4181759147926075E-006,1.7630427772835978E-008,2.9527388513658964E-011,3.5995022556439827E-013))

    Er10 = np.array((0.25797926741078331,8.6702130998735999E-002,3.7338128219991253E-002,1.9655872363802295E-002))
    Er20 = np.array((0.96541859757505810,0.35775961352530555,0.17250115305451461,0.10209023646241060))
    Es10 = np.array((3.2531574306105725E-002,1.3522707345099811E-003,7.8513899232997514E-004,4.6617152922997612E-004))
    Evol10 = np.array((3.4417283104374070E-005,1.7571916190260711E-007,3.1135293696234736E-010,4.1190069973368271E-012))

    lines = ['-','--']
    labels = ['$t=2$','$t=20$']
    marks = ['.','.']
    xdata = [N,N]
    
    ydata = [Er1,Er10]
    plotnow('relErr','$N$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')

    ydata = [Er2,Er20]
    plotnow('rel2Err','$N$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')

    ydata = [Evol1,Evol10]
    plotnow('volErr','$N$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')

    ydata = [Es1,Es10]
    plotnow('shapeErr','$N$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy')

    #Errors for 100X100 grid
    Er = np.array((6.7997872139337584E-002,2.4643036672224363E-002,1.0607091360067693E-002))
    Es = np.array((2.0241636945789641E-003,5.1377664875592525E-004,1.3987169063662963E-004))
    Ev = np.array((4.0443789879194159E-007,2.2296001487834778E-009,5.0550834957104743E-012))
    
    Er_Salami = np.array((1e-2,3.49e-3,2.82e-3,1.63e-3))
    Es_Salami = np.array((2.63e-3,6.02e-4,4.38e-4))
    Ev_Salami = np.array((1.19e-6,4.52e-6,3.77e-6))

    #Errors for 200X200 grid
    Er_200 = np.array((4.8184062740931469E-002,1.6450047965514962E-002,7.0090079207108464E-003))
    Es_200 = np.array((2.2110965752756779E-003,7.2261028410744714E-004,3.6792344649443006E-004))
    Ev_200 = np.array((4.9767753684283299E-008,2.6045146242288497E-010,2.8777495125669633E-012))
    
    Er_Salami200 = np.array((4.69e-3,1.54e-3,9.12e-4,8.08e-4))
    Es_Salami200 = np.array((8.45e-4,2.88e-4,2.12e-4))
    Ev_Salami200 = np.array((9.92e-8,1.71e-7,1.75e-7))

    H_Qian = np.array((50,100,200))
    Er2_Qian = np.array((6.4e-2,1.47e-2,7.04e-3)) #P2 order
    Er4_Qian = np.array((3.64e-2,9.98e-3,3.99e-3)) #P4 order

    H_Jibben = np.array((50,100,200))
    Ev3_Jibben = np.array((4.43e-4,8.29e-5,2.42e-5))
    Es3_Jibben = np.array((1.07e-3,3.45e-4,1.47e-4))
    Ev4_Jibben = np.array((1.06e-5,9.23e-5,4.95e-6))
    Es4_Jibben = np.array((4.83e-4,1.66e-4,5.49e-5))

    #Make h-convergence arrays
    Er3 = np.array((Er1[0],Er[0],Er_200[0]))
    Er5 = np.array((Er1[1],Er[1],Er_200[1]))
    Er7 = np.array((Er1[2],Er[2],Er_200[2]))
    Es3 = np.array((Es1[0],Es[0],Es_200[0]))
    Es5 = np.array((Es1[1],Es[1],Es_200[1]))
    Es7 = np.array((Es1[2],Es[2],Es_200[2]))
    Ev3 = np.array((Evol1[0],Ev[0],Ev_200[0]))
    Ev5 = np.array((Evol1[1],Ev[1],Ev_200[1]))
    Ev7 = np.array((Evol1[2],Ev[2],Ev_200[2]))
    
    Er2_Salami = np.array((Er_Salami[0],Er_Salami200[0]))
    Er3_Salami = np.array((Er_Salami[1],Er_Salami200[1]))
    Er4_Salami = np.array((Er_Salami[2],Er_Salami200[2]))
    Er5_Salami = np.array((Er_Salami[3],Er_Salami200[3]))
    Es2_Salami = np.array((Es_Salami[0],Es_Salami200[0]))
    Es3_Salami = np.array((Es_Salami[1],Es_Salami200[1]))
    Es4_Salami = np.array((Es_Salami[2],Es_Salami200[2]))
    Ev2_Salami = np.array((Ev_Salami[0],Ev_Salami200[0]))
    Ev3_Salami = np.array((Ev_Salami[1],Ev_Salami200[1]))
    Ev4_Salami = np.array((Ev_Salami[2],Ev_Salami200[2]))
                
    H = np.array((50,100,200))
    H_Salami = np.array((100,200))
    
    labels = ['$N=3$','$N=5$','$N=7$','$N=2$ Al-Salami','$N=3$ Salami','$N=4$ Salami','$N=5$ Salami','$N=2$ Qian','$N=4$ Qian']
    lines = ['-','-','-','--','--','--','--',':',':']
    marks = ['o','o','o','^','^','^','^','*','*']
    colors=[C3,C5,C7,C2,C3,C4,C5,C2,C4]
    xdata = [H, H, H, H_Salami, H_Salami, H_Salami, H_Salami, H_Qian, H_Qian]
    ydata = [Er3,Er5,Er7,Er2_Salami,Er3_Salami,Er4_Salami,Er5_Salami,Er2_Qian,Er4_Qian]
    xticks = [50,100,200]
    plotnow('Er','$1/H$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog',colors=colors,leg=False,xticks=xticks)

    labels = ['$N=3$','$N=5$','$N=7$','$N=2$ Salami','$N=3$ Salami','$N=4$ Salami','$N=3$ Jibben','$N=4$ Jibben']
    lines = ['-','-','-','--','--','--','-.','-.']
    marks = ['o','o','o','^','^','^','s','s']
    colors=[C3,C5,C7,C2,C3,C4,C3,C4]
    xdata = [H,H,H,H_Salami,H_Salami,H_Salami,H_Jibben,H_Jibben]
    ydata = [Ev3,Ev5,Ev7,Ev2_Salami,Ev2_Salami,Ev4_Salami,Ev3_Jibben,Ev4_Jibben]
    yticks = [1e-3,1e-4,1e-5,1e-6,1e-7,1e-8,1e-9,1e-10,1e-11,1e-12]
    plotnow('Ev','$1/H$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog',colors=colors,leg=False,xticks=xticks,yticks=yticks)

    xdata = [H,H,H,H_Salami,H_Salami,H_Salami,H_Jibben,H_Jibben]
    ydata = [Es3,Es5,Es7,Es2_Salami,Es3_Salami,Es4_Salami,Es3_Jibben,Es4_Jibben]
    plotnow('Es','$1/H$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog',colors=colors,leg=False,xticks=xticks)

    
    #faux plot for legend
    labels = ['$N=3$','$N=5$','$N=7$','$N=2$ Al-Salami(2021)','$N=3$ Al-Salami(2021)','$N=4$ Al-Salami(2021)','$N=5$ Al-Salami(2021)','$N=2$ Qian(2018)','$N=4$ Qian(2018)','$N=3$ Jibben(2017)','$N=4$ Jibben(2017)']
    lines = ['-','-','-','--','--','--','--',':',':','-.','-.']
    marks = ['o','o','o','^','^','^','^','*','*','s','s']
    colors=[C3,C5,C7,C2,C3,C4,C5,C2,C4,C3,C4]
    x = np.linspace(0,1,50)
    y = np.ones(50)
    xdata = [x,x,x,x,x,x,x,x,x,x,x]
    ydata = [y,y,y,y,y,y,y,y,y,y,y]
    plotnow('legend','$H$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='line',colors=colors,leg=True,grid=False,printleg=True)

    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
