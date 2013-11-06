import sys
import math
from pandac.PandaModules import GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, NodePath, GeomPoints


class CubeMaker:
    def __init__(self, size = 0.5):
        # self.smooth = True/False
        # self.uv = True/False or Spherical/Box/...
        # self.color = Method1/Method2/...
        # self.subdivide = 0/1/2/...
        self.size = size

    def generate(self):
        format = GeomVertexFormat.getV3()
        data = GeomVertexData("Data", format, Geom.UHStatic)
        vertices = GeomVertexWriter(data, "vertex")

        size = self.size
        vertices.addData3f(-size, -size, -size)
        vertices.addData3f(+size, -size, -size)
        vertices.addData3f(-size, +size, -size)
        vertices.addData3f(+size, +size, -size)
        vertices.addData3f(-size, -size, +size)
        vertices.addData3f(+size, -size, +size)
        vertices.addData3f(-size, +size, +size)
        vertices.addData3f(+size, +size, +size)

        triangles = GeomTriangles(Geom.UHStatic)

        def addQuad(v0, v1, v2, v3):
            triangles.addVertices(v0, v1, v2)
            triangles.addVertices(v0, v2, v3)
            triangles.closePrimitive()

        addQuad(4, 5, 7, 6) # Z+
        addQuad(0, 2, 3, 1) # Z-
        addQuad(3, 7, 5, 1) # X+
        addQuad(4, 6, 2, 0) # X-
        addQuad(2, 6, 7, 3) # Y+
        addQuad(0, 1, 5, 4) # Y+

        geom = Geom(data)
        geom.addPrimitive(triangles)

        node = GeomNode("CubeMaker")
        node.addGeom(geom)

        return NodePath(node)

def main():
    import direct.directbase.DirectStart
    base.setBackgroundColor(0.0, 0.0, 0.0)
    base.disableMouse()

    camera.setPos(1.0, 1.0, 20.0)
    camera.setHpr(5.0, -87.0, 5.0)

    cube = CubeMaker()
    cube.setColor(1.0, 1.0, 1.0)
    cube.reparentTo(render)

    base.accept("escape", sys.exit)
    base.accept("a", render.analyze)
    base.accept("o", base.oobe)

    run()

if __name__== '__main__': 
    main()   
