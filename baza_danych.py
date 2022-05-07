import sqlite3

baza_danych = sqlite3.connect("Baza_danych.db")
print('Database opened')

baza_danych.execute(''' CREATE TABLE IF NOT EXISTS Uzytkownik(
    ID_Uzytkownika INTEGER PRIMARY KEY AUTOINCREMENT,
    Haslo TEXT NOT NULL,
    Imie TEXT NOT NULL,
    Nazwisko TEXT NOT NULL,
    Email TEXT NOT NULL,
    Numer_telefonu INT NOT NULL,
    Rodzaj_uzytkownika TEXT NOT NULL) ''')

print('Table created')

baza_danych.execute(''' INSERT INTO Uzytkownik(ID_Uzytkownika, Haslo, Imie, Nazwisko, Email, Numer_telefonu, Rodzaj_uzytkownika)
        VALUES
            (1, 'ania123', 'Anna', 'Annowicz', 'ania.annowicz@gmail.com', 123456789, 'Administrator'),
            (2,'GroszkowyKos231' ,'Remigiusz', 'Andrzejewski', 'remigiusz.andrzejewski@gmail.com', 654321597, 'Kierowca'),
            (3, 'OberzynowyLampart350','Diego', 'Kozłowski', 'deigo.kozlowski@gmail.com', 987365472, 'Kontroler' ),
            (4, 'MarchewkowaStonka049', 'Lila', "Gajewska", "lila.gajewska@gmail.com", 546782169, "Administrator"),
            (5, "LilaZaba778", "Konstancja", "Krupa", "konstancja.krupa@gmail.com", 6549826741, "Kierowca"),
            (6, "EozynaCzarniak374", "Balbina", "Jaworska", "balbina.jaworskaatgmail.com", 548314674, "Kontroler") ''')
        
baza_danych.commit()
print('REcord inserted')

cursor = baza_danych.execute("SELECT ID_Uzytkownika, Haslo, Imie, Nazwisko, Email, Numer_telefonu, Rodzaj_uzytkownika from Uzytkownik")
for row in cursor:
   print('ID_Uzytkownika =', row[0])
   print("Haslo = ", row[1])
   print("Imie = ", row[2])
   print("Nazwisko = ", row[3])
   print("Email = ", row[4])
   print("Numer_telefonu = ", row[5])
   print("Rodzaj_uzytkownika = ", row[6], "\n")

baza_danych.close()
print(' Database Closed')