from rp.simulation import world as w

app = w.MyApp(w.MyWorld())
app.add_creature()
app.run(1000, visual=True)
