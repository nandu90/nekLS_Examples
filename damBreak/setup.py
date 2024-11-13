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
import sympy as sym


def main():
    L = 0.05715
    g = 9.81
    rhol = 1000.0
    rhog = 1.2
    mul = 1e-3
    mug = 1.8e-6
    gamma = 0.06
    nul = mul/rhol
    nug = mug/rhog

    print("Density ratio = ",rhol/rhog)
    print("Dynamic Viscosity ratio = ",mul/mug)
    print("Kinematic Viscosity of water =",nul)
    print("Kinematic Viscosity of air =",nug)
    print("Kinematic Viscosity ratio = ",nul/nug)
    

    U = math.sqrt(g*L)
    print("Characteristic Velocity = ",U)

    Re = rhol*U*L/mul
    print("Reynolds Number, based on water =",Re)

    print("Reg based on mug/mul/Re = ", 1.0/(mug/mul/Re))
    print("Reg based on nug/nul/Re = ", 1.0/(nug/nul/Re))

    Re = rhog*U*L/mug
    print("Reynolds Number, based on air =",Re)

    Fr = U**2/g/L
    print("Froude Number =",Fr)

    We = rhol*U**2*L/gamma
    print("Weber Number =",We)
    

    #Get the derivative of Spalding Wall Function 
    #https://www.sciencedirect.com/science/article/pii/S030193221100067X
    
    kappa = sym.Symbol('kappa')
    E = sym.Symbol('E')
    uplus = sym.Symbol('uplus')
    yplus = uplus + (1/E)*(sym.exp(kappa * uplus) - 1 - kappa*uplus - (kappa*uplus)**2/math.factorial(2) - (kappa*uplus)**3/math.factorial(3))
    sym.pprint(yplus)

    dydu = sym.diff(yplus, uplus)
    sym.pprint(dydu)
    

    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
