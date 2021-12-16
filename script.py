from math import radians
from compas.geometry import Frame, Point, Vector, Plane, Circle
from compas.geometry import Box, Cylinder
from compas.geometry import Translation, Rotation

from compas_gmsh.models import CSGModel

from compas_view2.app import App

# =============================================================================
# Components - Rod
# =============================================================================

box = Box(Frame.worldXY(), 0.6, 0.02, 0.05)
cyl1 = Cylinder(Circle(Plane(Point(0.3, 0, 0), Vector(0, 1, 0)), 0.025), 0.02)
cyl2 = Cylinder(Circle(Plane(Point(-0.3, 0, 0), Vector(0, 1, 0)), 0.025), 0.02)
hole1 = Cylinder(Circle(Plane(Point(0.3, 0, 0), Vector(0, 1, 0)), 0.01), 0.02)
hole2 = Cylinder(Circle(Plane(Point(-0.3, 0, 0), Vector(0, 1, 0)), 0.01), 0.02)

tree = {
    'difference': [
        {'difference': [{'union': [box, cyl1, cyl2]}, hole1]},
        hole2
    ]
}

model = CSGModel(tree, name='rod')

model.options.mesh.meshsize_from_curvature = True
model.options.mesh.min_nodes_circle = 16

model.compute_tree()
model.generate_mesh()
model.optimize_mesh()

rod = model.mesh_to_compas()

del model

# =============================================================================
# Components - Anchor
# =============================================================================

box = Box(Frame.worldXY(), 0.08, 0.01, 0.04)
box.transform(Translation.from_vector([0, 0, -0.02]))

cylinder = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 1, 0)), 0.04), 0.01)
hole = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 1, 0)), 0.01), 0.01)

tree = {'difference': [{'union': [box, cylinder]}, hole]}

model = CSGModel(tree, name='plate')

model.options.mesh.meshsize_from_curvature = True
model.options.mesh.min_nodes_circle = 32

model.compute_tree()
model.generate_mesh()
model.optimize_mesh()

plate = model.mesh_to_compas()

del model

# =============================================================================
# Components - Connectors
# =============================================================================

connector = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 1, 0)), 0.01), 0.07)

# =============================================================================
# Assembly
# =============================================================================

T = Translation.from_vector([0.3, 0, 0])
rod.transform(T)

R = Rotation.from_axis_and_angle([0, -1, 0], radians(60), point=[0, 0, 0])
rod1 = rod.transformed(R)

R = Rotation.from_axis_and_angle([0, +1, 0], radians(60), point=[0.6, 0, 0])
rod2 = rod.transformed(R)
rod2.transform(Translation.from_vector([0, 0.02, 0]))
rod3 = rod.transformed(R)
rod3.transform(Translation.from_vector([0, -0.02, 0]))

plate1 = plate.transformed(Translation.from_vector([0, 0.015, 0]))
plate2 = plate.transformed(Translation.from_vector([0, -0.015, 0]))

plate3 = plate.transformed(Translation.from_vector([0.6, 0, 0]))

con1 = connector
con2 = con1.transformed(Translation.from_vector([0.6, 0, 0]))
con3 = con2.transformed(Rotation.from_axis_and_angle([0, -1, 0], radians(60), point=[0, 0, 0]))

# =============================================================================
# Viz
# =============================================================================

viewer = App(width=1600, height=900)

# set the camera to a specific view
# this should be integrated in the viewer API
# PRs people!
viewer.view.camera.rz = 30
viewer.view.camera.rx = -75
viewer.view.camera.tx = -0.25
viewer.view.camera.ty = -0.25
viewer.view.camera.distance = 1

viewer.add(rod1)
viewer.add(rod2, facecolor=(0.4, 0.4, 0.4), linecolor=(0.6, 0.6, 0.6))
viewer.add(rod3, facecolor=(0.4, 0.4, 0.4), linecolor=(0.6, 0.6, 0.6))

viewer.add(plate1, facecolor=(0, 0, 0), linecolor=(0.2, 0.2, 0.2))
viewer.add(plate2, facecolor=(0, 0, 0), linecolor=(0.2, 0.2, 0.2))
viewer.add(plate3, facecolor=(0, 0, 0), linecolor=(0.2, 0.2, 0.2))

viewer.add(con1, facecolor=(1.0, 1.0, 1.0), linecolor=(0.8, 0.8, 0.8))
viewer.add(con2, facecolor=(1.0, 1.0, 1.0), linecolor=(0.8, 0.8, 0.8))
viewer.add(con3, facecolor=(1.0, 1.0, 1.0), linecolor=(0.8, 0.8, 0.8))

viewer.show()
