import gmsh
import math

gmsh.initialize()

gmsh.open("crucible.msh")

inletL = 3.175
inletL2 = inletL/2.0
theta = math.pi/4.0

node_tags, node_coords, _ = gmsh.model.mesh.getNodes()

for i, tag in enumerate(node_tags):
    x = node_coords[3 * i]
    y = node_coords[3 * i + 1]
    z = node_coords[3 * i + 2]
    
    rinfluence = math.sqrt(x**2 + z**2)
    rinfluence = rinfluence/inletL2
    fac = 0.5 - 0.5 * math.tanh(math.pi/6.0 * (rinfluence-1.5))
    
    xx = x/inletL2
    arm = xx/math.cos(theta)
    zz = arm * math.sin(theta) * fac * inletL2
    znew = z + zz
        
    # Replace all node coordinates
    gmsh.model.mesh.setNode(tag, [x,y,znew], [])

gmsh.option.setNumber("Mesh.MshFileVersion", 2.0)  # Set Version 2
gmsh.option.setNumber("Mesh.Binary", 1)  # Enable binary format

gmsh.write("modified.msh")
gmsh.finalize()
