""" file used for the implementation of the CPGs """
import numpy as np
import matplotlib.pyplot as pp
#import rp.datastructure.metastructure as metastructure


class ControlModel(object):
    """ abstract class to represent the layer between the control of the joints angle and the learning algorithm """
    def __init__(self, metastructure, plot=False):
        print "Building generic ControlModel"
        self.plot = plot
        self.n = metastructure.size()
        self.reset = True

        #variables
        self.theta = np.zeros((1, self.n))  # theta is the target
        self.angles = np.zeros(self.n)  # angles is the mesured value
        self.angles_velocity = np.zeros(self.n)
        
        if self.plot:
            self.plot_init()

    def get_theta(self):
        """ return the target value of the angles """
        self.update_theta()
        return self.theta

    def get_size(self):
        """ return the size of params """
        pass

    def read_parameters(self, params, reset):
        """ update the parameters of the control model, 
        and option to reset, """
        pass

    def plot_init(self):
        self.simu_time = 10
        self.step = 3000
        self.t_space = np.linspace(0, self.simu_time, self.step)
        self.fig = pp.figure(1)
        self.line = []
        self.linereal = []
        self.val = np.zeros((self.n, self.step))
        self.real_val = np.zeros((self.n, self.step))
        for j in range(self.n):
            self.val[j, 0] = - 3.5
            self.val[j, 1] = 3.5

        for j in range(self.n):
            pp.subplot(self.n, 1, j + 1).set_autoscaley_on(True)
            pp.ion()
            linej, = pp.plot(self.t_space, self.val[j, :])
            linejreal, = pp.plot(self.t_space, self.real_val[j, :])
            self.line.append(linej)
            self.linereal.append(linejreal)
        self.plot_ind = 0

    def update_plot(self):
        self.val[:, self.plot_ind] = self.get_theta()
        #self.real_val[:, self.plot_ind] = self.real_angles
        self.real_val[:, self.plot_ind] = self.angles
        #ploting
        if self.plot_ind < self.step - 1:
            self.plot_ind += 1
        if self.plot_ind % 10 == 0:
            for j in range(self.n):
                #print "update ", i , j
                self.line[j].set_ydata(self.val[j, :])
                self.linereal[j].set_ydata(self.real_val[j, :])
                pp.subplot(self.n, 1, j + 1)
            self.fig.canvas.draw()

