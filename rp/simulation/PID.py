import math
import matplotlib.pyplot as pp

class PID():
    def __init__(self, gd=0.7, gi=0.3):
        self.x = 0
        self.dx = 0
        self.ix = 0
        self.gd = gd
        self.gi = gi
        self.er = 0
        self.ge = 0.3
        self.target_value = 0
        self.mu = 0.1
        self.globalg = 500
        self.enableIntegrator = False
        self.count = 0
        self.satu = 50


    def set_target_value(self, target_value):
        self.target_value = target_value

    def read(self, x):
        self.x = x

    def step(self):
        er = self.target_value - self.x
        self.dx = er - self.er
        self.ix = self.mu * er + (1 - self.mu) * self.ix
        self.er = er
        if (not self.enableIntegrator) and self.count > 100:
            self.enableIntegrator = True
            print "start integrator"
        elif not self.enableIntegrator:
            self.count += 1
        command = self.globalg * (self.ix * self.gi * self.enableIntegrator + self.dx * self.gd + self.ge * self.er)
        if command > self.satu:
            print "satu"
            return self.satu
        elif command < -self.satu:
            print "satu"
            return -self.satu
        else:
            return command


def control(cmd, angle, limit = math.pi):
    if angle > limit and cmd > 0:
        return 0.
    elif angle < -limit and cmd < 0:
        return 0. 
    else:
        return cmd

def main():
    tmax = 100
    pid = PID()
    tv = 5
    pid.set_target_value(tv)
    value = 0
    all_valls = []
    for t in range(tmax):
        pid.read(value)
        value += pid.step()
        all_valls.append(value)
    print "done"
    pp.plot(all_valls)
    pp.show()


if __name__ == "__main__":
    main()
