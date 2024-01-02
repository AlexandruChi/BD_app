import tkinter as tk
from Hotel import Hotel

class App(tk.Tk):
    def __init__(self, geometry='960x600'):
        super().__init__()
        self.geometry(geometry)
        self.resizable(False, False)
        nav_bar = NavBar(self, ('UnifrakturMaguntia', 20))
        nav_bar.pack(fill=tk.X)


class NavBar(tk.Frame):
    def __init__(self, master=None, font=None):
        super().__init__(master)
        hotels = tk.Button(self, text="Hoteluri", font=font)
        create_reservation = tk.Button(self, text="Creare Rezervare", font=font)
        manage_reservation = tk.Button(self, text="Administrare Rezervare", font=font)
        exit_button = tk.Button(self, text="Închide", command=master.quit, font=font)

        hotels.pack(side=tk.LEFT)
        create_reservation.pack(side=tk.LEFT)
        manage_reservation.pack(side=tk.LEFT)
        exit_button.pack(side=tk.RIGHT)

        self.pack()


class HotelCard(tk.Frame):
    def __init__(self, hotel: Hotel, master=None):
        super().__init__(master)
        name = tk.Label(self, text=hotel.name, font=('Times New Roman', 15))

        name.pack(side=tk.LEFT)

        self.pack()


class HotelsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)