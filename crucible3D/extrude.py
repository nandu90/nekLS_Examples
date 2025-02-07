import gmsh
import numpy as np
from scipy.optimize import fsolve
import os
import time

def gp_equation(r,S,n,a):
    return a * (1-r**n) / (1-r) - S

def get_growth_ratio(S,n,a):
    if(n==1):
        return 1.0
    else:
        r_initial_guess = 1.2
        #solve for r
        r = fsolve(gp_equation, r_initial_guess, args=(S,n,a))
        return r[0]

def gp_sum(a,r,n):
    return a * (r**n - 1) / (r-1)

def get_surface_points(surface_tag):
    all_points = gmsh.model.getEntities(0)

    surface_adj = gmsh.model.getAdjacencies(2, surface_tag)

    curve_tags = surface_adj[1]

    point_tags = set()
    
    for curve_tag in curve_tags:
        curve_adj = gmsh.model.getAdjacencies(1, curve_tag)
        point_tags.update(curve_adj[1])

    points = []
    for pt_tag in point_tags:
        coord = gmsh.model.getValue(0, pt_tag, [])
        points.append(coord)

    return points

def extrude_layers(geo_commands, entities, final_z, num_layers, initial_height, excluded_surfaces={},offset=0):
    growth_factor = get_growth_ratio(final_z,num_layers,initial_height)

    # Compute first layer thickness ensuring geometric progression of gaps
    if num_layers == 1:
        layer_thicknesses = [final_z]  # Single layer, no progression
    else:
        layer_thicknesses = [gp_sum(initial_height,growth_factor,i) for i in range(1,num_layers+1)]

    layer_thicknesses = [i + offset for i in layer_thicknesses]
    
    surfaces = [tag for _, tag in entities if tag not in excluded_surfaces]

    new_entities = []
    # Perform extrusion with progression
    for thickness in layer_thicknesses:
        for tag in surfaces:
            extruded = gmsh.model.geo.extrude([(2,tag)], 0, 0, thickness, numElements=[1], recombine=True)
            geo_commands.append(f'Extrude {{0, 0, {thickness}}} {{ Surface{{{tag}}}; Layers{{1}}; Recombine; }}')

    return

def extrude_bump(geo_commands, entities, final_z, num_layers, initial_height, excluded_surfaces={}):
    growth_factor = get_growth_ratio(final_z/2.0, num_layers, initial_height)

    # Compute first layer thickness ensuring geometric progression of gaps
    if num_layers == 1:
        layer_thicknesses = [final_z/2.0]  # Single layer, no progression
    else:
        layer_thicknesses = [gp_sum(initial_height,growth_factor,i) for i in range(1,num_layers+1)]

    layers = layer_thicknesses[::-1]

    #Add the Bump layers
    for i in range(1,num_layers):
        layer_thicknesses.append(final_z - layers[i])

    layer_thicknesses.append(final_z)

    surfaces = [tag for _, tag in entities if tag not in excluded_surfaces]

    new_entities = []
    
    # Perform extrusion with progression
    for thickness in layer_thicknesses:
        for tag in surfaces:
            extruded = gmsh.model.geo.extrude([(2,tag)], 0, 0, thickness, numElements=[1], recombine=True)
            geo_commands.append(f'Extrude {{0, 0, {thickness}}} {{ Surface{{{tag}}}; Layers{{1}}; Recombine; }}')
    
    return

def assign_boundary_z(geo_commands, zloc, name, rlim=[]):
    # Extract the surface closest to final_z
    tolerance = 1e-6  # Small tolerance to handle floating-point precision
    matching_surfaces = []
    for entity in gmsh.model.getEntities(2):  # Get all 2D surfaces
        _, tag = entity
        x_min, y_min, z_min, x_max, y_max, z_max = gmsh.model.getBoundingBox(2, tag)

        # Check if the surface is at final_z (considering numerical precision)
        if (abs(z_max - zloc) < tolerance and abs(z_max - z_min) < tolerance):
            ifonsurface = True
            if(rlim != []):
                points = get_surface_points(tag)
                for p in points:
                    x = p[0]
                    y = p[1]
                    z = p[2]
                    rad = np.sqrt(x**2 + y**2)
                    if(rad + tolerance < rlim[0] or rad - tolerance > rlim[1]):
                        ifonsurface = False
                        break
            if(ifonsurface):
                matching_surfaces.append(tag)

        
            

    # Print the identified surfaces
    print(f"Surfaces at z={zloc}: {matching_surfaces}")

    # Assign boundary conditions using Physical Groups
    if matching_surfaces:
        top_surface_physical_group = gmsh.model.addPhysicalGroup(2, matching_surfaces)
        gmsh.model.setPhysicalName(2, top_surface_physical_group, name)
        
    geo_commands.append(f'Physical Surface("{name}") = {{{", ".join(map(str, matching_surfaces))}}};\n')

    return

def assign_boundary_circle_xy(geo_commands, rloc, name, zlim=[]):
    # Extract the surface closest to final_z
    tolerance = 1e-6  # Small tolerance to handle floating-point precision
    matching_surfaces = []
    for entity in gmsh.model.getEntities(2):  # Get all 2D surfaces
        _, tag = entity
        x_min, y_min, z_min, x_max, y_max, z_max = gmsh.model.getBoundingBox(2, tag)

        points = get_surface_points(tag)

        ifonsurface = True
        
        for p in points:
            x = p[0]
            y = p[1]
            z = p[2]
            approx_radius = np.sqrt(x**2+y**2)
            if(abs(approx_radius - rloc) > tolerance):
                ifonsurface = False
                break
            if(zlim != []):
                #print(z,zlim)
                zmin = zlim[0]
                zmax = zlim[1]
                if(z_min + tolerance < zmin or z_max - tolerance > zmax):
                    ifonsurface = False
                    break

        if(ifonsurface):
            matching_surfaces.append(tag)

    # Print the identified surfaces
    print(f"Surfaces at r={rloc}: {matching_surfaces}")

    # Assign boundary conditions using Physical Groups
    if matching_surfaces:
        top_surface_physical_group = gmsh.model.addPhysicalGroup(2, matching_surfaces)
        gmsh.model.setPhysicalName(2, top_surface_physical_group, name)
        
    geo_commands.append(f'Physical Surface("{name}") = {{{", ".join(map(str, matching_surfaces))}}};\n')

    return

def main():
    # Initialize Gmsh
    gmsh.initialize()
    gmsh.model.add("ExtrudedMesh")

    # Load existing 2D .geo file (assumed to contain quadrilateral elements)
    geo_file = "mesh.geo"
    gmsh.merge(geo_file)

    # Get all surfaces from the 2D geometry
    dim = 2  # Surface dimension
    entities = gmsh.model.getEntities(dim)

    # List to store extrusion commands for the .geo file
    geo_commands = []

    # Add the original geometry to the new .geo file
    geo_commands.append(f'Merge \"{geo_file}\";')

    #Injector surfaces
    inj_surf = {1, 2, 3, 4, 5}
    
    # Extrude in -Z
    final_z = -10.0      # Depth of crucible
    num_layers = 2      # Total number of layers
    initial_height = -1.0
    extrude_layers(geo_commands, entities, final_z, num_layers, initial_height)

    # Bump extrude in +Z
    final_z = 20.0       # Location of interface
    num_layers = 2      # Total number of layers in half bump
    initial_height = 1.0
    extrude_bump(geo_commands, entities, final_z, num_layers, initial_height,excluded_surfaces=inj_surf)

    # Extrude in +Z
    final_z = 10.0      # Delta Z from interface to outlet
    num_layers = 2      # Total number of layers
    initial_height = 1.0
    off = 20.0          # Location of interface
    extrude_layers(geo_commands, entities, final_z, num_layers, initial_height,excluded_surfaces=inj_surf,offset=off)
    
    # Synchronize the model after modifications
    gmsh.model.geo.synchronize()
    
    # Assign boundary
    assign_boundary_z(geo_commands, -10.0, "bottomWall")

    # Assign boundary
    assign_boundary_z(geo_commands, 30.0, "outlet")

    # Assign boundary
    assign_boundary_z(geo_commands, 0.0, "inlet",rlim=[0.0,1.5875])

    # Assign boundary
    assign_boundary_circle_xy(geo_commands, 24.5,"outerWall")

    # Assign boundary
    assign_boundary_circle_xy(geo_commands, 1.5875,"innerWall",zlim=[0,40])
    
    # Write to a new .geo file
    geo_output_file = "extruded_mesh.geo"
    with open(geo_output_file, "w") as f:
        f.write("\n".join(geo_commands))

    # Finalize Gmsh
    gmsh.finalize()

    print(f"Extruded .geo file saved as '{geo_output_file}' ensuring final point is at {final_z}")
    return

if __name__=="__main__":
    starttime = time.time()
    main()
    print('--- Code ran in %s seconds ---'%(time.time()-starttime))


