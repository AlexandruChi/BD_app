import tkinter as tk
from Cards import HotelCard, ScoreCard, ReviewCard, UserDetailsCard
from NavBar import NavBar


class App(tk.Tk):
    def __init__(self, db, geometry='960x600'):
        super().__init__()
        self.geometry(geometry)
        self.minsize(width=960, height=600)
        # self.resizable(False, False)
        # self.attributes('-fullscreen', True)
        self.db = db
        self.frame = None

        NavBar((
            ('Hoteluri', lambda: self.show_frame(HotelsFrame)),
            ('Creare Rezervare', lambda: self.show_frame(ReservationFrame)),
            ('Administrare Rezervare', lambda: self.show_frame(ManageFrame))
        ), master=self).pack(fill=tk.X, padx=1, pady=1)

        self.show_frame(HotelsFrame)

    def show_frame(self, frame):
        if self.frame is not None:
            self.frame.destroy()
        self.frame = frame(self.db, master=self)
        self.frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=True)


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

        review = tk.Frame(master=self, bg=self.cget('bg'))
        ReviewCard(
            self.db.get_hotel_reviews_data(hotel), master=review
        ).pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=(10, 0), padx=(0, 10))
        ScoreCard(
            self.db.get_hotel_score(hotel), self.db.get_hotel_nr_reviews(hotel), master=review
        ).pack(side=tk.TOP, pady=(10, 0))
        review.pack(fill=tk.BOTH, expand=1)


class ReservationFrame(AppFrame):
    def __init__(self, db, master=None):
        super().__init__(master=master)
        self.db = db
        self.name = tk.StringVar()
        self.CNP = tk.StringVar()
        self.reservation_frame = None
        self.select_hotel()

    def select_hotel(self):
        self.clear()
        hotels = self.db.get_hotels_data()
        for i in range(len(hotels)):
            HotelCard(
                hotels[i], ('Rezervă', lambda val=i: self.create_reservation(hotels[val])), 'green', master=self
            ).pack(pady=(int(i != 0) * 10, 0), fill=tk.X)

    def create_reservation(self, hotel):
        self.clear()
        HotelCard(
            hotel, ('Anulare', lambda: self.select_hotel()), 'red', master=self
        ).pack(fill=tk.X)

        self.enter_user_details()

    def enter_user_details(self):
        if self.reservation_frame is not None:
            self.reservation_frame.destroy()

        self.reservation_frame = tk.Frame(self, bg=self.cget('bg'))
        self.reservation_frame.grid_rowconfigure(0, weight=1)
        self.reservation_frame.grid_columnconfigure(0, weight=1)

        UserDetailsCard(
            master=self.reservation_frame, name=self.name, cnp=self.CNP, enter_command=None
        ).grid(sticky='', row=0, column=0)

        self.reservation_frame.pack(fill=tk.BOTH, expand=1)


class ManageFrame(AppFrame):
    def __init__(self, db, master=None):
        super().__init__(master=master)
