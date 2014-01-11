""" file used for the implementation of the CPGs """
import numpy as np
import math
import matplotlib.pyplot as pp
import rp.cpg.rk4 as rk4
import rp.datastructure.metastructure as metastructure


"""
    theta_i = angle returned
    r, x are vectors containing the amplitude, phase and offset
    of the cell ( R,X are the desired values)
    w is the connectivity matrix (and w_i_i the frequency of cell i),
    small_phi the delay matrix and phi_i_i the phase of cell i"""

apply = lambda m, n,  t: np.matrix([[t(m, n, i, j) for j in range(n.shape[1])] for i in range(n.shape[0])])


class CPG:
    def __init__(self, metastructure, plot=False):
        """ build the vectors of the CPG """
        print "Building CPG"
        self.n = metastructure.size()
        print " {} cells".format(self.n)
        self.omega = np.zeros((1, self.n))
        self.w = metastructure.compute_and_get_connectivity_matrix()
        self.phi = np.matrix(np.zeros(self.n))
        self.angles =  np.zeros((1, self.n))
        self.angles_velocity = np.zeros((1, self.n))
        self.phi_diff_error = np.zeros((1, self.n))
        self.mean_phi_diff_error = np.zeros((1, self.n))
        self.small_phi = np.matrix(np.zeros((self.n, self.n)))
        self.r = np.zeros((1, 2 * self.n))  # we store also the derivative
        self.R = np.zeros((1, self.n))
        self.theta = np.zeros((1, self.n))
        self.x = np.zeros((1, 2 * self.n))
        self.X = np.zeros((1, self.n))
        self.real_angles = np.zeros(self.n)
        self.reset = True

        self.ar = 20.0  # rad/s
        self.ax = 20.0  # rad/s
        self.aphi = 0  # rad/s

        self.m_amp = np.matrix(np.zeros((self.n * 2, self.n * 2)))
        for i in range(self.n):
            self.m_amp[i, i + self.n] = 1
            self.m_amp[i + self.n, i] = - self.ar ** 2 / 4
            self.m_amp[i + self.n, i + self.n] = - self.ar

        self.m_offset = np.matrix(np.zeros((self.n * 2, self.n * 2)))
        for i in range(self.n):
            self.m_offset[i, i + self.n] = 1
            self.m_offset[i + self.n, i] = - self.ax ** 2 / 4
            self.m_offset[i + self.n, i + self.n] = - self.ax

        self.plot = plot

        if self.plot:
            self.plot_init()

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
            self.val[j, 0] = -1
            self.val[j, 1] = 1

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
        self.real_val[:, self.plot_ind] = self.real_angles
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

    def get_x(self):
        """ return the value without the derivative"""
        return self.x[0, :self.n]

    def get_r(self):
        """ return the value without the derivative"""
        return self.r[0, :self.n]

    def set_desired_amplitude(self, R=None):
        if R is None:
            self.R = 2 * np.random.rand(1, self.n)
        else:
            self.R = R

    def set_desired_frequency(self, W=None):
        if W is None:
            self.omega = np.random.rand(self.n) * 3
        else:
            self.omega = W

    def set_desired_offset(self, X):
        self.X = X

    @staticmethod
    def phi_diff(omega, w, phi, small_phi, rr):
        """return the temporal derivative of phi """
        t = lambda phi, small_phi, i, j: phi[0, j] - phi[0, i] - small_phi[i, j]
        phi_d = omega + rr * np.multiply(apply(phi, small_phi, t), w).T
        return phi_d
    
    def run_dynamic(self, dt=0.01):
        f = lambda t, phi: CPG.phi_diff(self.omega, self.w, phi, self.small_phi, self.get_r()) + self.aphi * self.phi_diff_error
        self.phi = rk4.rk4(0, self.phi, dt, f)

    def get_theta(self):
        if self.reset:
            return np.zeros((1, self.n))
        else:
            self.theta = self.get_x() + np.multiply(self.get_r(), np.cos(self.phi))
        return self.theta

    def run_dynamic_amp_offset(self, dt=0.01):
        """ apply runge kutta on offset and amplitude """
        f_amp = lambda t, r: r * self.m_amp.T + np.concatenate((np.zeros((1, self.n)), self.R), axis=1) * self.ar ** 2 / 4
        self.r = rk4.rk4(0, self.r, dt, f_amp)
        f_offset = lambda t, x: x * self.m_offset.T + np.concatenate((np.zeros((1, self.n)), self.X), axis=1) * self.ax ** 2 / 4
        self.x = rk4.rk4(0, self.x, dt, f_offset)

    def run_all_dynamics(self, dt=0.01):
        self.run_dynamic(dt)
        self.run_dynamic_amp_offset(dt)
        if self.plot:
            self.update_plot()
    
    def correct_speed(self):
        """ implement the correcting term for modifying the phase in consequence """
        self.phi_diff_error = np.array([self.angles_velocity[0, i] / (self.r[0, i] * math.sin(self.phi[0, i])) for i in range(self.n)])
        self.phi_diff_error = self.phi_diff_error - CPG.phi_diff(self.omega, self.w, self.phi, self.small_phi, self.get_r())
        self.mean_phi_diff_error = self.mean_phi_diff_error * 0.99 + self.phi_diff_error * 0.01
        self.phi_diff_error = - self.mean_phi_diff_error + self.phi_diff_error

    def read_angle(self, angles=None, dt=0.01):
        self.angles_velocity = (angles - self.angles) / dt
        self.angles = angles

    def get_size(self):
        """ for now the vector of parameter contain (w -> same value for all joint)
        Ri and Xi """
        return self.n * 2 + 1

    def read_parameters(self, params=None):
        if params is None:
            params = np.zeros((1, 2 * self.n + 1))
            self.reset = True
        else:
            self.reset = False
        self.omega = params[0, 0] * 3 * np.ones(self.n)
        self.X[0,:] = (params[0, 1:self.n + 1] - 0.5) * math.pi
        self.R[0,:] = params[0, self.n + 1:] 


def main():
    print "Building Meta Structure"
    m = metastructure.MetaStructure()
    size = 5
    for i in range(size):
        m.add_block()
        m.follow_edge()
        m.add_joint()
        m.follow_edge()

    control = CPG(m)
    control.set_desired_frequency()
    control.set_desired_amplitude()

    steps = 1000

#plot
    print "Plot results"
   
    print "Start Simulation"
    #simulation
    for i in range(steps):
        control.run_all_dynamics()
        if i == 500:
            control.set_desired_amplitude()
   #pp.figure(1)

if __name__ == '__main__':
    main()
