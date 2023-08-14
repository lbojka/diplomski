from pathlib import Path
import pickle

import streamlit_authenticator as stauth

imena = ["Luka Bojka", "Ivo Ivic", "Pero Peric, Ana Anic"]
korImena = ["lbojka", "iivic", "pperic,", "aanic"]
lozinke = ["sifra123", "iivic123", "pperic123", "aanic123"]

hashed_password = stauth.Hasher(lozinke).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_password, file)
