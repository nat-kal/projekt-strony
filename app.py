from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
MAGAZYN = {}
SALDO = 0
HISTORIA_FILE = "historia.txt"

# Wczytanie historii z pliku
def zapisz_do_historii(tekst):
    with open(HISTORIA_FILE, "a", encoding="utf-8") as f:
        f.write(tekst + "\n")

@app.route("/", methods=["GET", "POST"])
def index():
    global SALDO, MAGAZYN

    if request.method == "POST":
        if "zmiana_salda" in request.form:
            komentarz = request.form["komentarz"]
            wartosc = int(request.form["wartosc"])
            SALDO += wartosc
            zapisz_do_historii(f"ZMIANA SALDA: {komentarz}, {wartosc} zł")

        elif "zakup" in request.form:
            nazwa = request.form["nazwa"]
            cena = int(request.form["cena"])
            ilosc = int(request.form["ilosc"])
            koszt = cena * ilosc
            if SALDO >= koszt:
                SALDO -= koszt
                MAGAZYN[nazwa] = MAGAZYN.get(nazwa, 0) + ilosc
                zapisz_do_historii(f"ZAKUP: {nazwa}, {cena} zł x {ilosc}")
            else:
                return "Za mało środków na zakup."

        elif "sprzedaz" in request.form:
            nazwa = request.form["nazwa"]
            cena = int(request.form["cena"])
            ilosc = int(request.form["ilosc"])
            if MAGAZYN.get(nazwa, 0) >= ilosc:
                SALDO += cena * ilosc
                MAGAZYN[nazwa] -= ilosc
                zapisz_do_historii(f"SPRZEDAŻ: {nazwa}, {cena} zł x {ilosc}")
            else:
                return "Brak produktu w magazynie."

    return render_template("index.html", saldo=SALDO, magazyn=MAGAZYN)

@app.route("/historia/")
@app.route("/historia/<int:start>/<int:end>/")
def historia(start=None, end=None):
    if not os.path.exists(HISTORIA_FILE):
        historia = []
    else:
        with open(HISTORIA_FILE, "r", encoding="utf-8") as f:
            linie = f.readlines()

    liczba_linii = len(linie)

    if start is None or end is None:
        zakres = linie
    elif start < 0 or end > liczba_linii or start > end:
        zakres = []
        komunikat = f"Błędny zakres. Wybierz od 0 do {liczba_linii - 1}."
        return render_template("historia.html", historia=zakres, liczba_linii=liczba_linii, komunikat=komunikat)
    else:
        zakres = linie[start:end]

    return render_template("historia.html", historia=zakres, liczba_linii=liczba_linii)

if __name__ == "__main__":
    app.run(debug=True)
