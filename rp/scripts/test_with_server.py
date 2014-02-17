import sys
sys.path.append('/home/clement/src/rp/rp/optim_server')

from rp.simulation import world_ode as w
app = w.MyApp()

#for i in range(2, 7):
#    app.add_snake(i)
#    app.run(100, visual=False)
#app.add_snake(6)
#app.add_creature()
app.add_four_legs_creature()
app.learn_with_server()
#app.run(1500, visual=True)
#app.run(500, visual=False)
