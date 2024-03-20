delete recenzii;
delete camere_rezervate;
delete rezervari;
delete clienti;
delete camere;
delete hoteluri;

insert into hoteluri values(
    NULL, 'Galeria 18', 4, 'RO-SV', 
    'Crucea', '+40123456789', 'galeria18@gmail.com'
);
insert into camere values(NULL, 2, 1, 5, 200, hoteluri_id_hotel_seq.currval);
insert into camere values(NULL, 4, 2, 2, 300, hoteluri_id_hotel_seq.currval);

insert into hoteluri values(
    NULL, 'Arcadia Bay', 3, 'US-OR', 
    NULL, NULL, NULL
);
insert into camere values(NULL, 2, 1, 5, 300, hoteluri_id_hotel_seq.currval);
insert into camere values(NULL, 3, 1, 5, 350, hoteluri_id_hotel_seq.currval);
insert into camere values(NULL, 4, 2, 5, 400, hoteluri_id_hotel_seq.currval);

insert into hoteluri values(
    NULL, 'Amber Hotel', 4, 'DE-BY', 
    'Füssen', NULL, 'amberfuessen@gmail.com'
);
insert into camere values(NULL, 2, 1, 7, 350, hoteluri_id_hotel_seq.currval);

insert into hoteluri values(
    NULL, 'Emerald Bay', 3, 'RO-TL', 
    'Caraorman', '+40407123123', NULL
);
insert into camere values(NULL, 2, 1, 3, 300, hoteluri_id_hotel_seq.currval);
insert into camere values(NULL, 3, 1, 2, 350, hoteluri_id_hotel_seq.currval);

insert into hoteluri values(
    NULL, 'Wolfsrudel', 3, 'RO-SV', 
    NULL, '+40745337337', 'wolfsrudel@gmail.com'
);
insert into camere values(NULL, 2, 1, 5, 250, hoteluri_id_hotel_seq.currval);

insert into clienti values(NULL, 'Alexandru Chiriac', '5030416330276');
insert into rezervari values(
    NULL, '7.12.2023', '7.12.2023', '8.12.2023', 
    clienti_id_client_seq.currval
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 2 and
            nr_dormitoare = 1 and
            nume = 'Galeria 18'
    ),
    1
);
insert into recenzii values(
    rezervari_id_rezervare_seq.currval, 5, '8.12.2023', 
    NULL
);

insert into clienti values(NULL, 'Victoria von Braun', '6030508330458');
insert into rezervari values(
    NULL, '12.10.2023', '13.10.2023', '14.10.2023', 
    clienti_id_client_seq.currval
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 3 and
            nr_dormitoare = 1 and
            nume = 'Emerald Bay'
    ),
    1
);
insert into recenzii values(
    rezervari_id_rezervare_seq.currval, 2, '15.10.2023', 
    'La prima impresie petele și nuanțele camerei de hotel par a fi o componentă artistică, totuși la o mai atentă analiză a pereților se pot observa agenți biochimici care ar putea duce la o toxiinfecție alimetară doar privindu-le. Concluzie: Mai bine cu cortul.'
);

insert into rezervari values(
    NULL, '12.11.2023', '12.11.2023', '13.11.2023', 
    clienti_id_client_seq.currval
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 2 and
            nr_dormitoare = 1 and
            nume = 'Amber Hotel'
    ),
    2
);
insert into recenzii values(
    rezervari_id_rezervare_seq.currval, 3, '15.11.2023', 
    'Für den Preis war es ein gutes Hotel. Aber ich hoffe dass ich nie wieder einen Fuß hineinsetzen werde.'
);

insert into rezervari values(
    NULL, '13.12.2023', '17.12.2023', '20.12.2023', 
    clienti_id_client_seq.currval
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 2 and
            nr_dormitoare = 1 and
            nume = 'Arcadia Bay'
    ),
    2
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 3 and
            nr_dormitoare = 1 and
            nume = 'Arcadia Bay'
    ),
    2
);
insert into recenzii values(
    rezervari_id_rezervare_seq.currval, 3, '21.12.2023', 
    'Pro: priveliște minunată, izolare foarte bună. Con: Gândaci mai rău ca-n T19.'
);

insert into clienti values(NULL, 'Rachel Amber', '8940722330184');
insert into rezervari values(
    NULL, '18.11.2023', '18.11.2023', '20.11.2023', 
    clienti_id_client_seq.currval
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 2 and
            nr_dormitoare = 1 and
            nume = 'Arcadia Bay'
    ),
    2
);
insert into rezervari values(
    NULL, '12.12.2023', '12.12.2023', '14.12.2023', 
    clienti_id_client_seq.currval
);

insert into clienti values(NULL, 'Chloe Price', '8940411330193');
insert into rezervari values(
    NULL, '12.11.2023', '15.11.2023', '17.11.2023', 
    clienti_id_client_seq.currval
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 2 and
            nr_dormitoare = 1 and
            nume = 'Amber Hotel'
    ),
    2
);
insert into recenzii values(
    rezervari_id_rezervare_seq.currval, 5, '16.11.2023', 
    'Sehr herzlich und schön. beste Reise in die BUNDESREPUBLIK DEUTSCHLAND.'
);

insert into rezervari values(
    NULL, '13.12.2023', '14.12.2023', '15.12.2023', 
    clienti_id_client_seq.currval
);

insert into clienti values(NULL, 'Max Caulfield', '8950921330187');
insert into rezervari values(
    NULL, '10.12.2023', '11.12.2023', '13.12.2023', 
    clienti_id_client_seq.currval
);
insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 2 and
            nr_dormitoare = 1 and
            nume = 'Wolfsrudel'
    ),
    1
);
insert into recenzii values(
    rezervari_id_rezervare_seq.currval, 5, '12.12.2023', 
    'A wonderful experience. Best room service ever.'
);

insert into rezervari values(
    NULL, '11.12.2023', '11.12.2023', '13.12.2023', 
    clienti_id_client_seq.currval
);

insert into camere_rezervate values(
    rezervari_id_rezervare_seq.currval, (
        select id_camera
        from camere join hoteluri using(id_hotel)
        where 
            nr_persoane = 2 and
            nr_dormitoare = 1 and
            nume = 'Wolfsrudel'
    ),
    4
);

commit;