class Hotel:
    def __init__(self, id_hotel, name, stars, score, region, location=None, phone=None, email=None):
        self.ID = id_hotel
        self.name = name
        self.stars = stars
        self.score = score
        self.region = region
        self.location = location
        self.phone = phone
        self.email = email
