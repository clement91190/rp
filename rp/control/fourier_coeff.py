""" file used for the implementation of the CPGs """
from rp.control.control_model import ControlModel
import numpy as np

#TODO add something to scale the b_coeff depending on the params.


class Fourier_Decompos(ControlModel):
    def __init__(self, metastructure, plot=False):

        #call to superclass
        ControlModel.__init__(self, metastructure, plot)

        print "Building Fourier Decompos Model"
        self.t = 0
        self.n_harmo = 2  # number of harmonics
        self.b_coeff = np.array(self.n, self.n_harmo * 2 + 1)

    def update_t_array(self):
        self.t_array = [self.t * i for i in range(1, self.n_harmo + 1)]

    def update_theta(self, dt=0.01):
        if not self.reset:
            self.t += dt
            self.update_t_array()
        cos_sin_val = [1.0] + list(np.cos(self.t_array)) + list(np.sin(self.t_array))
        cos_sin_val = np.array(cos_sin_val)
        assert(cos_sin_val.shape[0] == self.b_coeff.shape[1])
        self.theta = np.dot(self.b_coeff, cos_sin_val).reshape(1, self.n)

    def get_size(self):
        return np.prod(self.b_coeff.shape)

    def read_parameters(self, params, reset):
        self.b_coeff = self.params.reshape(self.b_coeff.shape)
        self.reset = reset
        if self.reset:
            self.t = 0
