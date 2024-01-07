import tkinter as tk
import oracledb

from Cards import (HotelCard, ScoreCard, ReviewCard, UserDetailsCard, SelectDateCard, RoomsCard, ReservationCard,
                   MessageCard, SelectReservationCard)
from NavBar import NavBar
from datetime import datetime, timedelta

DATE_FORMAT = "%d.%m.%Y"


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
        self.frame = None

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def load_frame(self):
        if self.frame is not None:
            self.frame.destroy()

        self.frame = tk.Frame(self, bg=self.cget('bg'))
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def pack_frame(self):
        self.frame.pack(fill=tk.BOTH, expand=1)


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
        self.hotel = None
        self.rooms = None
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

        select_date = SelectDateCard(master=self.frame, borderwidth=5, relief='solid', padx=5, pady=5)
        select_date.set_enter_command(lambda: self.check_date(select_date.get_date()))
        select_date.grid(sticky='', row=0, column=0)

        self.pack_frame()

    def check_date(self, date):
        self.check_in = datetime.strptime(date[0], DATE_FORMAT).date()
        self.check_out = datetime.strptime(date[1], DATE_FORMAT).date()

        if self.check_in >= self.check_out:
            self.enter_date()
            return

        sysdate = datetime.strptime(self.db.get_sysdate(), DATE_FORMAT).date()

        if sysdate > self.check_in + timedelta(days=1):
            self.enter_date()
            return

        self.select_rooms()

    def select_rooms(self):
        self.load_frame()

        self.rooms = self.db.get_available_rooms(
            self.hotel, self.check_in.strftime(DATE_FORMAT), self.check_out.strftime(DATE_FORMAT)
        )
        for room in self.rooms:
            room.append(tk.StringVar())
            room[-1].set(str(0))

        RoomsCard(
            master=self.frame, rooms=self.rooms, select=True,
            nr_days=(self.check_out - self.check_in).days,
            enter_command=lambda: self.check_rooms(),
            borderwidth=5, relief='solid', padx=5, pady=5
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def check_rooms(self):
        for room in self.rooms:
            if int(room[4].get()) != 0:
                self.enter_user_details()
                return

        self.select_rooms()

    def enter_user_details(self):
        self.load_frame()

        UserDetailsCard(
            master=self.frame, name=self.name, cnp=self.CNP, enter_command=lambda: self.check_user_details(),
            borderwidth=5, relief='solid', padx=5, pady=5
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

        self.show_reservation()

    def show_reservation(self):
        self.load_frame()

        for room in self.rooms:
            room[3] = int(room[4].get())

        ReservationCard(
            master=self.frame, check_in=self.check_in.strftime(DATE_FORMAT),
            check_out=self.check_out.strftime(DATE_FORMAT),
            nr_days=(self.check_out - self.check_in).days, rooms=self.rooms, name=self.name.get(),
            buttons=[('Rezervă', lambda: self.confirm_reservation())],
            borderwidth=5, relief='solid', padx=5, pady=5
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def confirm_reservation(self):
        for room in self.rooms:
            room[4] = int(room[4].get())

        reservation_id = None
        try:
            reservation_id = self.db.add_reservation(
                hotel=self.hotel, check_in=self.check_in.strftime(DATE_FORMAT),
                check_out=self.check_out.strftime(DATE_FORMAT), cnp=self.CNP.get(), rooms=self.rooms
            )
        except oracledb.Error:
            self.error()

        self.succes(reservation_id)

    def succes(self, reservation_id):
        self.clear()
        HotelCard(
            self.hotel, ('Înapoi', lambda: self.select_hotel()), 'gold', master=self
        ).pack(fill=tk.X)
        self.load_frame()

        MessageCard(
            master=self.frame, message='Rezervare ' + str(reservation_id) + ' creată',
            button=('OK', lambda: self.select_hotel()),
            borderwidth=5, relief='solid', padx=5, pady=5
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def error(self):
        self.load_frame()

        MessageCard(
            master=self.frame, message='Eroare', button=None,
            borderwidth=5, relief='solid', padx=5, pady=5
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()


class ManageFrame(AppFrame):
    def __init__(self, db, master=None):
        super().__init__(master=master)
        self.db = db
        self.name = tk.StringVar()
        self.CNP = tk.StringVar()
        self.reservation_id = tk.StringVar()
        self.reservations = None
        self.hotel = None
        self.select_hotel()

    def select_hotel(self):
        self.clear()
        self.hotel = None
        hotels = self.db.get_hotels_data()
        for i in range(len(hotels)):
            HotelCard(
                hotels[i], ('Rezervări', lambda val=i: self.get_reservation(hotels[val])),
                'green', master=self
            ).pack(pady=(int(i != 0) * 10, 0), fill=tk.X)

    def get_reservation(self, hotel):
        self.clear()
        self.hotel = hotel
        HotelCard(
            self.hotel, ('Înapoi', lambda: self.select_hotel()), 'gold', master=self
        ).pack(fill=tk.X)

        self.enter_user_details()

    def enter_user_details(self):
        self.load_frame()

        UserDetailsCard(
            master=self.frame, name=self.name, cnp=self.CNP, enter_command=lambda: self.check_user_details(),
            borderwidth=5, relief='solid', padx=5, pady=5
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def check_user_details(self):
        if len(self.CNP.get()) != 13 or not len(self.name.get()):
            self.enter_user_details()
            return

        name = self.db.get_user_name(self.CNP.get())

        if self.name.get() != name:
            self.enter_user_details()
            return

        self.reservations = self.db.get_reservations(self.hotel, self.db.get_user_id(self.CNP.get()))



        self.select_reservation()

    def select_reservation(self):
        self.load_frame()

        self.reservation_id = tk.StringVar()

        SelectReservationCard(
            master=self.frame, reservation_ids=self.reservations, selected=self.reservation_id,
            button=('Selectare', lambda: self.check_reservations()),
            borderwidth=5, relief='solid', padx=5, pady=5
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def check_reservations(self):
        val = self.reservation_id.get()
        if val != '':
            self.show_reservation()

    def show_reservation(self):
        self.load_frame()

        reservation_data = self.db.get_reservation_data(self.reservation_id.get())

        sysdate = datetime.strptime(self.db.get_sysdate(), DATE_FORMAT).date()
        check_in = datetime.strptime(reservation_data[0], DATE_FORMAT).date()
        check_out = datetime.strptime(reservation_data[1], DATE_FORMAT).date()

        buttons = []

        if check_in <= sysdate <= check_out + timedelta(days=7):
            buttons.append(('Recenzie', lambda: self.add_review()))

        ReservationCard(
            master=self.frame, check_in=reservation_data[0],
            check_out=reservation_data[1],
            nr_days=(
                    check_out - check_in
            ).days, rooms=reservation_data[3], name=self.name.get(), total=reservation_data[2],
            buttons=buttons, select=False,
            borderwidth=5, relief='solid', padx=5, pady=5
        ).grid(sticky='', row=0, column=0)

        self.pack_frame()

    def add_review(self):
        pass
