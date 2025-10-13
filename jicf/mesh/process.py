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
import gmsh
import sys


def main():
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)

    gmsh.open("jicf.geo")

    gmsh.model.geo.synchronize()

    with open("jicf.geo", "r") as f:
        lines = f.readlines()

    # Get all 2D surfaces
    surfaces = gmsh.model.getEntities(dim=2)
    #print("Surfaces found:", surfaces)

    #water inlet
    tol = 1e-6
    inlet_water = []
    inlet_air = []
    outlet = []
    side1 = []
    side2 = []
    top = []
    bottomWall = []
    injectorWall = []
    for (dim, tag) in surfaces:
        xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(dim, tag)
        if abs(zmin + 2.0) < tol and abs(zmax + 2.0) < tol:
            inlet_water.append(tag)
        elif abs(zmin - 10.0) < tol and abs(zmax - 10.0) < tol:
            top.append(tag)
        elif abs(xmin + 3.0) < tol and abs(xmax + 3.0) < tol:
            inlet_air.append(tag)
        elif abs(xmin - 9.0) < tol and abs(xmax - 9.0) < tol:
            outlet.append(tag)
        elif abs(ymin - 3.5) < tol and abs(ymax - 3.5) < tol:
            side1.append(tag)
        elif abs(ymin + 3.5) < tol and abs(ymax + 3.5) < tol:
            side2.append(tag)
        elif abs(zmin) < tol and abs(zmax) < tol:
            xmid = 0.5*(xmin + xmax)
            ymid = 0.5*(ymin + ymax)
            zmid = 0.5*(zmin + zmax)
            r = (xmid**2 + ymid**2)**0.5
            if r > 0.5:
                bottomWall.append(tag)


    inlet_line = f'Physical Surface("inletWater") = {{{", ".join(map(str, inlet_water))}}};\n'
    lines.append(inlet_line)
    inlet_line = f'Physical Surface("inletAir") = {{{", ".join(map(str, inlet_air))}}};\n'
    lines.append(inlet_line)
    inlet_line = f'Physical Surface("outlet") = {{{", ".join(map(str, outlet))}}};\n'
    lines.append(inlet_line)
    inlet_line = f'Physical Surface("side1") = {{{", ".join(map(str, side1))}}};\n'
    lines.append(inlet_line)
    inlet_line = f'Physical Surface("side2") = {{{", ".join(map(str, side2))}}};\n'
    lines.append(inlet_line)
    inlet_line = f'Physical Surface("top") = {{{", ".join(map(str, top))}}};\n'
    lines.append(inlet_line)
    inlet_line = f'Physical Surface("bottomWall") = {{{", ".join(map(str, bottomWall))}}};\n'
    lines.append(inlet_line)
    inlet_line = f'Physical Surface("injectorWall") = {{{", ".join(map(str, injectorWall))}}};\n'
    lines.append(inlet_line)

    with open("jicf_new.geo", "w") as f:
        f.writelines(lines)

    gmsh.finalize()
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))
