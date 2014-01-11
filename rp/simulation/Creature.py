import math
from panda3d.core import Vec3, LMatrix4f,  LQuaternionf, TransformState
from panda3d.ode import OdeHingeJoint
from panda3d.ode import OdeBody, OdePlaneGeom 

from rp.cpg import cpg
from rp.simulation.MultiBox import MultiBoxFactory
from rp.learning.interface import Interface
from rp.learning.Nelder_mead.NelderMead import NelderMead
from rp.simulation.PID import PID
"""file of definition of the physical engine and
3D display of the world """


class Creature():
    def __init__(self, metastructure, physics, render, cpg_graph=False):
        """constructor of the class
        use the metastructure"""
        self.metastructure = metastructure
        self.satu_cmd = 5
        self.physics = physics
        self.render = render
        self.quat_dict = {
            1: (0, Vec3(1, 0, 0)),
            2: (90, Vec3(0, 1, 0)),
            3: (-90, Vec3(0, 1, 0)),
            4: (90, Vec3(0, 0, 1)),
            5: (-90, Vec3(0, 0, 1))}
        self.dof_motors = {}
        self.factory = MultiBoxFactory(self.physics, self.render)
        self.build()
        self.cpg = cpg.CPG(self.metastructure, cpg_graph)
        self.cpg.set_desired_frequency()
        self.cpg.set_desired_amplitude()
        self.position = 0
        self.problem = False
        self.penalty = 0

    def affect_optimizer(self, interface=None):
        """ affect to the structure a learning process """
        if interface is None:
            #self.brain = Interface(self.cpg.get_size())
            self.brain = NelderMead(self.cpg.get_size())
        else:
            self.brain = interface
        self.update_position()

    def send_result_to_brain(self):
        traveled_distance = self.update_position()
        if self.brain is not None:
            if traveled_distance.length() == 0:
                self.brain.set_result(self.penalty)
                self.penalty = 0
            else:
                self.brain.set_result(traveled_distance.length())
            self.cpg.read_parameters(self.brain.next_val_to_test())

    def update_position(self):
        """ update the position and return the traveled distance """
        position = self.get_position()
        traveled_distance = position - self.position
        self.position = position
        if self.problem:
            self.problem = False
            return self.position - position
        return traveled_distance

    def get_position(self):
        """ return the position of the center of
        gravity of the multibox containing the head """
        return self.factory.get_position()

    def build_head(self, id_mb, transform):
        """ build the head of the creature """
        print "add head"
        size = 0.5
        color = (1, 1, 1)
        self.factory.add_to_multi(size, transform, color, id_mb)

    def build_bloc(self, id_mb, transform):
        print " add bloc at {}".format(transform)
        size = 0.5
        color = (0, 1, 1)
        self.factory.add_to_multi(size, transform, color, id_mb)

#TODO  implement this function with different cases
    def build_joint(self, id_mb, transform):
        print " add joint at {}".format(transform)
        size = 0.25
        color = (1, 0, 1)
        self.factory.add_to_multi(size, transform, color, id_mb)

#TODO  implement this function with different cases
    def build_vertebra(self, id_mb, transform):
        print " add vertebra at {}".format(transform)
        size = 0.25
        color = (1, 1, 0)
        self.factory.add_to_multi(size, transform, color, id_mb)

    def build_link(self, node):
        
        (id_bda, ta), (id_bdb, tb) = self.link_building_status[node] 

        bda = self.factory.multiboxes[id_bda]
        bdb = self.factory.multiboxes[id_bdb]
        
        pos =  bda.body.getPosition()
        quat = LQuaternionf(bda.body.getQuaternion())
        mat = TransformState.makePosQuatScale(pos, quat, Vec3(1, 1, 1)).getMat()
        mat = ta.getMat() * mat
        print "ta", ta

        print "absol", TransformState.makeMat(mat)
        mat = LMatrix4f.translateMat(Vec3(0.5, 0, 0)) * mat
        anchor = TransformState.makeMat(mat).getPos() 
        print "absol", TransformState.makeMat(mat)
        
        axis = self.quat_dict[1][1]
        if node.orientation == 1:
            t = LMatrix4f.rotateMat(*self.quat_dict[4]) * mat
        else:
            t = LMatrix4f.rotateMat(*self.quat_dict[2]) * mat
        row = t.getRow(0)
        print "rotation", t.getRow(0), type(t.getRow(0))
        #axis = t.getQuat().getAxis()
        axis = Vec3(row.getX(), row.getY(), row.getZ())
        print "axis",axis
        print "anchor", anchor

        mat = LMatrix4f.translateMat(Vec3(0.5, 0, 0)) * mat
        mat = tb.getInverse().getMat() * mat
        t = TransformState.makeMat(mat)
        posb = t.getPos()
        quatb = t.getQuat()

        bdb.body.setPosition(posb)
        bdb.body.setQuaternion(quatb)

        cs = OdeHingeJoint(self.physics.world, self.physics.servogroup)
        cs.attach(bda.body, bdb.body)
        cs.setAxis(axis)
        cs.setAnchor(anchor)
        
        #add the motor
        cs.setParamFMax(self.satu_cmd)
        cs.setParamFudgeFactor(0.5)
        cs.setParamCFM(11.1111)
        cs.setParamStopCFM(11.1111)
        cs.setParamStopERP(0.444444)
        cs.setParamLoStop(- math.pi * 0.5)
        cs.setParamHiStop(math.pi * 0.5)
        pid = PID()

        self.dof_motors[node] = (cs, pid)
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
        self.factory.finish()

    def recursive_build(self, node):
        """ recursive function to build the
        structure
        -> this is where the magic appends"""
        #print " building node :{}".format(node)
        #adding
        id_mb1, transform = self.create_shape(node)
        self.complete_shape(id_mb1, node, transform)
        #self.world.attachRigidBody(id_mb1[0])  # this must be at done at the end...
        l = self.next_link(id_mb1)
        while l is not None:
            #print "recursive build {}".format(l)
            self.recursive_build(l)
            l = self.next_link(id_mb1)

    def create_shape(self, node):
        """ create the shape and return it"""

        id_of_multibox = self.factory.create() 
        transform = TransformState.makePos(Vec3(0.0, 0.0, 0.0))
        return (id_of_multibox, transform)
     
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
        mat = LMatrix4f.translateMat(Vec3(-1.0, 0, 0)) * mat
        mat = mult * mat
        transform = transform.makeMat(mat)
        return transform


    def complete_shape(self, id_mb1, node, transform):
        """ create the shape then call recursive function"""
        #print "complete shape {}".format(node)
        ## construct the node
        self.add_node_to_shape(node, id_mb1, transform)
        if node.gen_type == 'piece':
            self.shape_building_status[node] = True
        elif node.gen_type() == 'link':
            self.link_building_status[node][1] = (id_mb1, TransformState.makeMat(transform.getMat()))
            self.build_link(node)
        ## recursive loop over the edges
        for face, edge in enumerate(node.edges[1:]):
            if edge.type() != 'empty':
                transform = self.change_transform(transform, face + 1, type)
                if edge.gen_type() == 'shape':
                    if not self.shape_building_status[edge]:
                    #then we have to add this node (because it
                    #is not entirely finished
                        self.complete_shape(id_mb1, edge, transform)
                elif edge.gen_type() == 'link':
                    if self.link_building_status[edge][0][0] is None:
                        # first time we see this link
                        #print "hi new link"
                        self.add_node_to_shape(edge, id_mb1, transform)
                        self.link_building_status[edge][0] = (id_mb1, TransformState.makeMat(transform.getMat()))
                    else:
                        # link is complete:
                        #print " hi end link"
                        self.add_node_to_shape(edge, id_mb1)
                        self.link_building_status[edge][1] = (id_mb1, TransformState.makeMat(transform.getMat()))
                        self.build_link(edge)
                transform = self.change_back_transform(transform, face + 1, type)

    def next_link(self, shape):
        """ get all the half-built links going away from
        a shape. a link is a vertebra or a joint """
        #print self.link_building_status
        for edge, l in self.link_building_status.items():
            if l[0][0] == shape and l[1][0] is None:
                print "changing shape"
                return edge
        return None

    def add_node_to_shape(self, node, id_mb, transform):
        """ depending on the type of node call different
        functions """

        return {
            'head': self.build_head,
            'block': self.build_bloc,
            'vertebra': self.build_vertebra,
            'joint': self.build_joint}[node.type()](id_mb, transform)

    def get_variables(self):
        """ variables is probably going to be a list of list
        [[coefficient] for all angles]"""
        return self.variables

    def update_angles(self, dt):
        """update the target angles """
        self.cpg.run_all_dynamics(0.01)
        angles = self.cpg.get_theta()
     
        #self.cpg.read_angle(angles, 0.01)
        #self.cpg.correct_speed()
        for i, node in enumerate(self.metastructure.dof_nodes):
            (hinge, pid) = self.dof_motors[node]
            pid.set_target_value(angles[0, i])
            cmd = pid.step(self.satu_cmd)
            #cmd = angles[0, i] * 400
            #print "commande" , cmd
            pid.read(hinge.getAngle())
            hinge.addTorque(cmd)
            #print hinge.getAngle()
            self.cpg.real_angles[i] = hinge.getAngle()
            #hinge.addTorque(5)
            if abs(hinge.getAngleRate()) > 100:
                #print "problem"
                self.problem = True
                if self.penalty > - abs(hinge.getAngleRate()):
                    self.penalty = - abs(hinge.getAngleRate())
            #print i, hinge.getParamVel(), hinge.getAngleRate()

    def draw(self):
        self.factory.draw()
