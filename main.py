import UI
from Database import Database

db = Database('bd076/bd076@bd-dc.cs.tuiasi.ro:1539/orcl')
app = UI.App(db)
app.mainloop()
