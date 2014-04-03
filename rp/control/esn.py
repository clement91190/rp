""" file used for the implementation of the CPGs """
import numpy as np
import math
import matplotlib.pyplot as pp
import rp.cpg.rk4 as rk4
import rp.datastructure.metastructure as metastructure


class LiquidLayer():
    def __init__(self, input, size=50):
        self.size = 50
        self.Vm = np.zeros()
        self.Cm = 1.0
        self.Gm = 1.0
        self.phi = np.random.random((size, size))
        self.phi_input = np.random.random((size, len(input)))
        if len(input) == 0:
            input = [0]
            self.phi_input = np.zeros((size, 1)) 
        self.input = input
        #TODO add connection from input matrix
        self.t = 0
        self.activation = np.tanh

    def integrate(self, dt):
        """update the dynamic of the layer """
        f = lambda t, y: self.Cm * (np.dot(self.phi, self.activation(y)) + np.dot(self.phi_input, self.activation(self.input)) - self.Gm * y)
        self.Vm = rk4(self.t, self.Vm, self.t + dt, f)


class EchoStateNetwork(ControlModel):
    def __init__(self):
        self.input_layer = []
        size = 50
        self.liquid_layer = LiquidLayer(self.input_layer, size)
        self.phi_out = np.random.random((size, n))
        #self.output_layer = 
