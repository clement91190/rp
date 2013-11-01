from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from multiprocessing import Process

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, -1)


app = MyApp()
base.cam.setPos(10, -30, 20)
base.cam.lookAt(0, 0, 5)
 
# World
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))
 
# Plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, -2)
world.attachRigidBody(node)


def define_model():
    model = loader.loadModel('models/box.egg')
    model.setPos(-0.5, -0.5, -0.5)
    model.flattenLight()
    return model


def define_shape():
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
    return shape


model = define_model()
shape = define_shape()


def add_box(i):
    # Boxes
    node = BulletRigidBodyNode('Box')
    node.setMass(1.0)
    node.addShape(shape)
    np = render.attachNewNode(node)
    np.setPos(0, i*0.2 % 0.5, 2+i*1.1 )
    world.attachRigidBody(node)
    model.copyTo(np)


for i in range(4):
    add_box(i)


def get_render():
    return render


# Update
def update(task):
    dt = globalClock.getDt()
    world.doPhysics(dt)
    return task.cont
 
taskMgr.add(update, 'update')


def main():
    while(True):
        taskMgr.step()

#p = Process(target=main)

#p.start()

print "coucou ca va ?"
#p.join()
#app.run()
