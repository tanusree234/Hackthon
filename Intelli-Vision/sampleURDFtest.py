from urdfpy import URDF

robot = URDF.load('tests/data/ur5/ur5.urdf')
robot.save('/tmp/ur5/ur5.urdf')

for link in robot.links:
    print(link.name)
