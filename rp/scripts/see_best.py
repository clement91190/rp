import rp.utils.config

rp.utils.config.config.visual=True

from rp.simulation import world_ode as w


app = w.MyApp()

#for i in range(2, 7):
#    app.add_snake(i)
#    app.run(100, visual=False)
#app.add_snake(6)
#app.add_creature(True)
app.add_four_legs_creature(True)
app.see_best()
