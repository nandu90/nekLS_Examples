import gmsh
import math

# Initialize Gmsh
gmsh.initialize()

gmsh.model.add("extruded")  # Add model explicitly
gmsh.merge("extruded.geo")

gmsh.model.geo.synchronize()  # Ensure synchronizationa

#gmsh.option.setNumber("Mesh.Recombine3D", 1)

# Generate 2D or 3D mesh (depends on the geometry)
gmsh.model.mesh.generate(3)  # Change to generate(2) for a surface mesh

# Set mesh order to 2 (higher-order elements)
gmsh.model.mesh.setOrder(2)

# Parameters for node transformation
inletL = 3.175
inletL2 = inletL / 2.0
theta = math.pi / 4.0

# Get all mesh nodes
node_tags, node_coords, _ = gmsh.model.mesh.getNodes()

# Apply transformation to all nodes
for i, tag in enumerate(node_tags):
    x = node_coords[3 * i]
    y = node_coords[3 * i + 1]
    z = node_coords[3 * i + 2]
    
    rinfluence = math.sqrt(x**2 + z**2)
    rinfluence = rinfluence / inletL2
    fac = 0.5 - 0.5 * math.tanh(math.pi / 6.0 * (rinfluence - 1.5))
    
    xx = x / inletL2
    arm = xx / math.cos(theta)
    zz = arm * math.sin(theta) * fac * inletL2
    znew = z + zz
        
    # Replace all node coordinates
    gmsh.model.mesh.setNode(tag, [x, y, znew], [])

# Print element types in the mesh
element_types = gmsh.model.mesh.getElementTypes(3)
print("Element types in the mesh:")
for etype in element_types:
    element_properties = gmsh.model.mesh.getElementProperties(etype)
    if element_properties:
        element_name = element_properties[0]  # Get element name
        element_tags, _ = gmsh.model.mesh.getElementsByType(etype)
        num_elements = len(element_tags) if element_tags is not None else 0
        print(f"Type {etype}: {element_name}, Count: {num_elements}")



# Set mesh format options
gmsh.option.setNumber("Mesh.MshFileVersion", 2.0)  # Set Version 2
gmsh.option.setNumber("Mesh.Binary", 1)  # Enable binary format
gmsh.option.setNumber("Mesh.SaveAll", 0)  # Disable 'Save All Elements'

# Save the modified mesh
gmsh.write("extruded.msh")

# Finalize Gmsh
gmsh.finalize()

