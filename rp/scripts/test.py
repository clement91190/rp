from rp.simulation import world_ode as w

app = w.MyApp()

#for i in range(2, 7):
#    app.add_snake(i)
#    app.run(100, visual=False)
app.add_snake(1)

app.run(10000, visual=True)
