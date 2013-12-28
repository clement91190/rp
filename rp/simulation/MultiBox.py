from panda3d.ode import OdeBoxGeom, OdeBody, OdeMass
from panda3d.core import Vec3, LQuaternionf, TransformState, BitMask32, Quat

from rp.utils.primitives.cube import CubeMaker


class MultiBox():
    def __init__(self, render, physics):
        self.boxes = []
        self.transforms = []
        self.geoms = []
        self.physics = physics
        self.render = render
        self.body = OdeBody(physics.world)
        self.M = OdeMass()
        #self.M.setBox(50, 0.1, 0.1, 0.1)
        #self.body.setMass(self.M)
        self.body.setPosition(0, 0, 10)

    def add(self, size, color, transform):
        self.transforms.append(transform)
        m = OdeMass()
        m.setBox(50, size, size, size)
        m.translate(transform.getPos())
        self.M.add(m)
        box = Box(self.render, size, self.physics, color, self.body, transform)
        self.boxes.append(box.get_np_and_body())
        self.geoms.append(box.get_geom())

    def get_transform(self):
        pos = self.body.getPosition()
        quat = self.body.getQuaternion()
        quat = LQuaternionf(quat)
        scale = Vec3(1, 1, 1)
        return TransformState.makePosQuatScale(pos, quat, scale)

    def draw(self):
        """ draw all the boxes in the correct position/orientation
        transform is a TransformState"""
        transform_body = self.get_transform()
        transform_body = transform_body.getMat()
        for i, (model, body) in enumerate(self.boxes):
            transform = self.transforms[i]
            mat = transform.getMat() * transform_body
            transform = TransformState.makeMat(mat)
            model.setPosQuat(self.render, transform.getPos(), Quat(transform.getQuat()))

    def finish(self):
        offset = self.M.getCenter()
        self.M.translate(-offset)
        for geom in self.geoms:
            off = geom.getOffsetPosition()
            geom.setOffsetPosition(off - offset)
        self.body.setMass(self.M)


class MultiBoxFactory():
    def __init__(self, physics, render):
        self.multiboxes = []
        self.physics = physics
        self.render = render

    def create(self):
        self.multiboxes.append(MultiBox(self.render, self.physics))

    def add_to_multi(self, size=0.5, transform=TransformState.makeIdentity(), color=(0, 1, 1), id_of_multi=-1):
        self.multiboxes[id_of_multi].add(size, color, transform) 


class Box():
    def __init__(self, render, size, physics, color, body, transform):
              # Create a BoxGeom
        self.body = body
        self.boxGeom = OdeBoxGeom(physics.space, size, size, size)
        self.boxGeom.setCollideBits(BitMask32(0x00000002))
        self.boxGeom.setCategoryBits(BitMask32(0x00000001))
        self.boxGeom.setBody(body)
        pos = transform.getPos()
        self.boxGeom.setOffsetPosition(pos)
        self.model = CubeMaker(size).generate()
        self.model.flattenLight()
        self.model.setColor(color[0], color[1], color[2])
        self.render_node = self.model.copyTo(render)
    
    def get_np_and_body(self):
        return (self.render_node, self.body)
    
    def get_geom(self):
        return self.boxGeom


