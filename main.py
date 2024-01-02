import UI
from Database import Database

db = Database()
app = UI.App(db)
app.mainloop()