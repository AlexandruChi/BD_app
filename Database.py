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
            reviews.append((row[0], row[1], row[2], row[3]))

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
            'select nume \
            from clienti cl \
            where cl.cnp = ' + cnp
        ):
            return row[0]

    def add_user(self, name, cnp):
        self.cursor.execute('insert into clienti values (NULL, \'' + str(name) + '\', \'' + str(cnp) + '\')')
        self.connection.commit()

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
                ca.nr_persoane p, \
                ca.nr_dormitoare d, \
                ca.pret, \
                ca.nr_camere - NVL(( \
                    select nr from camere_ocupate where id = id_camera \
                ), 0) nr_c \
            from camere ca \
            where id_hotel = ' + str(hotel.ID)
        ):
            available_rooms.append((row[0], row[1], row[2], row[3]))

        return available_rooms
