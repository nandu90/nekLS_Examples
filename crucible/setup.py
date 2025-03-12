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
    flowrate = 10.0/60.0 * 1e-6
    areainlet = math.pi*(L/2.0)**2.0
    U = flowrate/areainlet
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

    
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
