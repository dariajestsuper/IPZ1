import os, sqlite3
from flask import Flask, config, render_template, url_for, request
app = Flask(__name__, template_folder='templates')


@app.route('/')
def Strona_glowna():
    return render_template('homepage.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        try:
            ID_Uzytkownika = request.form['ID_Uzytkownika']
            Haslo = request.form['Haslo']

            with sqlite3.connect('Baza_danych.db') as con:
                cur = con.cursor()

                if (cur.execute("SELECT Haslo FROM Uzytkownik WHERE ID_Uzytkownika= ?", [ID_Uzytkownika]).fetchone()[0] == Haslo):
                    if(cur.execute("SELECT Rodzaj_uzytkownika FROM Uzytkownik WHERE ID_Uzytkownika= ?", [ID_Uzytkownika]).fetchone()[0] == 'Administrator'):
                        return render_template('admin.html')
                    elif(cur.execute("SELECT Rodzaj_uzytkownika FROM Uzytkownik WHERE ID_Uzytkownika= ?", [ID_Uzytkownika]).fetchone()[0] == 'Kierowca'):
                        return render_template('kierowca.html')
                    elif(cur.execute("SELECT Rodzaj_uzytkownika FROM Uzytkownik WHERE ID_Uzytkownika= ?", [ID_Uzytkownika]).fetchone()[0] == 'Kontroler'):
                        return render_template('kontroler.html')
                    else:
                        return render_template('homepage.html')

        except:
            sqlite3.connect('Baza_danych.db').rollback()
        
        finally:
            sqlite3.connect('Baza_danych.db').close()
    return render_template('login.html')

    
if __name__ == '__main__':
    app.run(debug = True)
