import tkinter as tk
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
    def __init__(self, name: tk.StringVar, cnp: tk.StringVar, enter_command, bg='white', fg='black', master=None):
        super().__init__(master, borderwidth=5, relief='solid', padx=5, pady=5, bg=bg)

        tk.Label(
            self, text='Nume', bg=bg, fg=fg, font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=5
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(
            self, text='CNP', bg=bg, fg=fg, font=('Times New Roman', 20), anchor='w', justify=tk.LEFT, width=5
        ).grid(row=1, column=0, padx=5, pady=5)

        name_fild = tk.Entry(self, textvariable=name)
        cnp_fild = tk.Entry(self, textvariable=cnp)

        name_fild.focus_set()

        name_fild.grid(row=0, column=1, padx=5, pady=5)
        cnp_fild.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            self, text='Introduce', command=enter_command, font=('American Typewriter', 20)
        ).grid(row=2, column=1, padx=5, pady=5)
