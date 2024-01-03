import tkinter as tk
from HotelCard import HotelCard
from NavBar import NavBar


class App(tk.Tk):
    def __init__(self, db, geometry='960x600'):
        super().__init__()
        self.geometry(geometry)
        #self.resizable(False, False)
        self.db = db
        hotels_frame = HotelsFrame(self.get_hotels(), master=self)

        NavBar((
            ('Hoteluri', lambda: hotels_frame.show_hotels()),
            ('Creare Rezervare', None),
            ('Administrare Rezervare', None)
        ), master=self).pack(fill=tk.X, padx=1, pady=1)

        hotels_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=True)

    def get_hotels(self):
        return self.db.get_hotels_data()


class AppFrame(tk.Frame):
    def __init__(self, bg='gray', master=None):
        super().__init__(master=master, bg=bg, relief='solid', borderwidth=5, padx=10, pady=10)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()


class HotelsFrame(AppFrame):
    def __init__(self, hotels, master=None):
        super().__init__(master=master)
        self.hotels = hotels
        self.show_hotels()

    def show_hotels(self):
        self.clear()
        for i in range(len(self.hotels)):
            HotelCard(
                self.hotels[i], ('Recenzii', lambda val=i: self.show_reviews(self.hotels[val])),
                'green', master=self
            ).pack(fill=tk.X, pady=(int(i != 0) * 10, 0))

    def show_reviews(self, hotel):
        self.clear()
        HotelCard(
            hotel, ('Înapoi', lambda: self.show_hotels()), 'gold', master=self
        ).pack(fill=tk.X)
