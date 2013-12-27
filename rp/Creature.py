from panda3d.core import Vec3, LMatrix4f,  LQuaternionf, TransformState
from panda3d.ode import OdeWorld, OdeBoxGeom
from panda3d.ode import OdeBody, OdeMass, OdeSimpleSpace, OdeJointGroup, OdePlaneGeom 


from rp.datastructure.metastructure import MetaStructure
from rp.utils.primitives.cube import CubeMaker
from rp.control.BrainControl import BrainControl
from rp.cpg import cpg

"""file of definition of the physical engine and
3D display of the world """


class Creature():
    def __init__(self, metastructure, physics):
        """constructor of the class
        use the metastructure"""
        self.metastructure = metastructure
        self.physics = physics
        self.quat_dict = {
            1: (0, Vec3(1, 0, 0)),
            2: (90, Vec3(0, 1, 0)),
            3: (-90, Vec3(0, 1, 0)),
            4: (90, Vec3(0, 0, 1)),
            5: (-90, Vec3(0, 0, 1))}
        self.dof_motors = {}  
        self.build()
        self.cpg = cpg.CPG(self.metastructure)
        self.cpg.set_desired_frequency()
        self.cpg.set_desired_amplitude()

    def build_head(self, shape, transform):
        """ build the head of the creature """
        print "add head"
        bullet_node, render_node = shape
        #bullet_node.setMass(bullet_node.getMass() + 1.0)
        
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        bullet_node.addShape(shape)
        #TransformState.makePos(Vec3(1.0, 0.0, 0.0)))
        render_node.setPos(0, 0, 4)

        model = CubeMaker(0.5).generate()
        #loader.loadModel('models/cube.egg')
        model.setPos(0, 0, 0)
        model.flattenLight()
        model.setColor(1.0, 1.0, 1.0)
        model.copyTo(render_node)
       
    def build_bloc(self, shape, transform):
        print " add bloc at {}".format(transform)
        bullet_node, render_node = shape
        bullet_node.setMass(bullet_node.getMass() + 1.0)
        bullet_shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        bullet_node.addShape(bullet_shape, transform)

        model = CubeMaker(0.5).generate()
        #loader.loadModel('models/cube.egg')
        model.setTransform(transform)
        model.flattenLight()
        model.setColor(0, 1.0, 1.0)
        model.copyTo(render_node)


#TODO  implement this function with different cases 
    def build_joint(self, shape, transform):
        print " add joint at {}".format(transform)
        bullet_node, render_node = shape
        bullet_node.setMass(bullet_node.getMass() + 1.0)
        bullet_shape = BulletBoxShape(Vec3(0.25, 0.25, 0.25))
        bullet_node.addShape(bullet_shape, transform)

        model = CubeMaker(0.25).generate()
        #loader.loadModel('models/cube.egg')
        model.setTransform(transform)
        model.flattenLight()
        model.setColor(1.0, 0, 1.0)
        model.copyTo(render_node)


#TODO  implement this function with different cases
    def build_vertebra(self, shape, transform):
        print " add vertebra at {}".format(transform)
        bullet_node, render_node = shape
        bullet_node.setMass(bullet_node.getMass() + 1.0)
        bullet_shape = BulletBoxShape(Vec3(0.25, 0.25, 0.25))
        bullet_node.addShape(bullet_shape, transform)

        model = CubeMaker(0.25).generate()
        #loader.loadModel('models/cube.egg')
        model.setTransform(transform)
        model.flattenLight()
        model.setColor(1.0, 1.0, 0)
        model.copyTo(render_node)

    def build_link(self, node):

        (bda, ta), (bdb, tb) = self.link_building_status[node] 
        
        mat = tb.getMat()
        mat = LMatrix4f.translateMat(Vec3(-0.5, 0, 0)) * mat
        mat = LMatrix4f.rotateMat(*self.quat_dict[2]) * mat
        tb = TransformState.makeMat(mat)
       
        mat = ta.getMat()
        mat = LMatrix4f.translateMat(Vec3(0.5, 0, 0)) * mat
        mat = LMatrix4f.rotateMat(*self.quat_dict[2]) * mat
        ta = TransformState.makeMat(mat)
       
        cs = BulletHingeConstraint(bda[0], bdb[0], ta.getPos(), tb.getPos(),ta.getQuat().getAxis(), tb.getQuat().getAxis() ) 
    
        #add the motor
        cs.enableMotor(True)
        cs.setLimit(-90, 90)
        cs.setMaxMotorImpulse(5.0)  #TODO look for the unit of this thing 
        self.world.attachConstraint(cs)

        self.dof_motors[node] = cs 
        print "add constraint"


    def build(self):
        """ this function build the structure and add it in panda
            world
            - this should be called in the constructor of Creature
        """

        #create a dictionary to chech the nodes already added and linked
        self.shape_building_status = dict(zip(
            filter(lambda i: i.gen_type() == 'shape', self.metastructure.all_nodes),
            [False for i in self.metastructure.all_nodes if i.gen_type() == 'shape']))
        #print "building status {}".format(self.shape_building_status)
        self.link_building_status = dict(zip(
            filter(lambda i: i.gen_type() == 'link', self.metastructure.all_nodes),
            [[(None, None), (None, None)] for i in self.metastructure.all_nodes if i.gen_type() == 'link']))
        #print "building link status {}".format(self.link_building_status)
        # we build this to check for joints if the 2 parts of the 
        #joints have been built and the link also
        self.recursive_build(self.metastructure.head)

    def recursive_build(self, node):
        """ recursive function to build the
        structure
        -> this is where the magic appends"""
        #print " building node :{}".format(node)
        #adding
        sh1, transform = self.create_shape(node)
        self.complete_shape(sh1, node, transform)
        self.world.attachRigidBody(sh1[0])  # this must be at done at the end...
        l = self.next_link(sh1)
        while l is not None:
            #print "recursive build {}".format(l)
            self.recursive_build(l)
            l = self.next_link(sh1)

    def create_shape(self, node):
        """ create the shape and return it"""

        ode_body = OdeBody(self.physics.world)
        ode_mass = OdeMass()
        ode_mass.setBox(50, 1, 1, 1)
        bullet_node = BulletRigidBodyNode('bloc')
        render_node = render.attachNewNode(bullet_node)
        transform = TransformState.makePos(Vec3(0.0, 0.0, 0.0))
        shape = (bullet_node, render_node)
        return (shape, transform)
     
    def change_transform(self, transform, face, type='shape'):
        """ change to transform to go on a face """
        #print " change face to {}".format(face)
        mat = transform.getMat()
        mat = LMatrix4f.rotateMat(*self.quat_dict[face]) * mat
        mat = LMatrix4f.translateMat(Vec3(1.0, 0, 0)) * mat
        transform = transform.makeMat(mat)
        return transform

    def change_back_transform(self, transform, face, type='bloc'):
        #print "back transform"
        mat = transform.getMat()
        mult = LMatrix4f.rotateMat(*self.quat_dict[face])
        mult.invertInPlace()
        mat =  LMatrix4f.translateMat(Vec3(-1.0, 0, 0)) * mat
        mat =  mult * mat
        transform = transform.makeMat(mat)
        return transform


    def complete_shape(self, sh1, node, transform):
        """ create the shape then call recursive function"""
        #print "complete shape {}".format(node)
        ## construct the node
        self.add_node_to_shape(node, sh1, transform)
        if node.gen_type == 'piece':
            self.shape_building_status[node] = True
        elif node.gen_type() == 'link':
            print "## link done ##"
            self.link_building_status[node][1] = (sh1, TransformState.makeMat(transform.getMat()))
            self.build_link(node)
        ## recursive loop over the edges
        for face, edge in enumerate(node.edges[1:]):
            if edge.type() != 'empty':
                transform = self.change_transform(transform, face + 1  , type)
                if edge.gen_type() == 'shape':
                    if not self.shape_building_status[edge]:
                    #then we have to add this node (because it
                    #is not entirely finished
                        self.complete_shape(sh1, edge, transform)
                elif edge.gen_type() == 'link':
                    if self.link_building_status[edge][0][0] is None:
                        # first time we see this link
                        #print "hi new link"
                        self.add_node_to_shape(edge, sh1, transform)
                        self.link_building_status[edge][0] = (sh1, TransformState.makeMat(transform.getMat()))
                    else:
                        # link is complete:
                        #print " hi end link"
                        self.add_node_to_shape(edge, sh1)
                        self.link_building_status[edge][1] = (sh1, TransformState.makeMat(transform.getMat()))
                        self.build_link(edge)
                transform = self.change_back_transform(transform, face + 1 , type)
                        
    def next_link(self, shape):
        """ get all the half-built links going away from
        a shape. a link is a vertebra or a joint """
        #print self.link_building_status
        for edge, l in self.link_building_status.items():
            if l[0][0] == shape and l[1][0] is None:
                print "changing shape"
                return edge
        return None
    
    def add_node_to_shape(self, node, shape, transform):
        """ depending on the type of node call different
        functions """

        return {
            'head': self.build_head,
            'block': self.build_bloc,
            'vertebra': self.build_vertebra,
            'joint': self.build_joint}[node.type()](shape, transform)

    def get_variables(self):
        """ variables is probably going to be a list of list
        [[coefficient] for all angles]"""
        return self.variables

    def update_angles(self, dt):
        """update the target angles """
        self.cpg.run_all_dynamics( 0.01)
        angles = self.cpg.get_theta()
        for i, node in enumerate(self.metastructure.dof_nodes):
            self.dof_motors[node].setMotorTarget(angles[0,i], dt)
            s
