-- Generated by Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   at:        2024-01-07 00:59:38 EET
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



DROP TABLE camere CASCADE CONSTRAINTS;

DROP TABLE camere_rezervate CASCADE CONSTRAINTS;

DROP TABLE clienti CASCADE CONSTRAINTS;

DROP TABLE hoteluri CASCADE CONSTRAINTS;

DROP TABLE recenzii CASCADE CONSTRAINTS;

DROP TABLE rezervari CASCADE CONSTRAINTS;

-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE camere (
    id_camera     NUMBER(5) NOT NULL,
    nr_persoane   NUMBER(1) NOT NULL,
    nr_dormitoare NUMBER(1) NOT NULL,
    nr_camere     NUMBER(3) NOT NULL,
    pret          NUMBER(4) NOT NULL,
    id_hotel      NUMBER(3) NOT NULL
)
LOGGING;

ALTER TABLE camere ADD CONSTRAINT camera_nr_persoane_ck CHECK ( nr_persoane > 0 );

ALTER TABLE camere ADD CONSTRAINT camera_nr_dormitoare_ck CHECK ( nr_dormitoare > 0 );

ALTER TABLE camere ADD CONSTRAINT camera_nr_camere_ck CHECK ( nr_camere > 0 );

ALTER TABLE camere ADD CONSTRAINT camera_pret_ck CHECK ( pret > 0 );

ALTER TABLE camere ADD CONSTRAINT camere_pk PRIMARY KEY ( id_camera );

ALTER TABLE camere
    ADD CONSTRAINT camere_un UNIQUE ( nr_persoane,
                                      nr_dormitoare,
                                      id_hotel );

CREATE TABLE camere_rezervate (
    id_rezervare NUMBER(8) NOT NULL,
    id_camera    NUMBER(5) NOT NULL,
    nr_camere    NUMBER(1) NOT NULL
)
LOGGING;

ALTER TABLE camere_rezervate ADD CONSTRAINT camere_rezervate_ck CHECK ( nr_camere > 0 );

ALTER TABLE camere_rezervate ADD CONSTRAINT camere_rezervate_pk PRIMARY KEY ( id_rezervare,
                                                                              id_camera );

CREATE TABLE clienti (
    id_client NUMBER(7) NOT NULL,
    nume      VARCHAR2(30) NOT NULL,
    cnp       VARCHAR2(13) NOT NULL
)
LOGGING;

ALTER TABLE clienti
    ADD CONSTRAINT client_nume_ck CHECK ( length(nume) > 0 );

ALTER TABLE clienti
    ADD CONSTRAINT client_cnp_ck CHECK ( length(cnp) = 13 );

ALTER TABLE clienti ADD CONSTRAINT clienti_pk PRIMARY KEY ( id_client );

ALTER TABLE clienti ADD CONSTRAINT clienti_cnp_un UNIQUE ( cnp );

CREATE TABLE hoteluri (
    id_hotel    NUMBER(3) NOT NULL,
    nume        VARCHAR2(30) NOT NULL,
    nr_stele    NUMBER(1) NOT NULL,
    cod_regiune CHAR(6) NOT NULL,
    locatie     VARCHAR2(30),
    nr_telefon  VARCHAR2(15),
    email       VARCHAR2(30)
)
LOGGING;

ALTER TABLE hoteluri
    ADD CONSTRAINT hotel_nume_ck CHECK ( length(nume) > 0 );

ALTER TABLE hoteluri
    ADD CONSTRAINT hotel_nr_stele_ck CHECK ( nr_stele BETWEEN 1 AND 5 );

ALTER TABLE hoteluri
    ADD CONSTRAINT hotel_email_ck CHECK ( REGEXP_LIKE ( email,
                                                        '[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}' ) );

ALTER TABLE hoteluri ADD CONSTRAINT hoteluri_pk PRIMARY KEY ( id_hotel );

ALTER TABLE hoteluri ADD CONSTRAINT hoteluri_nr_telefon_un UNIQUE ( nr_telefon );

ALTER TABLE hoteluri ADD CONSTRAINT hoteluri_email_un UNIQUE ( email );

ALTER TABLE hoteluri ADD CONSTRAINT hoteluri_nume_un UNIQUE ( nume );

CREATE TABLE recenzii (
    id_rezervare NUMBER(8) NOT NULL,
    scor         NUMBER(1) NOT NULL,
    data         DATE NOT NULL,
    detalii      VARCHAR2(300)
)
LOGGING;

ALTER TABLE recenzii
    ADD CONSTRAINT recenzie_scor_ck CHECK ( scor BETWEEN 0 AND 5 );

ALTER TABLE recenzii
    ADD CONSTRAINT recenzi_detalii_ck CHECK ( length(detalii) > 0 );

ALTER TABLE recenzii ADD CONSTRAINT recenzii_pk PRIMARY KEY ( id_rezervare );

CREATE TABLE rezervari (
    id_rezervare NUMBER(8) NOT NULL,
    data_creare  DATE NOT NULL,
    check_in     DATE NOT NULL,
    check_out    DATE NOT NULL,
    id_client    NUMBER(7) NOT NULL
)
LOGGING;

ALTER TABLE rezervari
    ADD CONSTRAINT rezervare_data_creare_ck CHECK ( data_creare <= check_in + 1 );

ALTER TABLE rezervari ADD CONSTRAINT rezervare_check_in_ck CHECK ( check_in < check_out );

ALTER TABLE rezervari ADD CONSTRAINT rezervare_check_out_ck CHECK ( check_out > check_in );

ALTER TABLE rezervari ADD CONSTRAINT rezervari_pk PRIMARY KEY ( id_rezervare );

ALTER TABLE camere
    ADD CONSTRAINT camere_hoteluri_fk FOREIGN KEY ( id_hotel )
        REFERENCES hoteluri ( id_hotel )
    NOT DEFERRABLE;

ALTER TABLE camere_rezervate
    ADD CONSTRAINT camere_rezervate_camere_fk FOREIGN KEY ( id_camera )
        REFERENCES camere ( id_camera )
    NOT DEFERRABLE;

ALTER TABLE camere_rezervate
    ADD CONSTRAINT camere_rezervate_rezervari_fk FOREIGN KEY ( id_rezervare )
        REFERENCES rezervari ( id_rezervare )
    NOT DEFERRABLE;

ALTER TABLE recenzii
    ADD CONSTRAINT recenzii_rezervari_fk FOREIGN KEY ( id_rezervare )
        REFERENCES rezervari ( id_rezervare )
    NOT DEFERRABLE;

ALTER TABLE rezervari
    ADD CONSTRAINT rezervari_clienti_fk FOREIGN KEY ( id_client )
        REFERENCES clienti ( id_client )
    NOT DEFERRABLE;

CREATE OR REPLACE TRIGGER tgr_ck_camere_briu 
    BEFORE INSERT OR UPDATE ON Camere_rezervate 
    FOR EACH ROW 
DECLARE
avalible_rooms NUMERIC;
BEGIN
with  
    camere_ocupate as (
        select 
            sum(nr_camere) nr,
            id_camera id
        from rezervari rz
            join camere_rezervate cr using (id_rezervare)
        where
            check_in < (
                select check_out 
                from rezervari 
                where id_rezervare = :new.id_rezervare
            ) and (
                select check_in
                from rezervari 
                where id_rezervare = :new.id_rezervare
            ) < check_out
        group by id_camera
    )
select 
    nr_camere - NVL((
        select nr from camere_ocupate where id = id_camera
    ), 0)
into avalible_rooms
from camere
where id_camera = :new.id_camera;
IF (avalible_rooms < :new.nr_camere)
THEN
RAISE_APPLICATION_ERROR( -20001, 
	'Numarul maxim de camere disponibile: ' || avalible_rooms
);
END IF;
END; 
/

CREATE OR REPLACE TRIGGER trg_camere_rezervate_briu 
    BEFORE INSERT OR UPDATE ON Camere_rezervate 
    FOR EACH ROW 
DECLARE
nrRows NUMERIC;
v_hotel camere.id_hotel%TYPE;
v_hotel_new camere.id_hotel%TYPE;
BEGIN
SELECT count(*) INTO nrRows FROM camere_rezervate WHERE id_rezervare = :new.id_rezervare; 
IF( nrRows != 0 )
THEN
SELECT DISTINCT id_hotel INTO v_hotel FROM camere_rezervate JOIN camere USING (id_camera) WHERE id_rezervare = :new.id_rezervare;
SELECT id_hotel INTO v_hotel_new FROM camere WHERE id_camera = :new.id_camera;
IF( v_hotel != v_hotel_new )
THEN
RAISE_APPLICATION_ERROR( -20001, 
	'Pot fi adaugate doar camere de la hotelul cu id-ul: ' || v_hotel
);
END IF;
END IF;
END; 
/

CREATE OR REPLACE TRIGGER trg_recenzii_briu 
    BEFORE INSERT OR UPDATE ON Recenzii 
    FOR EACH ROW 
DECLARE
nr_zile CONSTANT NUMERIC := 7;
nrRows NUMERIC;
v_check_in rezervari.check_in%TYPE;
v_check_out rezervari.check_out%TYPE;
BEGIN
SELECT check_in INTO v_check_in FROM rezervari WHERE ID_rezervare = :new.ID_rezervare;
SELECT check_out INTO v_check_out FROM rezervari WHERE ID_rezervare = :new.ID_rezervare;
SELECT COUNT(*) INTO nrRows FROM camere_rezervate WHERE ID_rezervare = :new.ID_rezervare;
IF( nrRows = 0 )
THEN
RAISE_APPLICATION_ERROR( -20001, 
	'Rezervare incompleta' 
);
END IF;
IF( :new.data <  v_check_in )
THEN
RAISE_APPLICATION_ERROR( -20001, 
	'Data invalida: ' || TO_CHAR( :new.data, 'DD.MM.YYYY' ) || ' trebuie sa fie mai mare sau egal cu data check-in.' 
);
END IF;
IF( :new.data > v_check_out + nr_zile )
THEN
RAISE_APPLICATION_ERROR( -20001, 
	'Data invalida: ' || TO_CHAR( :new.data, 'DD.MM.YYYY' ) || ' trebuie sa fie mai mica decat data ' || TO_CHAR( v_check_out + nr_zile + 1, 'DD.MM.YYYY' ) || '.'
);
END IF;
END; 
/

CREATE OR REPLACE TRIGGER trg_rezervari_briu 
    BEFORE INSERT OR UPDATE ON Rezervari 
    FOR EACH ROW 
DECLARE
nrRows NUMERIC;
BEGIN
SELECT count(*) INTO nrRows FROM rezervari LEFT JOIN camere_rezervate USING (id_rezervare) WHERE id_camera IS NULL AND id_client = :new.id_client; 
IF( nrRows != 0 )
THEN
RAISE_APPLICATION_ERROR( -20001, 
	'Rezervare incompletă existentă pentru client'
);
END IF;
END; 
/

CREATE SEQUENCE camere_id_camera_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER camere_id_camera_trg BEFORE
    INSERT ON camere
    FOR EACH ROW
    WHEN ( new.id_camera IS NULL )
BEGIN
    :new.id_camera := camere_id_camera_seq.nextval;
END;
/

CREATE SEQUENCE clienti_id_client_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER clienti_id_client_trg BEFORE
    INSERT ON clienti
    FOR EACH ROW
    WHEN ( new.id_client IS NULL )
BEGIN
    :new.id_client := clienti_id_client_seq.nextval;
END;
/

CREATE SEQUENCE hoteluri_id_hotel_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER hoteluri_id_hotel_trg BEFORE
    INSERT ON hoteluri
    FOR EACH ROW
    WHEN ( new.id_hotel IS NULL )
BEGIN
    :new.id_hotel := hoteluri_id_hotel_seq.nextval;
END;
/

CREATE SEQUENCE rezervari_id_rezervare_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER rezervari_id_rezervare_trg BEFORE
    INSERT ON rezervari
    FOR EACH ROW
    WHEN ( new.id_rezervare IS NULL )
BEGIN
    :new.id_rezervare := rezervari_id_rezervare_seq.nextval;
END;
/



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             0
-- ALTER TABLE                             31
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           8
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          4
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
