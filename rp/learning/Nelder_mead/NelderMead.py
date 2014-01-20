import pickle
import numpy as np
from rp.learning.interface import Interface


class NelderMead(Interface):
    def __init__(self, size):
        self.size = size
        self.n = self.size + 1
        self.num_of_points_to_test = -1
        self.points_and_v = []
        self.evalr = False
        self.evalc_or_e = False
        self.resr = 0
        self.rese_or_c = 0
        self.random_init()

    def random_init(self):
        """ generate self.size + 1 points in the research space """
        for i in range(self.n):
            self.points_and_v.append((np.random.rand(1, self.size), 0))

    def next_val_to_test(self):
        """ logic of Nelder Mead """
        if self.num_of_points_to_test >= self.n - 1:
            if not self.evalr:
                self.update_simplex()
                print "eval xr"
                return self.xr
            else:
                if not self.evalc_or_e:
                    _, vn = self.points_and_v[-2]
                    xn_1, vn_1 = self.points_and_v[-2]
                    if self.resr > vn:
                        self.xe_or_c = self.x0 + 2 * (self.x0 - xn_1)
                        self.evale = True
                    else:
                        self.xe_or_c = xn_1 + 0.5 * (self.x0 - xn_1)
                        self.evale = False
                    self.evalc_or_e = True
                    print "eval xe_or_c"
                    return self.xe_or_c
                else:
                    if self.evale:
                        if self.rese_or_c > self.resr:
                            self.points_and_v[-1] = (self.xe_or_c, self.rese_or_c)
                        else:
                            self.points_and_v[-1] = (self.xr, self.resr)
                    else:
                        if self.rese_or_c >= self.points_and_v[-2][1]:
                            self.points_and_v[-1] = (self.xe_or_c, self.rese_or_c)
                        else:
                            self.homotethia()
                            self.num_of_points_to_test = 0
                    self.evalc_or_e = self.evalr = False
        else:
            self.num_of_points_to_test += 1
        print "eval x", self.num_of_points_to_test
        return self.points_and_v[self.num_of_points_to_test][0]

    def set_result(self, res):
        print "results ", res
        if self.evalr:
            if self.evalc_or_e:
                self.rese_or_c = res
            else:
                self.resr = res
        else:
            if self.num_of_points_to_test >= 0:
                p = self.points_and_v[self.num_of_points_to_test][0]
                self.points_and_v[self.num_of_points_to_test] = (p, res)

    def update_simplex(self):
        print "update"
        print self.points_and_v
        self.points_and_v.sort(key=lambda(p, res): -res)  # best score at the start
        self.save_best()
        self.x0 = np.array([p for (p, res) in self.points_and_v]).mean(axis=0)  # center of gravity
        self.xr = 2 * self.x0 - self.points_and_v[-1][0]  # reflexion of xn+1
        self.evalr = True

    def homotethia(self):
        """ homotethia of scale 0.5 centered on best point """
        x1 = self.points_and_v[0][0]
        for i, (xi, res) in enumerate(self.points_and_v[1:]):
            self.points_and_v[i + 1] = (0.5 * (xi - x1), 0 )
            try: 
                assert len(np.shape(self.points_and_v[i + 1][0])) == 2
            except:
                print self.points_and_v[i + 1][0]
                raw_input()
        print "homotethia"

    def save_best(self):
        print "best score", self.points_and_v[0][1]
        with open('results.txt', 'w') as fich:
            pickle.dump(self.points_and_v[0][0], fich)


def test_f(params):
    print " testing for params ", params
    return 10 - np.average([p ** 2 for p in params])


def main():

    optim = NelderMead(1)
    while True:
        params = optim.next_val_to_test()
        res = test_f(params)
        print " res", res
        optim.set_result(res)


if __name__ == "__main__":
    main()


