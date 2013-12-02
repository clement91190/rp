import time
import math

class BrainControl:
    def __init__(self):
        pass

    def calc_angles(self, metastructure):
        """return a dictionary linking dof nodes to a target angle"""
        return{node: math.pi * 0.5 * math.sin(time.time() + node.phi) for node in metastructure.dof_nodes}    



