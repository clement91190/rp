""" file used for the implementation of the CPGs """
import numpy as np
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
    def __init__(self, metastructure):
        """ build the vectors of the CPG """
        print "Building CPG"
        self.n = metastructure.size()
        print " {} cells".format(self.n)
        self.omega = np.zeros((1, self.n))
        self.w = metastructure.compute_and_get_connectivity_matrix()
        self.phi = np.matrix(np.zeros(self.n))
        self.small_phi = np.matrix(np.zeros((self.n, self.n)))
        self.r = np.zeros((1, 2 * self.n))  # we store also the derivative
        self.R = np.zeros((1, self.n))
        self.theta = np.zeros((1, self.n))
        self.x = np.zeros((1, 2 * self.n))
        self.X = np.zeros((1, self.n))

        self.ar = 20.0  # rad/s
        self.ax = 20.0  # rad/s

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

    def get_x(self):
        """ return the value without the derivative"""
        return self.x[0, :self.n]

    def get_r(self):
        """ return the value without the derivative"""
        return self.r[0, :self.n]

    def set_desired_amplitude(self, R=None):
        if R is None:
            self.R = 45 * np.random.rand(1, self.n)
        else:
            self.R = R

    def set_desired_frequency(self, W=None):
        if W is None:
            self.omega = np.random.rand(self.n) * 10
        else:
            self.omega = W
        
    def set_desired_offset(self, X):
        self.X = X

    @staticmethod
    def phi_diff(omega, w, phi, small_phi, rr):
        """return the temporal derivative of phi """
        t = lambda phi, small_phi, i, j: phi[0, j] - phi[0, i] - small_phi[i, j]
        return omega + rr * np.multiply(apply(phi, small_phi, t), w).T

    def run_dynamic(self, dt=0.01):
        f = lambda t, phi: CPG.phi_diff(self.omega, self.w, self.phi, self.small_phi, self.get_r())
        self.phi = rk4.rk4(0, self.phi, dt, f)

    def get_theta(self):
        self.theta = self.get_x() + np.multiply(self.get_r(), np.cos(self.phi))
        return self.theta

    def run_dynamic_amp_offset(self, dt=0.01):
        """ apply runge kutta on offset and amplitude """
        f_amp = lambda t, r: r * self.m_amp.T + np.concatenate((np.zeros((1, self.n)), self.R), axis=1) * self.ar ** 2 / 4
        self.r = rk4.rk4(0, self.r, dt, f_amp)
        f_offset = lambda t, x: x * self.m_offset.T + np.concatenate((np.zeros((1, self.n)), self.X), axis=1) * self.ax ** 2 / 4
        self.x = rk4.rk4(0, self.x, dt, f_offset)


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

    simu_time = 10
    t_space = np.linspace(0, simu_time, 1000)

    print "Start Simulation"
    #simulation
    val = np.zeros((control.n, 1000))
    for i, t in enumerate(t_space):
        control.run_dynamic()
        control.run_dynamic_amp_offset()
        #val[:, i] = control.R - control.get_r()
        # val[:, i] = control.get_x()
        val[:, i] = control.get_theta()
        #val[:, i] = (control.phi)
    print "Plot results"

    #plot
    pp.figure(1)
    for i in range(control.n):
        pp.subplot(control.n, 1, i + 1)
        pp.plot(t_space, np.array(val[i, :]))

    pp.show()


if __name__== '__main__': 
    main()   
