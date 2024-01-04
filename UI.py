import tkinter as tk
from HotelCard import HotelCard, ScoreCard
from NavBar import NavBar


class App(tk.Tk):
    def __init__(self, db, geometry='960x600'):
        super().__init__()
        self.geometry(geometry)
        self.minsize(width=960, height=600)
        # self.resizable(False, False)
        self.db = db

        hotels_frame = HotelsFrame(self.db, master=self)

        NavBar((
            ('Hoteluri', lambda: hotels_frame.show_hotels()),
            ('Creare Rezervare', None),
            ('Administrare Rezervare', None)
        ), master=self).pack(fill=tk.X, padx=1, pady=1)

        hotels_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=True)


class AppFrame(tk.Frame):
    def __init__(self, bg='gray', master=None):
        super().__init__(master=master, bg=bg, relief='solid', borderwidth=5, padx=10, pady=10)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()


class HotelsFrame(AppFrame):
    def __init__(self, db, master=None):
        super().__init__(master=master)
        self.db = db
        self.show_hotels()

    def show_hotels(self):
        self.clear()
        hotels = self.db.get_hotels_data()
        for i in range(len(hotels)):
            HotelCard(
                hotels[i], ('Recenzii', lambda val=i: self.show_reviews(hotels[val])),
                'green', master=self
            ).pack(fill=tk.X, pady=(int(i != 0) * 10, 0))

    def show_reviews(self, hotel):
        self.clear()
        HotelCard(
            hotel, ('Înapoi', lambda: self.show_hotels()), 'gold', master=self
        ).pack(fill=tk.X)
        ScoreCard(
            self.db.get_hotel_score(hotel), self.db.get_hotel_nr_reviews(hotel), master=self
        ).pack(fill=tk.X, pady=(10, 0))
