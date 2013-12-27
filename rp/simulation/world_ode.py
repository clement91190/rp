from rp.datastructure.metastructure import MetaStructure
from direct.showbase.ShowBase import ShowBase
from panda3d.ode import OdeWorld
from panda3d.ode import OdeSimpleSpace, OdeJointGroup, OdePlaneGeom 
from panda3d.core import Vec3, TransformState
from panda3d.core import BitMask32, Vec4


class Physics():
    def __init__(self):
        #init the world
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        #init the friction 
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)
        
        #init the collision space
        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)
      
        #cm = CardMaker("ground")
        #cm.setFrame(-20, 20, -20, 20)
        #ground = render.attachNewNode(cm.generate())
        #ground.setPos(0, 0, 0); ground.lookAt(0, 0, -1)
        # Ground definition
        self.groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))
        self.groundGeom.setCollideBits(BitMask32(0x00000001))
        self.groundGeom.setCategoryBits(BitMask32(0x00000002))

        self.deltaTimeAccumulator = 0.0 
        self.stepSize = 1.0 / 90.0

    # The task for our simulation
    def simulationTask(self, creatures, dt=0):
        # Add the deltaTime for the task to the accumulator
        for multi_box in creatures:
            #c.update_angles(dt)
            multi_box.draw()
            #model.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
        if dt == 0:
            self.deltaTimeAccumulator += globalClock.getDt()
        else:
            self.deltaTimeAccumulator = dt
        while self.deltaTimeAccumulator > self.stepSize:
            # Remove a stepSize from the accumulator until
            # the accumulated time is less than the stepsize
            self.deltaTimeAccumulator -= self.stepSize
            # Step the simulation
            self.space.autoCollide()  # Setup the contact joints
            self.world.quickStep(self.stepSize)
            # set the new positions
            self.contactgroup.empty() # Clear the contact joints
    
    def run_physics(self, t, creatures):
        """ run physics for t steps """
        for i in range(t):
            self.simulationTask(creatures, 0.1)


class MyApp(ShowBase):
    def __init__(self):
        """initialiation with a physical world """
        ShowBase.__init__(self)
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, -1)

        # World
        self.physics = Physics()
        #np = render.attachNewNode(self.world.ground_node)
        #np.setPos(0, 0, -2)
 
        #camera
        base.cam.setPos(10, -30, 20)
        base.cam.lookAt(0, 0, 5)

        self.taskMgr.add(self.update, 'update')
        #taskMgr.doMethodLater(0.5, simulationTask, "Physics Simulation")  
        #creatures
        self.creatures=[]
        self.factory = MultiBoxFactory(self.physics, self.render)
        self.factory.create()
        self.factory.add_to_multi(0.9, TransformState.makePos(Vec3(3, 0, -1)))
        self.factory.add_to_multi()
        self.factory.multiboxes[0].finish()
        self.creatures = self.factory.multiboxes
      
    def update(self, task):
        self.physics.simulationTask(self.creatures)
        return task.cont

    def run(self, t, visual=False):
        if visual:
            self.display_simu(t)
        else:
            self.physics.run_physics(t, self.creatures)
   
    def display_simu(self, t):
        """ display the 3d rendering of the seen during t steps"""
        #TODO CHANGE THIS with a meaning in time
        for i in range(t):
            taskMgr.step()

    def add_creature(self):
        """function that add the creature described in a file (name)
        and add it in panda world"""
        m = MetaStructure()
        #m.add_vertebra()
        m.add_block()
        m.follow_edge()
        m.next_edge()
        m.add_joint()
        #m.next_edge()
       # m.add_joint()
       # m.next_edge()
       # m.add_joint()
       # m.next_edge()
       # m.add_joint()
        
#m.follow_edge()

        self.creatures.append(Creature(m, self))
        #return Creature(m).get_variables()

    def add_snake(self, size):
        """function that add the creature described in a file (name)
        and add it in panda world"""
        m = MetaStructure()
        
        for i in range(size):
            m.add_block()
            m.follow_edge()
            m.add_joint()
            m.follow_edge()

        self.creatures.append(Creature(m, self))
        #return Creature(m).get_variables()


def main():
    app = MyApp()
    #factory = BoxFactory(app.physics, render)
    #factory.add(0.5) 
    app.run(500, True)
    pass

if __name__ == "__main__":
    main()
