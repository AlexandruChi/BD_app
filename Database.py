import oracledb
from Hotel import Hotel


class Database:
    def __init__(self, dsn):
        self.connection = oracledb.connect(dsn)
        self.cursor = self.connection.cursor()

    def get_sysdate(self):
        for row in self.cursor.execute(
            'select to_char(sysdate, \'dd.mm.yyyy\') from dual'
        ):
            return row[0]

    def get_hotels_data(self):
        hotels = []
        for row in self.cursor.execute(
            'select id_hotel, nume, nr_stele, cod_regiune, locatie, nr_telefon, email from hoteluri'
        ):
            hotels.append(Hotel(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        return hotels

    def get_hotel_score(self, hotel):
        for row in self.cursor.execute(
            'select avg(rc.scor) \
            from recenzii rc \
                join rezervari rz using (id_rezervare) \
                join camere_rezervate cr using (id_rezervare) \
                join camere ca using (id_camera) \
                join hoteluri ho using (id_hotel) \
                join clienti cl using (id_client) \
            where id_hotel = ' + str(hotel.ID)
        ):
            return row[0]

    def get_hotel_nr_reviews(self, hotel):
        nr_reviews = []
        for i in range(6):
            for row in self.cursor.execute(
                'select count(*) \
                from recenzii rc \
                    join rezervari rz using (id_rezervare) \
                    join camere_rezervate cr using (id_rezervare) \
                    join camere ca using (id_camera) \
                    join hoteluri ho using (id_hotel) \
                    join clienti cl using (id_client) \
                where id_hotel = ' + str(hotel.ID) + ' and scor = ' + str(i)
            ):
                nr_reviews.append(row[0])

        return nr_reviews

    def get_hotel_reviews_data(self, hotel):
        reviews = []
        for row in self.cursor.execute(
            'select to_char(data, \'dd.mm.yyyy\'), scor, nume, detalii \
            from ( \
                select distinct rc.data data, rc.scor scor, cl.nume nume, rc.detalii detalii \
                from recenzii rc \
                    join rezervari rz using (id_rezervare) \
                    join camere_rezervate cr using (id_rezervare) \
                    join camere ca using (id_camera) \
                    join hoteluri ho using (id_hotel) \
                    join clienti cl using (id_client) \
                where rc.detalii is not null and id_hotel = ' + str(hotel.ID) + ' \
            ) \
            order by data desc, scor desc, nume, detalii'
        ):
            reviews.append([row[0], row[1], row[2], row[3]])

        return reviews

    def get_user_name(self, cnp):
        for row in self.cursor.execute(
            'select nume \
            from clienti cl \
            where cl.cnp = ' + cnp
        ):
            if row is None:
                return False
            return row[0]

    def get_user_id(self, cnp):
        for row in self.cursor.execute(
            'select id_client \
            from clienti cl \
            where cl.cnp = ' + cnp
        ):
            return row[0]

    def add_user(self, name, cnp):
        self.cursor.execute('insert into clienti values (null, \'' + str(name) + '\', \'' + str(cnp) + '\')')

    def get_available_rooms(self, hotel, check_in, check_out):
        available_rooms = []
        for row in self.cursor.execute(
            'with \
                check_date as ( \
                    select \
                        to_date(\'' + check_in + '\', \'dd.mm.yyyy\') check_in, \
                        to_date(\'' + check_out + '\', \'dd.mm.yyyy\') check_out \
                    from dual \
                ), \
                camere_ocupate as ( \
                    select \
                        sum(nr_camere) nr, \
                        id_camera id \
                    from rezervari rz \
                        join camere_rezervate cr using (id_rezervare) \
                    where ( \
                        (select check_in from check_date) < \
                        (select check_out from check_date) \
                    ) and ( \
                        check_in < (select check_out from check_date) and \
                        (select check_in from check_date) < check_out \
                    ) \
                    group by id_camera \
                ) \
            select \
                ca.nr_dormitoare d, \
                ca.nr_persoane p, \
                ca.pret, \
                ca.nr_camere - NVL(( \
                    select nr from camere_ocupate where id = id_camera \
                ), 0) nr_c \
            from camere ca \
            where id_hotel = ' + str(hotel.ID)
        ):
            available_rooms.append([row[0], row[1], row[2], row[3]])

        return available_rooms

    def add_reservation(self, hotel, check_in, check_out, cnp, rooms):
        user_id = self.get_user_id(cnp)
        sysdate = self.get_sysdate()

        self.cursor.execute(
            'delete from rezervari \
            where id_rezervare = ( \
                select id_rezervare \
                from rezervari \
                    left join camere_rezervate using (id_rezervare) \
                where nr_camere is null and id_client = ' + str(user_id) + ' \
            )'
        )

        self.cursor.execute(
            'insert into rezervari values ( \
               null, to_date(\'' + sysdate + '\', \'dd.mm.yyyy\'), to_date(\'' + check_in + '\', \'dd.mm.yyyy\'), \
               to_date(\'' + check_out + '\', \'dd.mm.yyyy\'), ' + str(user_id) + '\
            )'
        )

        reservation_id = None
        for row in self.cursor.execute(
            'select rezervari_id_rezervare_seq.currval from dual'
        ):
            reservation_id = row[0]

        for room in rooms:
            if room[4] != 0:
                self.cursor.execute(
                    'insert into camere_rezervate values (' + str(reservation_id) + ', (\
                        select id_camera \
                        from camere \
                        where \
                            nr_dormitoare = ' + str(room[0]) + ' and \
                            nr_persoane = ' + str(room[1]) + ' and \
                            id_hotel = ' + str(hotel.ID) + ' \
                    ), ' + str(room[3]) + ')'
                )

        self.connection.commit()

        return reservation_id

    def get_reservations(self, hotel, user_id):
        reservations = []

        for row in self.cursor.execute(
            'select distinct id_rezervare \
            from rezervari rz \
                join camere_rezervate cz using (id_rezervare) \
                join camere ca using (id_camera) \
            where id_hotel = ' + str(hotel.ID) + ' and id_client = ' + str(user_id) + ' \
            order by id_rezervare desc'
        ):
            reservations.append(row[0])

        return reservations

    def get_reservation_data(self, reservation_id):
        reservation_data = []

        for row in self.cursor.execute(
            'select \
                to_char(check_in, \'dd.mm.yyyy\'), \
                to_char(check_out, \'dd.mm.yyyy\') \
            from rezervari rz \
            where id_rezervare = ' + str(reservation_id)
        ):
            reservation_data.append(row[0])
            reservation_data.append(row[1])

        for row in self.cursor.execute(
            'select \
                sum(ca.pret * cz.nr_camere * (rz.check_out - rz.check_in)) total \
            from camere_rezervate cz \
                join camere ca using (id_camera) \
                join rezervari rz using (id_rezervare) \
            where id_rezervare = ' + str(reservation_id)
        ):
            reservation_data.append(row[0])

        rooms = []
        for row in self.cursor.execute(
            'select \
                ca.nr_dormitoare, ca.nr_persoane, \
                ca.pret * (rz.check_out - rz.check_in) pret, \
                cz.nr_camere \
            from camere_rezervate cz \
                join camere ca using (id_camera) \
                join rezervari rz using (id_rezervare) \
            where id_rezervare = ' + str(reservation_id)
        ):
            rooms.append([row[0], row[1], row[2], row[3]])

        reservation_data.append(rooms)

        return reservation_data

    def get_review(self, reservation_id):
        review = None
        for row in self.cursor.execute(
            'select \
                scor, \
                detalii \
            from recenzii \
            where id_rezervare = ' + str(reservation_id)
        ):
            review = [row[0], row[1]]

        return review

    def add_review(self, reservation_id, review):
        sysdate = self.get_sysdate()
        review_string = 'null'
        if review[1] is not None:
            review_string = '\'' + review[1] + '\''

        self.cursor.execute(
            'insert into recenzii values( \
                ' + str(reservation_id) + ', ' + str(review[0]) + ', \
                            to_date(\'' + sysdate + '\', \'dd.mm.yyyy\'), ' + review_string + ' \
                        )'
        )
        self.connection.commit()

    def update_review(self, reservation_id, review):
        sysdate = self.get_sysdate()
        review_string = 'null'
        if review[1] is not None:
            review_string = '\'' + review[1] + '\''

        self.cursor.execute(
            'update recenzii \
            set \
                scor = ' + str(review[0]) + ', \
                data = to_date(\'' + sysdate + '\', \'dd.mm.yyyy\'), \
                detalii = ' + review_string + ' \
            where id_rezervare = ' + str(reservation_id)
        )
        self.connection.commit()

    def delete_review(self, reservation_id):
        self.cursor.execute(
            'delete from recenzii \
            where id_rezervare = ' + str(reservation_id)
        )
        self.connection.commit()
