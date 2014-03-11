""" file used for the implementation of the CPGs """
from rp.control.control_model import ControlModel
import numpy as np

#TODO add something to scale the b_coeff depending on the params.


class Fourier_Decompos(ControlModel):
    def __init__(self, metastructure, plot=False):

        print " PLOTTING ", plot
        #call to superclass
        ControlModel.__init__(self, metastructure, plot)

        print "Building Fourier Decompos Model"
        self.t = 0
        self.n_harmo = 2  # number of harmonics
        self.b_coeff = np.zeros((self.n, self.n_harmo * 2 + 1))
        self.t_array = [self.t * i for i in range(1, self.n_harmo + 1)]
        print "# n of parameters  : ", self.get_size()

    def update_t_array(self):
        self.t_array = [self.t * i for i in range(1, self.n_harmo + 1)]

    def update_theta(self, dt=0.01):
        if not self.reset:
            self.t +=  0.3 * dt
            self.update_t_array()
        cos_sin_val = [1.0] + [v * 0.5 / (i + 1) * (i + 1)  for i, v in enumerate(list(np.cos(self.t_array)))] + [v * 0.5 / (i + 1) * (i + 1)  for i, v in enumerate(list(np.sin(self.t_array)))] 
        cos_sin_val = np.array(cos_sin_val)
        assert(len(cos_sin_val) == self.b_coeff.shape[1])
        self.theta = np.dot(self.b_coeff, cos_sin_val).reshape(1, self.n)
        self.right_range_for_theta()

    def get_size(self):
        return np.prod(self.b_coeff.shape)

    def read_parameters(self, params, reset):
        self.b_coeff =  0.5 * params.reshape(self.b_coeff.shape)
        self.reset = reset
        if self.reset:
            self.t = 0
            
    def run_all_dynamics(self, dt=0.01):
        self.update_theta(dt)
        if self.plot:
            self.update_plot()
    

    def random_init(self):
        self.read_parameters(np.random.random(self.b_coeff.shape), reset=True)
