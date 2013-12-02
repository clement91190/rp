""" file used for the implementation of the CPGs """
import numpy as np
import rk4
import math

"""
    theta_i = angle returned
    r, x are vectors containing the amplitude, phase and offset
    of the cell ( R,X are the desired values)
    w is the connectivity matrix (and w_i_i the frequency of cell i),
    small_phi the delay matrix and phi_i_i the phase of cell i"""

apply = lambda m, t: np.matrix([[t(m, i, j) for j in range(m.shape[1])] for i in range(m.shape[0])])


class CPG:
    def __init__(self, metastructure):
        """ build the vectors of the CPG """
        self.n = metastructure.size()
        self.w = metastructure.compute_and_get_connectivity_matrix()
        self.phi = np.matrix(np.zeros((self.n, self.n)))
        self.r = np.zeros((1, 2 * self.n))  # we store also the derivative
        self.R = np.zeros((1, self.n))
        self.theta = np.zeros((1, self.n))
        self.x = np.zeros((1, 2 * self.n))
        self.X = np.zeros((1, self.n))

        self.ar = 20.0  # rad/s
        self.ax = 20.0  # rad/s

    def get_x(self):
        """ return the value without the derivative"""
        return self.x[:self.n]

    def get_r(self):
        """ return the value without the derivative"""
        return self.r[:self.n]

    def set_desired_amplitude(self, R):
        self.R = R

    def set_desired_frequency(self, W):
        for i, W_i in enumerate(W):
            self.w[i, i] = W[0, i]

    def set_desired_offset(self, X):
        self.X = X

    @staticmethod
    def phi_diff(w, phi, r):
        """return the temporal derivative of phi """
        t = lambda m, i, j: m[j, j] - m[i, i] - m[i, j]
        return np.diag(np.diag(w) + r * np.multiply(apply(phi, t), w).T)

    def run_dynamic(self, dt):
        f = lambda t, phi: CPG.phi_diff(self.w, phi, self.get_r())
        self.phi = rk4.rk4(0, self.phi, dt, f)
        self.theta = self.get_x() + self.get_r() * math.cos(np.diag(self.phi))
        
    def run_dynamic_amp_offset(self, dt):
        """ apply runge kutta on offset and amplitude """
        #TODO put this in the constructor. and implement it for offset 
        m_amp = np.zeros((self.n * 2 , self.n * 2))
        for i in range(1,n):
            m_amp[i, i + self.n] = 1
            m_amp[i + self.n, i ] = - self.ar ** 2 / 4 
            m_amp[i + self.n, i + self.n ] = - self.ar
            
        f_amp = lamda t, r :  m_amp * r + numpy.concatenate((zeros(self.n), self.R) * self.ar / 4

        self.r = rk4.rk4(0, self.r, dt, f_amp)



