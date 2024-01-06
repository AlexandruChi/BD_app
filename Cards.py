import tkinter as tk
import tkcalendar
import pycountry
from Hotel import Hotel


class HotelCard(tk.Frame):
    def __init__(
            self, hotel: Hotel, option=None, option_colour=None, bg='white', fg='black', master=None
    ):
        super().__init__(master, borderwidth=5, relief='solid', padx=5, pady=5, bg=bg)

        hotel_details = tk.Frame(self, bg=bg)

        name_card = tk.Frame(hotel_details, bg=bg)
        flag = tk.Label(
            name_card, text=pycountry.subdivisions.get(code=hotel.region.strip()).country.flag,
            font=('Times New Roman', 25), bg=bg, fg=fg
        )
        name = tk.Label(name_card, text=hotel.name, font=('Times New Roman', 25), bg=bg, fg=fg)

        flag.pack(side=tk.LEFT)
        name.pack(side=tk.LEFT, padx=(0, 10))
        name_card.pack(fill=tk.X)

        location_card = tk.Frame(hotel_details, bg=bg)
        stars = tk.Label(
            location_card, text='★' * hotel.stars + '☆' * (5 - hotel.stars), font=('Times New Roman', 20),
            justify=tk.CENTER, width=10, anchor='w', bg=bg, fg=fg
        )
        stars.pack(side=tk.LEFT)

        subdivision = pycountry.subdivisions.get(code=hotel.region.strip())
        if subdivision is not None:
            location_string = subdivision.country.name
            parent = subdivision.parent
            parent_v = []
            while parent is not None:
                parent_v.append(parent.name)
                parent = parent.parent
            for subdivision_parent in reversed(parent_v):
                location_string += ', ' + subdivision_parent.name
            location_string += ', ' + subdivision.name
        else:
            location_string = hotel.region.strip()
        if hotel.location is not None:
            location_string += ', ' + hotel.location
        location = tk.Label(location_card, text=location_string, font=('Times New Roman', 20), bg=bg, fg=fg)
        location.pack(side=tk.LEFT)

        location_card.pack(fill=tk.X)
        hotel_details.pack(side=tk.LEFT, fill=tk.X)

        if option is not None:
            option_button = tk.Frame(self, width=10, bg=option_colour, borderwidth=1, relief='solid')
            tk.Button(
                option_button, text=option[0], font=('American Typewriter', 20), width=10, command=option[1]
            ).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            option_button.pack(side=tk.RIGHT, fill=tk.Y)

        if hotel.phone is not None or hotel.email is not None:
            contact_card = tk.Frame(self, bg=bg)
            if hotel.phone is not None:
                tk.Label(
                    contact_card, text='☏ ' + str(hotel.phone), font=('Times New Roman', 20),
                    bg=bg, fg=fg, anchor='w', justify=tk.LEFT, width=30
                ).pack(side=tk.BOTTOM, fill=tk.X)
            if hotel.email is not None:
                tk.Label(
                    contact_card, text='@ ' + str(hotel.email), font=('Times New Roman', 20),
                    bg=bg, fg=fg, anchor='w', justify=tk.LEFT, width=30
                ).pack(side=tk.BOTTOM, fill=tk.X)
            contact_card.pack(side=tk.RIGHT, fill=tk.Y)


class ScoreCard(tk.Frame):
    def __init__(self, score, nr_reviews, bg='white', fg='black', master=None):
        super().__init__(master, borderwidth=5, relief='solid', padx=5, pady=5, bg=bg)

        tk.Label(
            self, text=f'{(score * 2):.1f} / 10', font=('Charter', 30), bg=bg, fg=fg, width=10
        ).pack(fill=tk.X, pady=10)

        font = 'Charter'
        size = 20

        reviews_card = tk.Frame(self, bg=bg)
        for i in reversed(range(6)):
            card = tk.Frame(reviews_card, bg=bg)
            tk.Label(
                card, text='★' * i + '☆' * (5 - i) + ' ', font=(font, size), bg=bg, fg=fg, justify=tk.LEFT, anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X)
            tk.Label(
                card, text=nr_reviews[i], font=(font, size), justify=tk.RIGHT, bg=bg, fg=fg, anchor='w'
            ).pack(side=tk.RIGHT, fill=tk.X)
            card.pack(fill=tk.BOTH, expand=True)

        reviews_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))


class ReviewCard(tk.Frame):
    def __init__(self, reviews, bg='white', fg='black', master=None):
        super().__init__(master, borderwidth=5, relief='solid', padx=5, pady=5, bg=bg)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        reviews_frame = tk.Text(
            self, bg=bg, fg=fg, yscrollcommand=scrollbar.set, font=('American Typewriter', 15),
            width=0, height=0, wrap=tk.WORD
        )
        scrollbar.config(command=reviews_frame.yview)

        for review in reviews:
            reviews_frame.insert(
                tk.END, str(review[0]) + ' ' + '★' * review[1] + '☆' * (5 - review[1]) + ' ' +
                str(review[2]) + ':\n' + str(review[3]) + '\n\n'
            )

        reviews_frame.config(state="disabled")
        reviews_frame.focus_set()
        reviews_frame.pack(fill=tk.BOTH, expand=True)


class UserDetailsCard(tk.Frame):
    def __init__(self, name: tk.StringVar, cnp: tk.StringVar, enter_command, master=None, **kw):
        super().__init__(master)

        self.config(
            borderwidth=kw.get('borderwidth'), relief=kw.get('relief'), padx=kw.get('padx'), pady=kw.get('pady')
        )

        tk.Label(
            self, text='Nume', font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=5
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(
            self, text='CNP', font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=5
        ).grid(row=1, column=0, padx=5, pady=5)

        name_fild = tk.Entry(self, textvariable=name)
        cnp_fild = tk.Entry(self, textvariable=cnp)

        name_fild.focus_set()

        name_fild.grid(row=0, column=1, padx=5, pady=5)
        cnp_fild.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            self, text='Introduce', command=enter_command, font=('American Typewriter', 20)
        ).grid(row=2, column=1, padx=5, pady=5)


class SelectDateCard(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master)

        self.config(
            borderwidth=kw.get('borderwidth'), relief=kw.get('relief'), padx=kw.get('padx'), pady=kw.get('pady')
        )

        tk.Label(
            self, text='Check-in', font=('Times New Roman', 20)
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(
            self, text='Check-out', font=('Times New Roman', 20)
        ).grid(row=0, column=1, padx=5, pady=5)

        self.check_in_fild = tkcalendar.Calendar(self, selectmode="day")
        self.check_out_fild = tkcalendar.Calendar(self, selectmode="day")

        self.check_in_fild.grid(row=1, column=0, padx=5)
        self.check_out_fild.grid(row=1, column=1, padx=5)

        self.button = tk.Button(self, text='Introduce', font=('American Typewriter', 20))
        self.button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def set_enter_command(self, enter_command):
        self.button.configure(command=enter_command)

    def get_date(self):
        return self.check_in_fild.get_date(), self.check_out_fild.get_date()


class RoomsCard(tk.Frame):
    def __init__(self, rooms, nr_days, enter_command=None, select=False, master=None, **kw):
        super().__init__(master)

        self.config(
            borderwidth=kw.get('borderwidth'), relief=kw.get('relief'), padx=kw.get('padx'), pady=kw.get('pady')
        )

        tk.Label(
            self, text='Nr. dormitoare', font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=15
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(
            self, text='Nr. persoane', font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=15
        ).grid(row=1, column=0, padx=5, pady=5)
        tk.Label(
            self, text='Preț cameră', font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=15
        ).grid(row=2, column=0, padx=5, pady=5)
        if select:
            tk.Button(
                self, text='Introduce', font=('American Typewriter', 20), command=enter_command
            ).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        else:
            tk.Label(
                self, text='Nr. camere', font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=15
            ).grid(row=3, column=0, padx=5, pady=5)

        i = 0
        for room in rooms:
            for c in range(2):
                tk.Label(
                    self, text=str(room[c]), font=('Charter', 20), width=5
                ).grid(row=c, column=i + 1, padx=5, pady=5)
            tk.Label(
                self, text=str(room[2] * nr_days), font=('Charter', 20), width=5
            ).grid(row=2, column=i + 1, padx=5, pady=5)
            if select:
                options = []
                for val in range(room[3]):
                    options.append(str(val))
                tk.OptionMenu(
                    self, room[4], *options
                ).grid(row=3, column=i + 1, padx=5)
            else:
                tk.Label(
                    self, text=str(room[4].get()), font=('Charter', 20), width=5
                ).grid(row=3, column=i + 1, padx=5)
            i += 1


class ReservationCard(tk.Frame):
    def __init__(self, name, check_in, check_out, nr_days, rooms, buttons, master=None, **kw):
        super().__init__(master)

        self.config(
            borderwidth=kw.get('borderwidth'), relief=kw.get('relief'), padx=kw.get('padx'), pady=kw.get('pady')
        )

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        name_frame = tk.Frame(master=self, borderwidth=5, relief='groove', padx=5, pady=5)
        name_frame.rowconfigure(0, weight=1)
        name_frame.columnconfigure(0, weight=1)
        tk.Label(name_frame, text=name, font=('Snell Roundhand', 20)).grid(row=0, column=0, padx=5, pady=5, sticky='')
        name_frame.grid(row=0, column=0, padx=2.5, pady=2.5, sticky='nsew')

        date_frame = tk.Frame(master=self, borderwidth=5, relief='groove', padx=5, pady=5)
        date_frame.rowconfigure(0, weight=1)
        date_frame.rowconfigure(1, weight=1)
        date_frame.columnconfigure(0, weight=1)
        tk.Label(
            date_frame, text=check_in, font=('Charter', 20)
        ).grid(row=0, column=0, padx=5, pady=5, sticky='ews')
        tk.Label(
            date_frame, text=check_out, font=('Charter', 20)
        ).grid(row=1, column=0, padx=5, pady=5, sticky='ewn')
        date_frame.grid(row=1, column=0, padx=2.5, pady=2.5, sticky='nsew')

        rooms_frame = tk.Frame(master=self, borderwidth=5, relief='groove', padx=5, pady=5)
        rooms_frame.rowconfigure(0, weight=1)
        rooms_frame.columnconfigure(1, weight=1)
        RoomsCard(
            master=rooms_frame, nr_days=nr_days, rooms=rooms,
        ).grid(row=0, column=0, rowspan=2, columnspan=2, padx=5, pady=5, sticky='')
        rooms_frame.grid(row=0, column=1, rowspan=2, columnspan=2, padx=2.5, pady=2.5, sticky='nsew')

        options_frame = tk.Frame(master=self, borderwidth=5, relief='groove', padx=5, pady=5)
        i = 0
        for button in buttons:
            tk.Button(
                options_frame, text=button[0], command=button[1], font=('American Typewriter', 20)
            ).grid(row=0, column=i, sticky='w')
            i += 1
        options_frame.grid(row=2, column=0, columnspan=2, padx=2.5, pady=2.5, sticky='nsew')

        total = 0
        for room in rooms:
            total += room[2] * int(room[4].get()) * nr_days

        total_frame = tk.Frame(master=self, borderwidth=5, relief='groove', padx=5, pady=5)
        total_frame.rowconfigure(0, weight=1)
        total_frame.columnconfigure(0, weight=1)
        tk.Label(
            total_frame, text='Total: ' + str(total), font=('American Typewriter', 20)
        ).grid(row=0, column=0, padx=5, pady=5, sticky='')
        total_frame.grid(row=2, column=2, padx=2.5, pady=2.5, sticky='nsew')
