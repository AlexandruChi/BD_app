import tkinter as tk
from Cards import HotelCard, ScoreCard, ReviewCard, UserDetailsCard, SelectDateCard, SelectRoomsCard
from NavBar import NavBar
from datetime import datetime


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
        self.check_in = None
        self.check_out = None
        self.nr_days = None
        self.hotel = None
        self.frame = None
        self.select_hotel()

    def select_hotel(self):
        self.clear()
        self.hotel = None
        hotels = self.db.get_hotels_data()
        for i in range(len(hotels)):
            HotelCard(
                hotels[i], ('Rezervă', lambda val=i: self.create_reservation(hotels[val])),
                'green', master=self
            ).pack(pady=(int(i != 0) * 10, 0), fill=tk.X)

    def create_reservation(self, hotel):
        self.clear()
        self.hotel = hotel
        HotelCard(
            self.hotel, ('Anulare', lambda: self.select_hotel()), 'red', master=self
        ).pack(fill=tk.X)

        self.enter_date()

    def enter_date(self):
        self.load_frame()

        select_date = SelectDateCard(master=self.frame)
        select_date.set_enter_command(lambda: self.check_date(select_date.get_date()))
        select_date.grid(sticky='', row=0, column=0)

        self.pack_frame()

    def check_date(self, date):
        date_format = "%d.%m.%Y"
        check_in = datetime.strptime(date[0], date_format).date()
        check_out = datetime.strptime(date[1], date_format).date()

        if check_in >= check_out:
            self.enter_date()
            return

        sysdate = datetime.strptime(self.db.get_sysdate(), date_format).date()

        if sysdate > check_in:
            self.enter_date()
            return

        self.nr_days = (check_out - check_in).days

        self.check_in = date[0]
        self.check_out = date[1]

        self.select_rooms()

    def select_rooms(self):
        self.load_frame()

        SelectRoomsCard(
            master=self.frame, rooms=self.db.get_available_rooms(self.hotel, self.check_in, self.check_out),
            nr_days=self.nr_days
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def enter_user_details(self):
        self.load_frame()

        UserDetailsCard(
            master=self.frame, name=self.name, cnp=self.CNP, enter_command=lambda: self.check_user_details()
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def check_user_details(self):
        if len(self.CNP.get()) != 13 or not len(self.name.get()):
            self.enter_user_details()
            return

        name = self.db.get_user_name(self.CNP.get())

        if name is None:
            self.db.add_user(self.name.get(), self.CNP.get())
        elif self.name.get() != name:
            self.enter_user_details()
            return

        self.enter_date()

    def load_frame(self):
        if self.frame is not None:
            self.frame.destroy()

        self.frame = tk.Frame(self, bg=self.cget('bg'))
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def pack_frame(self):
        self.frame.pack(fill=tk.BOTH, expand=1)


class ManageFrame(AppFrame):
    def __init__(self, db, master=None):
        super().__init__(master=master)
