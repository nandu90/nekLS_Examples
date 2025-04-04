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
    off = np.array((2.9407653498870519E-004,2.7446071174175465E-005,9.7980711625767897E-007,4.8428231633871924E-008,3.6616352823200690E-009,2.0930341285921334E-009))
    avm = np.array((2.0917531408130869E-003,9.8193860029867851E-004,1.1064561251340109E-004,4.4376863120931654E-006,3.3604294240006040E-007,8.9927558159165132E-009))
    svv001 = np.array((3.5841099464030521E-004,7.9266172103079749E-005,1.4442370379943432E-005,3.2332286061702439E-006,6.8273918317143596E-007,1.5394116808091191E-007))
    svv01 = np.array((2.6844443026280665E-003,7.0517521145619147E-004,1.4764294701577113E-004,3.2398716854415289E-005,6.9767745378030882E-006,1.5161241650573107E-006))
    svv1 = np.array((2.2240900396330473E-002,6.4241671600184002E-003,1.6194123203355799E-003,3.7265757955174165E-004,7.7291505939236580E-005,1.5795367165733171E-005))

    svvN001 = np.array((2.6972242395592740E-004,2.5314613883253688E-005,9.5795911232633860E-007,8.8083085718817080E-008,9.7121132850755004E-009,2.4466063546595168E-009))
    svvN01 = np.array((3.4467326606520230E-004,5.4688336694114147E-005,3.7333925022202275E-006,7.2283064795220605E-007,8.5596490985984267E-008,1.2254537709290267E-008))
    svvN1 = np.array((3.2253376589465293E-003,4.2470170105066119E-004,4.6332886387621650E-005,5.6224841098244110E-006,8.2116973389608131E-007,1.1118288437471049E-007))

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
