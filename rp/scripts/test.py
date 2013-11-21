from rp.simulation import world as w

app = w.MyApp(w.MyWorld())

#for i in range(2, 7):
#    app.add_snake(i)
#    app.run(100, visual=False)
app.add_creature()

app.run(10000, visual=True)
