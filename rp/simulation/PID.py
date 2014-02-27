import math
import matplotlib.pyplot as pp

class PID():
    def __init__(self, gd=0.6, gi=0.25):
        
        self.x = 0
        self.dx = 0
        self.ix = 0
        
        self.gd = gd
        self.gi = gi
        self.er = 0
        self.ge = 0.2
        self.target_value = 0
        self.mu = 0.01
        self.globalg = 25
        self.count = 0
        self.satu = 100


    def set_target_value(self, target_value):
        self.target_value = target_value

    def read(self, x):
        self.x = x

    def reset(self):
        self.ix = 0.

    def step(self, satu_cmd):
        er = self.target_value - self.x
        self.dx = er - self.er
        self.ix += self.mu * er # + (1 - self.mu) * self.ix
        self.er = er
        self.satu = satu_cmd
        
        command = self.globalg * (self.ix * self.gi + self.dx * self.gd + self.ge * self.er)
        if command > self.satu:
            self.ix -= self.er * self.mu
            return self.control(self.satu)
        elif command < -self.satu:
            self.ix -= self.er * self.mu
            return self.control(-self.satu)
        else:
            command = self.globalg * (self.ix * self.gi + self.dx * self.gd + self.ge * self.er)
            return self.control(command)

    def control(self, cmd, limit=math.pi * 0.75):
        angle = self.x
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
