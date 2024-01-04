import tkinter as tk
import pycountry
from Hotel import Hotel


class HotelCard(tk.Frame):
    def __init__(self, hotel: Hotel, option, option_colour, bg='white', fg='black', master=None):
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

        stars.pack(side=tk.LEFT)
        location.pack(side=tk.LEFT)
        location_card.pack(fill=tk.X)

        hotel_details.pack(side=tk.LEFT, fill=tk.X)

        if option is not None:
            option_button = tk.Frame(self, width=10, bg=option_colour, borderwidth=1, relief='solid')
            tk.Button(
                option_button, text=option[0], font=('American Typewriter', 20), width=10, command=option[1]
            ).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            option_button.pack(side=tk.RIGHT, fill=tk.Y)


class ScoreCard(tk.Frame):
    def __init__(self, score, nr_reviews, bg='white', fg='black', master=None):
        super().__init__(master, borderwidth=5, relief='solid', padx=5, pady=5, bg=bg)

        tk.Label(
            self, text=f'{(score * 2):.1f} / 10', font=('Charter', 30), bg=bg, fg=fg, width=10
        ).pack(fill=tk.X, padx=10, pady=10)

        font = 'Charter'
        size = 20

        reviews_card = tk.Frame(self, bg=bg)
        tk.Label(reviews_card, bg=bg, fg=fg, text=f'★★★★★ → {nr_reviews[5]}', font=(font, size)).pack()
        tk.Label(reviews_card, bg=bg, fg=fg, text=f'★★★★☆ → {nr_reviews[4]}', font=(font, size)).pack()
        tk.Label(reviews_card, bg=bg, fg=fg, text=f'★★★☆☆ → {nr_reviews[3]}', font=(font, size)).pack()
        tk.Label(reviews_card, bg=bg, fg=fg, text=f'★★☆☆☆ → {nr_reviews[2]}', font=(font, size)).pack()
        tk.Label(reviews_card, bg=bg, fg=fg, text=f'★☆☆☆☆ → {nr_reviews[1]}', font=(font, size)).pack()
        tk.Label(reviews_card, bg=bg, fg=fg, text=f'☆☆☆☆☆ → {nr_reviews[0]}', font=(font, size)).pack()
        reviews_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))


class ReviewCard(tk.Frame):
    def __init__(self, bg='white', fg='black', master=None):
        super().__init__(master, borderwidth=5, relief='solid', padx=5, pady=5, bg=bg)

