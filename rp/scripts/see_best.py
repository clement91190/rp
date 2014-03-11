#cd "/home/clement/src/rp/rp/"
from rp.optim_server.optim_server.db import models as m
import numpy as np
import rp.utils.config
rp.utils.config.config.visual=True
from rp.simulation import world_ode as w


objs = m.ParamInstance.objects(optim_problem="quad_learning", optim_run=0, done=True).order_by('-score')
obj = objs[0]
print obj.score
print obj.params
params = np.array(obj.params)
params.reshape((1,20))


#sys.path.insert(0, "/home/clement/src/rp/")
app = w.MyApp()
app.add_four_legs_creature(True)
app.see_params(params)

