import UI
from Database import Database

db = Database()
hotels = db.get_hotel_data()

app = UI.App()
app.mainloop()
