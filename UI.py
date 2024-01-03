import tkinter as tk
import pycountry
from Hotel import Hotel
from Database import Database


class App(tk.Tk):
    def __init__(self, db, geometry='960x600'):
        super().__init__()
        self.geometry(geometry)
        self.resizable(False, False)
        nav_bar = NavBar(('UnifrakturMaguntia', 20), self)
        hotels_frame = HotelsFrame(db.get_hotels_data(), self)

        nav_bar.pack(fill=tk.X)
        hotels_frame.pack(fill=tk.X)


class NavBar(tk.Frame):
    def __init__(self, font=None, master=None):
        super().__init__(master)
        hotels = tk.Button(self, text="Hoteluri", font=font)
        create_reservation = tk.Button(self, text="Creare Rezervare", font=font)
        manage_reservation = tk.Button(self, text="Administrare Rezervare", font=font)
        exit_button = tk.Button(self, text="Închide", command=master.quit, font=font)

        hotels.pack(side=tk.LEFT)
        create_reservation.pack(side=tk.LEFT)
        manage_reservation.pack(side=tk.LEFT)
        exit_button.pack(side=tk.RIGHT)


class HotelCard(tk.Frame):
    def __init__(self, hotel: Hotel, master=None):
        super().__init__(master, borderwidth=5, relief='solid', padx=5, pady=5)

        name_card = tk.Frame(self)
        flag = tk.Label(
            name_card, text=pycountry.countries.get(alpha_2=hotel.region[:2]).flag, font=('Times New Roman', 25)
        )
        name = tk.Label(name_card, text=hotel.name, font=('Times New Roman', 25))

        flag.pack(side=tk.LEFT)
        name.pack(side=tk.LEFT, padx=(0, 10))
        name_card.pack(fill=tk.X)

        location_card = tk.Frame(self)
        stars = tk.Label(
            location_card, text='⭐️ ' * hotel.stars, font=('Times New Roman', 20), justify=tk.LEFT, width=20, anchor='w'
        )
        subdivision = pycountry.subdivisions.get(code=hotel.region.strip())
        location_string = ''
        if subdivision is not None:
            location_string = subdivision.country.name + ', ' + subdivision.name
        if hotel.location is not None:
            location_string = location_string + ', ' + hotel.location
        location = tk.Label(location_card, text=location_string, font=('Times New Roman', 20))
        stars.pack(side=tk.LEFT)
        location.pack(side=tk.LEFT)
        location_card.pack(fill=tk.X)


class HotelsFrame(tk.Frame):
    def __init__(self, hotels, master=None):
        super().__init__(master)
        for hotel in hotels:
            hotel_card = HotelCard(hotel, self)
            hotel_card.pack(fill=tk.X, padx=5, pady=5)
