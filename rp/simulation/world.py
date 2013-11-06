from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, TransformState
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from rp.datastructure.metastructure import MetaStructure
from rp.utils.primitives.cube import CubeMaker

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
            self.world.run_physics(t)


    def display_simu(self, t):
        """ display the 3d rendering of the seen during t steps"""
        for i in range(t):
            taskMgr.step()
    
    def add_creature(self):
        """function that add the creature described in a file (name)
        and add it in panda world"""
        m = MetaStructure()
        self.creatures.append(Creature(m, self))
        #return Creature(m).get_variables()



class Creature():
    def __init__(self, metastructure, app):
        """constructor of the class
        use the metastructure"""
        self.metastructure = metastructure
        self.world = app.world
        self.build()
        self.pieces = []

        
    def build_head(self, node=BulletRigidBodyNode('bloc'), np=None):
        """ build the head of the creature """
        node.setMass( node.getMass() + 1.0)
        if np is None:
            np = render.attachNewNode(node)
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        shape2 = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        node.addShape(shape)
        node.addShape(shape2, TransformState.makePos(Vec3(1.0, 0.0, 0.0)))
        np.setPos(0, 0, 4)
        
        self.world.attachRigidBody(node)  # this must be at done at the end...
        model = CubeMaker(0.5).generate()
        #loader.loadModel('models/cube.egg')
        model.setPos(0,0,0)
        model.flattenLight()
        model.setColor(1.0, 1.0, 1.0)
        model.copyTo(np)
        model = CubeMaker(0.5).generate()
        #loader.loadModel('models/cube.egg')
        model.setPos(1.0,0.0,0.0)
        model.flattenLight()
        model.setColor(0, 1.0, 1.0)
        model.copyTo(np)
        return (node, np)



    def build_bloc(self):
        pass

#TODO  implement this function with different cases 
    def build_joint(self, build_stat):
        pass

#TODO  implement this function with different cases
    def build_vertebra(self, build_stat):
        pass
#TODO  implement this function

    def build(self):
        """ this function build the structure and add it in panda
            world
        """

        #create a dictionary to chech the nodes already added and linked
        self.building_status = dict(zip(
            self.metastructure.all_nodes,
            [[False, False, False] for i in self.metastructure.all_nodes]))
        # we build this to check for joints if the 2 parts of the 
        #joints have been built and the link also
        self.recursive_build(self.metastructure.head)

    def recursive_build(self, node):
        """ recursive function to build the
        structure """
        self.build_node(node, self.building_status[node])
        print " building node :{}".format(node)
        print node.edges
     #TODO complete here in case of a joint/vertebra
        #adding
        for face, edge in enumerate(node.edges[1:]):
            if edge.type() != 'empty':
                if edge.gen_type() == 'piece':
                    if not all(self.building_status[edge][0]):
                    #then we have to add this node (because it
                    #is not entirely finished
                        self.recursive_build_piece(edge)

    def build_node(self, node, build_stat):
        """ depending on the type of node call different
        functions """
        if node.gen_type == 'piece':
            self.building_status[node] = [True, True, True]
        return {
            'head': self.build_head(),
            'block': self.build_bloc(),
            'vertebra': self.build_vertebra(build_stat),
            'joint': self.build_joint(build_stat)}[node.type()]


    def link(self, nodeA, nodeB, face):
        """ build a solid link between 2 nodes (or elastic) """
#TODO  implement this function

    def get_variables(self):
        """ variables is probably going to be a list of list
        [[coefficient] for all angles]"""
        return self.variables

    def update_angles():
        """calculate the new value of the angles based on the
        variables"""



