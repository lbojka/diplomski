# Diplomski rad - Luka Bojka
Razvijena aplikacija za potrebe diplomskog rada na temu 'Razvoj sustava preporuke sadržaja i personalizacije korisničkog sučelja web-aplikacije korištenjem metoda umjetne inteligencije'.

## Struktura
Aplikacija je napravljena u programskom jeziku Python, s naglaskom na biblioteku Streamlit.

Potrebno je preuzeti potrebne biblioteke unosom komande:
```
pip install -r requirements.txt
```

### Korisnici
Aplikacija trenutno ima 4 korisnika, u nastavku slijede podaci za korisničko ime i lozinku:
- lbojka - sifra123
- iivic - iivic123
- pperic - pperic123
- aanic - aanic123

### Dodavanje korisnika
Ako se želi dodati korisnik, potrebno ga je dodati u polja u sklopu _generator.py_ datoteke. Kada se doda, potrebno je pokrenuti datoteku i novi korisnik će biti dodan u _hashed_pw.pkl_ datoteku. Također, potrebno je novog korisnika dodati u _app.py_ (linije 107-108).

### Pokretanje aplikacije
Aplikacija se pokreće unosom komande:
```
streamlit run app.py
```

### Disclaimer
Dokument app.ipynb je tu za lakšu vizualizaciju podataka, nije zamišljen za pokretanje web aplikacije zbog kompatibilnosti sa Streamlit bibliotekom, za to služi app.py :) .
