import oracledb
from Hotel import Hotel


class Database:
    def __init__(self):
        self.connection = oracledb.connect(
            user='bd076', password='bd076', host='bd-dc.cs.tuiasi.ro', port=1539, service_name='orcl'
        )
        self.cursor = self.connection.cursor()

    def get_hotels_data(self):
        hotels = []
        for row in self.cursor.execute(
                'select id_hotel id, nume, nr_stele, cod_regiune, locatie, nr_telefon, email from hoteluri'
        ):
            hotels.append(Hotel(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        return hotels
