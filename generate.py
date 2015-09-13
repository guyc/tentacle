#!/usr/bin/env python

# outer perimeter  points must be added clockwise.
# interior hole points must be added counter-clockwise.
# Mesh triangles will be returned counter-clockwise and must be reversed.

import math
from openscad import *
from quake import *

print "hello world\n"

ArcAngle = 60.0/8.0 # degrees
ArcRadius = 895
ArcPoints = 16

ArmWidth = 40
ArmDepth = 30
BulgeRadius  = 30
BulgePoints  = 16

TunnelX = 0
TunnelY = 22
TunnelRadius = 4
TunnelPoints = 16

TrackWidth = 14.5
TrackDepth = 1.5
TrackOverhang = 1.0
TrackOverhangDepth = 1.0

DiffuserDepth = 1.0
DiffuserWidth = 32.0
DiffuserOverhang = 5.0
DiffuserOverhangDepth = 1.0
DiffuserBackDepth = 11.2

def arc2d(angle, scale):
  # clockwise outer boundary
  ax = ArmWidth/2.0
  ay = 0.0
  bx = 0.0
  by = ArmDepth
  dab = math.sqrt(ax*ax+by*by)
  angleab = math.atan(by/ax)
  angleabc = math.acos(dab/2/BulgeRadius)
  angleac = angleabc - angleab
  cx = ax - BulgeRadius * math.cos(angleac)
  cy = ay - BulgeRadius * math.sin(angleac)
  sweep = math.pi - 2 * angleabc
  # now place points along cirlce centered at cx,cy across arc from ax,ay to bx,by
  [angleabc*180/math.pi,sweep*180/math.pi]
  arc = []
  a0 = angleac

  for i in xrange(0,BulgePoints,1):
    a = a0 + sweep * i / BulgePoints
    arc.append([cx+BulgeRadius * math.cos(a),
                cy+BulgeRadius * math.sin(a)])

  for i in xrange(BulgePoints,-1,-1):
    a = a0 + sweep * i / BulgePoints
    arc.append([-cx-BulgeRadius * math.cos(a),
                cy+BulgeRadius * math.sin(a)])

  arc.reverse
  return arc

def face2d(angle, scale):
  face = []

  y = 0
  x = -DiffuserWidth/2+DiffuserOverhang/2
  face.append([x,y])
  y = DiffuserOverhangDepth
  face.append([x,y])
  x = -DiffuserWidth/2
  face.append([x,y])
  y = DiffuserOverhangDepth+DiffuserDepth
  face.append([x,y])
  x = -DiffuserWidth/2+DiffuserOverhang/2
  face.append([x,y])
  y = DiffuserOverhangDepth+DiffuserDepth+DiffuserBackDepth
  face.append([x,y])
  x = -TrackWidth/2+TrackOverhang
  face.append([x,y])
  y = DiffuserOverhangDepth+DiffuserDepth+DiffuserBackDepth+TrackOverhangDepth
  face.append([x,y])

  x = -TrackWidth/2
  face.append([x,y])
  y = DiffuserOverhangDepth+DiffuserDepth+DiffuserBackDepth+TrackOverhangDepth+TrackDepth
  face.append([x,y])

  x = TrackWidth/2
  face.append([x,y])
  y = DiffuserOverhangDepth+DiffuserDepth+DiffuserBackDepth+TrackOverhangDepth
  face.append([x,y])


  x = TrackWidth/2-TrackOverhang
  face.append([x,y])
  y = DiffuserOverhangDepth+DiffuserDepth+DiffuserBackDepth
  face.append([x,y])
  x = DiffuserWidth/2-DiffuserOverhang/2
  face.append([x,y])
  y = DiffuserOverhangDepth+DiffuserDepth
  face.append([x,y])
  x = DiffuserWidth/2
  face.append([x,y])
  y = DiffuserOverhangDepth
  face.append([x,y])
  x = DiffuserWidth/2-DiffuserOverhang/2
  face.append([x,y])
  y = 0
  face.append([x,y])

  face.reverse
  return face

# counter clockwise, because it's a hole
def tunnel2d(angle, scale):
  tunnel = []

  for i in xrange(0,TunnelPoints):
    a = math.pi * 2.0 / TunnelPoints * i
    tunnel.append([+TunnelX + TunnelRadius * math.cos(a),
                   +TunnelY + TunnelRadius * math.sin(a)])

  return tunnel


# angle in radians please
def projectPoint(point2d, angle):
  x = point2d[0]
  y = point2d[1]

  x1 = x
  y1 = (ArcRadius + y) * math.cos(angle) - ArcRadius
  z1 = (ArcRadius + y) * math.sin(angle)
  return [x1,y1,z1]


def polyhedronFromMesh(mesh):
    polyhedron = OpenscadPolyhedron()
    polyhedron.convexity = 10
    m = len(mesh.vertices)

    for step in range(0,ArcPoints+1):
        a = math.pi / 180.0 * ArcAngle * step / ArcPoints
        for vertex in mesh.vertices:
            polyhedron.points.append(projectPoint(vertex,a))

    # trangles for edge faces
    for step in range(0,ArcPoints):
        offset0 = m * step
        offset1 = m * (step+1)
        for segment in mesh.segments:
            v0 = segment[0] + offset0
            v1 = segment[1] + offset0
            v2 = segment[0] + offset1
            v3 = segment[1] + offset1

            # order of segments matches order of triangles which is anticlockwise so we reverse it.
            polyhedron.triangles.append([v3,v1,v0])
            polyhedron.triangles.append([v0,v2,v3])

    offset = ArcPoints * m
    # front and back face triangles
    for triangle in mesh.triangles:
        # reverse the direction
        polyhedron.triangles.append([triangle[0],triangle[1],triangle[2]])
        polyhedron.triangles.append([triangle[2]+offset, triangle[1]+offset, triangle[0]+offset])
    
    return polyhedron


arc = face2d(0,0) + arc2d(0,0)
tunnel = tunnel2d(0,0)

qp = QuakePolygon()

for curve in [arc, tunnel]:
  v0 = len(qp.vertices)
  print curve
  print "v0=%d\n" % v0
  n = len(curve)
  qp.vertices.extend(curve)
  for i in range(0,n):
      qp.segments.append([v0+i,v0+((i+1)%n)])

if len(tunnel):
    qp.holes.append([TunnelX, TunnelY])

tri = QuakeTriangle()
mesh = tri.polyToMesh(qp, "x")
polyhedron = polyhedronFromMesh(mesh)
scadFile = open("generated.scad", "w")
fields = ['ArcAngle',
          'ArcRadius']
for field in fields:
    scadFile.write("%s = %s;\n" % (field,globals()[field]))
scadFile.write("\nmodule object() {\n");
polyhedron.write(scadFile)
scadFile.write("\n}\n");
#scadFile.write("object();\n");
scadFile.close();
