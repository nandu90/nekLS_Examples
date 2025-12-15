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

COLORS=['#0072B2','#D55E00','#009E73','#CC0000','#990099']

C2 = '#990099'
C3 = '#0072B2'
C4 = '#D55E00'
C5 = '#009E73'
C6 = '#CC0000'

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[],xint=False,colors=[],leg=True,xticks=[],yticks=[],grid=True,printleg=False,ylim=[],xlim=[]):
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

    if(ylim!=[]):
        ax.set_ylim(ylim)

    if(xlim!=[]):
        ax.set_xlim(xlim)

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
    N = np.array((3,4,5,6))
    Er_128 = np.array((1.9644083817968675E-003,1.2505462043959949E-003,9.0074804500609969E-004,7.5801378427325797E-004))
    E1_128 = np.array((1.8254146844088545E-003,1.1621009937442339E-003,8.3705519982045300E-004,7.0352560441701425E-004))
    Es_128 = np.array((3.6506660941431284E-004,1.8843727028095889E-004,1.2337203716325268E-004,8.0736765497260273E-005))
    Ev_128 = np.array((1.6900277217981905E-008,3.2202974948058349E-009,2.9858006055035767E-009,1.3824220209486620E-009))

    Er_64 = np.array((1.0193065884140861E-002,4.2000679346736181E-003,3.2726916086903927E-003,2.4654990246460750E-003))
    E1_64 = np.array((9.4697022275516650E-003,3.9025201829118888E-003,3.0410284438296938E-003,2.2910503037710389E-003))
    Es_64 = np.array((3.0315880961756998E-003,1.1797094041241895E-003,1.0004653370184796E-003,6.0951393037267376E-004))
    Ev_64 = np.array((3.2104170740309537E-006,1.2453082221275868E-006,9.2859093688488435E-008,2.2735482543591080E-007))

    Er_32 = np.array((3.1294708518886778E-002,2.0885617144906263E-002,1.3688639528156177E-002,1.5031589347505449E-002))
    E1_32 = np.array((2.9047565786994224E-002,1.9396119671401313E-002,1.2715520074301899E-002,1.3964855054418860E-002))
    Es_32 = np.array((1.1022049939580498E-002,7.3391989192228922E-003,4.3399399372452624E-003,4.0363397147625815E-003))
    Ev_32 = np.array((3.4494303871338423E-005,2.9297602751318913E-005,6.6520582508711100E-006,7.6671200282072673E-006))

    labels=['$H=1/32$','$H=1/64$','$H=1/128$']
    lines = ['-','-','-','--','--','--']
    marks = ['.','.','.','.','.','.']

    xdata = [N,N,N]
    ydata = [Er_32,Er_64,Er_128]
    plotnow('Er','$N$','$E_r$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)


    labels=['$H=1/32$','$H=1/64$','$H=1/128$']
    xdata = [N,N,N]
    ydata = [Es_32,Es_64,Es_128]
    plotnow('Es','$N$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)
    
    xdata = [N,N,N]
    ydata = [Ev_32,Ev_64,Ev_128]
    plotnow('Ev','$N$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='semilogy',xint=True)

    #h-convergence plots
    H = np.array((32,64,128))
    E1_3 = np.array((E1_32[0],E1_64[0],E1_128[0]))
    E1_4 = np.array((E1_32[1],E1_64[1],E1_128[1]))
    E1_5 = np.array((E1_32[2],E1_64[2],E1_128[2]))
    E1_6 = np.array((E1_32[3],E1_64[3],E1_128[3]))

    Es_3 = np.array((Es_32[0],Es_64[0],Es_128[0]))
    Es_4 = np.array((Es_32[1],Es_64[1],Es_128[1]))
    Es_5 = np.array((Es_32[2],Es_64[2],Es_128[2]))
    Es_6 = np.array((Es_32[3],Es_64[3],Es_128[3]))

    Ev_3 = np.array((Ev_32[0],Ev_64[0],Ev_128[0]))
    Ev_4 = np.array((Ev_32[1],Ev_64[1],Ev_128[1]))
    Ev_5 = np.array((Ev_32[2],Ev_64[2],Ev_128[2]))
    Ev_6 = np.array((Ev_32[3],Ev_64[3],Ev_128[3]))

    H_Salami = np.array((32,64,128))
    E1_3Salami = np.array((6.11e-3,2.14e-3,6.67e-4))
    E1_4Salami = np.array((5.51e-3,1.25e-3,3.79e-4))
    E1_5Salami = np.array((3.97e-3,7.64e-4,2.60e-4))

    Hsv_Salami = np.array((64,128))
    Es_2Salami = np.array((1e-2,3.04e-3))
    Es_3Salami = np.array((4.82e-3,2.33e-3))
    Es_4Salami = np.array((3.72e-3,1.21e-3))

    Ev_2Salami = np.array((3.41e-6,6.12e-7))
    Ev_3Salami = np.array((3.16e-5,1.62e-6))
    Ev_4Salami = np.array((8.03e-6,1.39e-6))

    H_Qian = np.array((32,64,128))
    E1_2Qian = np.array((1e-1,1.22e-2,1.2e-3))
    E1_4Qian = np.array((2.85e-2,3.39e-3,6.79e-4))
    
    H_Jibben = np.array((64,128))
    Es_2Jibben=np.array((2.69e-2,5.56e-3))
    Es_3Jibben=np.array((7.81e-3,1.47e-3))
    Es_4Jibben=np.array((3.43e-3,7.06e-4))

    Ev_2Jibben=np.array((6e-3,4.81e-3))
    Ev_3Jibben=np.array((8.25e-3,2.58e-3))
    Ev_4Jibben=np.array((5.36e-3,1.65e-3))

    labels=['$N=3$','$N=4$','$N=5$','$N=6$','$N=3$ Salami','$N=4$ Salami','$N=5$ Salami','$N=2$ Qian', '$N=4$ Qian']
    lines = ['-','-','-','-','--','--','--',':',':']
    marks = ['o','o','o','o','^','^','^','*','*']
    colors = [C3,C4,C5,C6,C3,C4,C5,C2,C4]
    xdata = [H,H,H,H,H_Salami,H_Salami,H_Salami,H_Qian,H_Qian]
    ydata = [E1_3,E1_4,E1_5,E1_6,E1_3Salami,E1_4Salami,E1_5Salami,E1_2Qian,E1_4Qian]
    plotnow('E1_H','$1/H$','$E_{L1}$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog',colors=colors,leg=False)


    labels=['$N=3$','$N=4$','$N=5$','$N=6$','$N=2$ Salami','$N=3$ Salami','$N=4$ Salami','$N=2$ Jibben', '$N=3$ Jibben', '$N=4$ Jibben']
    lines = ['-','-','-','-','--','--','--','-.','-.','-.']
    marks = ['o','o','o','o','^','^','^','s','s','s']
    colors = [C3,C4,C5,C6,C2,C3,C4,C2,C3,C4]
    xdata = [H,H,H,H,Hsv_Salami,Hsv_Salami,Hsv_Salami,H_Jibben,H_Jibben,H_Jibben]
    ydata = [Es_3,Es_4,Es_5,Es_6,Es_2Salami,Es_3Salami,Es_4Salami,Es_2Jibben,Es_3Jibben,Es_4Jibben]
    plotnow('Es_H','$1/H$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog',colors=colors,leg=False)

    labels=['$N=3$','$N=4$','$N=5$','$N=6$','$N=2$ Salami','$N=3$ Salami','$N=4$ Salami','$N=2$ Jibben', '$N=3$ Jibben', '$N=4$ Jibben']
    lines = ['-','-','-','-','--','--','--','-.','-.','-.']
    marks = ['o','o','o','o','^','^','^','s','s','s']
    colors = [C3,C4,C5,C6,C2,C3,C4,C2,C3,C4]
    xdata = [H,H,H,H,Hsv_Salami,Hsv_Salami,Hsv_Salami,H_Jibben,H_Jibben,H_Jibben]
    ydata = [Ev_3,Ev_4,Ev_5,Ev_6,Ev_2Salami,Ev_3Salami,Ev_4Salami,Ev_2Jibben,Ev_3Jibben,Ev_4Jibben]
    plotnow('Ev_H','$1/H$','$|E_v|$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='loglog',colors=colors,leg=False)

    #faux plot for legend
    labels = ['$N=3$','$N=4$','$N=5$','$N=6$','$N=2$ Al-Salami(2021)','$N=3$ Al-Salami(2021)','$N=4$ Al-Salami(2021)','$N=5$ Al-Salami(2021)','$N=2$ Qian(2018)','$N=4$ Qian(2018)','$N=2$ Jibben(2017)','$N=3$ Jibben(2017)','$N=4$ Jibben(2017)']
    lines = ['-','-','-','-','--','--','--','--',':',':','-.','-.','-.']
    marks = ['o','o','o','o','^','^','^','^','*','*','s','s','s']
    colors=[C3,C4,C5,C6,C2,C3,C4,C5,C2,C4,C2,C3,C4]
    x = np.linspace(0,1,50)
    y = np.ones(50)
    xdata = [x,x,x,x,x,x,x,x,x,x,x,x,x,x]
    ydata = [y,y,y,y,y,y,y,y,y,y,y,y,y]
    plotnow('legend','$H$','$E_s$',xdata,ydata,labels,linestyles=lines,markers=marks,ptype='line',colors=colors,leg=True,grid=False,printleg=True)

    #plot Ev v/s time error
    lines = [':','-.','--']
    marks = ['','','']
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
