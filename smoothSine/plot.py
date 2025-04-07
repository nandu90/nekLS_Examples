from cycler import cycler
import math
import numpy as np
import os
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress

def plotnow(fname,xlabel,ylabel,x,y,labels,ptype='line',linestyles=[],markers=[]):
    default_cycler = (cycler(color=['#0072B2','#D55E00','#009E73','#CC0000','#990099'])*\
                      cycler(linestyle=['-'])*cycler(marker=['']))
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
            ax.semilogx(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
        elif(ptype=='semilogy'):
            ax.semilogy(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
        else:
            ax.loglog(x[i],y[i],label=labels[i],linestyle=linestyles[i],marker=markers[i])
    
            
    ax.grid()
    ax.legend(loc='best',fontsize=12)
    fig.savefig(fname+'.pdf',\
                bbox_inches='tight',dpi=100)
    plt.close()
    return

def main():
    off = np.array((2.9407653500005489E-004,2.7446071175460241E-005,9.7980712022381672E-007,4.8428234039750572E-008,3.6616323976729894E-009,2.0930346847838373E-009))
    avm = np.array((2.0917531408130865E-003,9.8193860029867895E-004,1.1064561251340115E-004,4.4376863120931637E-006,3.3604294240006035E-007,8.9927558159165148E-009))
    svv001 = np.array((3.5841099463738291E-004,7.9266172105008423E-005,1.4442370375877842E-005,3.2332285994201016E-006,6.8273918305761940E-007,1.5394116816135325E-007))
    svv01 = np.array((2.6844443026326076E-003,7.0517521145041452E-004,1.4764294701446155E-004,3.2398716850955383E-005,6.9767745406128726E-006,1.5161241616575030E-006))
    svv1 = np.array((2.2240900396324238E-002,6.4241671600228237E-003,1.6194123203320027E-003,3.7265757955317876E-004,7.7291505937193849E-005,1.5795367166704694E-005))

    svvN001 = np.array((2.6972242396051146E-004,2.5314613882300640E-005,9.5795911780949055E-007,8.8083081608950671E-008,9.7121146746926355E-009,2.4466047996992587E-009))
    svvN01 = np.array((3.4467326606398420E-004,5.4688336692478025E-005,3.7333925034096172E-006,7.2283064580591234E-007,8.5596489823507489E-008,1.2254535059161463E-008))
    svvN1 = np.array((3.2253376589419873E-003,4.2470170104329800E-004,4.6332886383387752E-005,5.6224841092486311E-006,8.2116973522630579E-007,1.1118288353489161E-007))

    N = np.array((4,5,6,7,8,9))
    NN = [N,N,N,N,N]

    errs = [off,avm,svv001,svv01,svv1]
    
    labels=['No diffusion','AVM','SVV-$c_0=0.01$','SVV-$c_0=0.1$','SVV-$c_0=1$']
    lines = ['--',':','-','-','-']
    marks = ['.','.','.','.','.']
    plotnow('sineN2','$N$','$\|e\|_{L_2}$',NN,errs,labels,linestyles=lines,markers=marks,ptype='semilogy')

    #write slope
    print("slope: no diffusion",linregress(N[:-1],np.log(off[:-1])).slope)
    print("slope: AVM",linregress(N[:-1],np.log(avm[:-1])).slope)
    print("slope: svv=N/2 c0=0.01",linregress(N[:-1],np.log(svvN001[:-1])).slope)
    print("slope: svv=N/2 c0=0.1",linregress(N[:-1],np.log(svvN01[:-1])).slope)
    print("slope: svv=N/2 c0=1",linregress(N[:-1],np.log(svvN1[:-1])).slope)

    print("slope: svv=N/4 c0=0.01",linregress(N[:-1],np.log(svv001[:-1])).slope)
    print("slope: svv=N/4 c0=0.1",linregress(N[:-1],np.log(svv01[:-1])).slope)
    print("slope: svv=N/4 c0=1",linregress(N[:-1],np.log(svv1[:-1])).slope)

    errs = [off,avm,svvN001,svvN01,svvN1]
    plotnow('sineN','$N$','$\|e\|_{L_2}$',NN,errs,labels,linestyles=lines,markers=marks,ptype='semilogy')
    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
