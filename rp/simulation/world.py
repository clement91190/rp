from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from rp.datastructure.metastructure import MetaStructure

"""file of definition of the physical engine and
3D display of the world """


class MyWorld(BulletWorld):
    def __init__(self):
        BulletWorld.__init__(self)
        
        #adding gravity
        self.setGravity(Vec3(0, 0, -9.81))
        
        # Ground definition
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        self.ground_node = BulletRigidBodyNode('Ground')
        self.ground_node.addShape(shape)
        self.attachRigidBody(self.ground_node)

    def physical_step(self):
        """perform one step on the physical world
        and read the command..."""
        dt = globalClock.getDt()
        self.doPhysics(dt)
        #TODO add the command part 

    def run_physics(self, t):
        """ run physics for t steps """
        for i in range(t):
            self.physical_step()



class MyApp(ShowBase):
    def __init__(self, world):
        """initialiation with a physical world """
        ShowBase.__init__(self)
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, -1)

        # World
        self.world = world
        np = render.attachNewNode(self.world.ground_node)
        np.setPos(0, 0, -2)
 
        #camera
        base.cam.setPos(10, -30, 20)
        base.cam.lookAt(0, 0, 5)

        taskMgr.add(self.update, 'update')
        
        #creatures
        self.creatures=[]

       # Update
    def update(self, task):
        self.world.physical_step()
        return task.cont


    def run(self, t, visual=False):
        if visual:
            self.display_simu(t)
        else:
            self.run_physics(t)


    def display_simu(self, t):
        """ display the 3d rendering of the seen during t steps"""
        for i in range(t):
            taskMgr.step()
    
    def add_creature(self):
        """function that add the creature described in a file (name)
        and add it in panda world"""
        m = MetaStructure()
        m.add_joint()
        self.creatures.append(Creature(m, self))
        #return Creature(m).get_variables()



class Creature():
    def __init__(self, metastructure, app):
        """constructor of the class
        use the metastructure"""
        self.metastucture = metastructure
        self.world = app.world
        
    def build_head():
        for i in range(100):
            node = BulletRigidBovdyNode('bloc')
            node.setMass(1.0)
            shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
            node.addShape(shape)
            np = render.attachNewNode(node)
            np.setPos(0, 0, 2 + 1.1 *i)
            self.world.attachRigidBody(node)
            model = loader.loadModel('models/box.egg')
            model.setPos(-0.5, -0.5, -0.5)
            model.flattenLight()
            model.copyTo(np)

    def build_bloc():
        pass

    def build_joint():
        pass

    def build_vertebra():
        pass

    def build(self, creature):
        """ creature is a metastructure ( graph describing the struct)
            this function build the structure and add it in panda
            world
        """

        build_head()
#TODO  implement this function

    def get_variables(self):
        """ variables is probably going to be a list of list
        [[coefficient] for all angles]"""
        return self.variables

    def update_angles():
        """calculate the new value of the angles based on the
        variables"""



