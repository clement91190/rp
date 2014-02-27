import numpy as np
import pickle


class Interface:
    """Model that any optimisation algorithm needs to follow (here random)"""
    def __init__(self, size, init=None):
        self.size = size
        self.result = 0
        self.init = np.random.rand(1, self.size)
        if init:
            self.init = init
        else:
            self.init = np.random.rand(1, self.size)
        self.best_score = 0
        self.best_val = np.random.rand(1, self.size)

    def next_val_to_test(self):
        """ return the new vector of parameters to test, default, random between 0 and 1"""
        self.current = np.random.rand(1, self.size)
        return self.current

    def set_result(self, res):
        """return the result and call for new result """
        self.result = res
        print "traveled distance", res 
        if self.best_score < self.result:
            self.best_score = self.result
            print " new best score ", self.best_score
            self.best_val = self.current
            self.save_best()

    def save_best(self):
        with open('results.txt', 'w') as fich:
            pickle.dump(self.best_val, fich)

class TestRandom(Interface):
    def __init__(self, size):
        self.current = np.random.random(size)

    def next_val_to_test(self):
        return self.current

    def set_result(self, res):
        print "traveled distance", res 


class TestBest(Interface):
    def __init__(self):
        with open('results.txt', 'r') as fich:
            self.current = pickle.load(fich)
            print " loading best score", self.current

    def next_val_to_test(self):
        return self.current

    def set_result(self, res):
        print "traveled distance", res 


class TestGiven(Interface):
    def __init__(self, params):
        self.current = params 
        print " loading ", self.current

    def next_val_to_test(self):
        return self.current

    def set_result(self, res):
        print "traveled distance", res 
