from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from rp.datastructure import metastructure

"""file of definition of the physical engine and
3D display of the world """


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, -1)

        # World
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

app = MyApp()
base.cam.setPos(10, -30, 20)
base.cam.lookAt(0, 0, 5)
 

# Plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, -2)
app.world.attachRigidBody(node)


# Boxes
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
    node = BulletRigidBodyNode('Box')
    node.setMass(1.0)
    node.addShape(shape)
    np = render.attachNewNode(node)
    np.setPos(0, i * 0.2 % 0.5, 2 + i * 1.1 )
    app.world.attachRigidBody(node)
    model.copyTo(np)


for i in range(200):
    add_box(i)

def physical_step():
    """perform one step on the physical world
    and read the command..."""
    dt = globalClock.getDt()
    app.world.doPhysics(dt)
    #TODO add the command part 


# Update
def update(task):
    physical_step()
    return task.cont


taskMgr.add(update, 'update')


def display_simu(t):
    """ display the 3d rendering of the seen during t steps"""
    for i in range(t):
        taskMgr.step()


def run_physics(t):
    """ run physics for t steps """
    for i in range(t):
        physical_step()


class Creature():
    def __init__(self, metastructure):
        """constructor of the class
        use the metastructure"""
        self.metastucture = metastructure

    def build(self, creature):
        """ creature is a metastructure ( graph describing the struct)
            this function build the structure and add it in panda
            world
        """
#TODO  implement this function

    def get_variables(self):
        """ variables is probably going to be a list of list
        [[coefficient] for all angles]"""
        return self.variables

    def update_angles():
        """calculate the new value of the angles based on the
        variables"""


def add_creature(name):
    """function that add the creature described in a file (name)
    and add it in panda world"""
    mstructure = metastructure.load_structure(name)
    Creature(mstructure).get_variables()


def run(t, visual=False):
    if visual:
        display_simu(t)
    else:
        run_physics(t)



