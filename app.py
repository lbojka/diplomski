import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

netflix_data = pd.read_csv("netflix_titles.csv")


tfidf = TfidfVectorizer(
    stop_words="english"
)  # lista uobicajenih rijeci kao "and, the, of, a..."
netflix_data["description"] = netflix_data["description"].fillna(
    ""
)  # mijenja null vrijednosti s ''
tfidf_matrix = tfidf.fit_transform(
    netflix_data["description"]
)  # Transformira podatke u podatke koje ML može čitati

from sklearn.metrics.pairwise import linear_kernel

cosine_sim = linear_kernel(
    tfidf_matrix, tfidf_matrix
)  # izračunava kosinus slicnost tako da odvaja podatke s linijama i tako ih grupira prema njihovim svojstvima

indices = pd.Series(
    netflix_data.index, index=netflix_data["title"]
).drop_duplicates()  # uklanja duplikate po Naslovu


def dohvati_preporuke(naslov, cosine_sim=cosine_sim):
    idx = indices[naslov]
    sim_scores = list(
        enumerate(cosine_sim[idx])
    )  # Dohvaca rezultate parova sličnosti svih filmova s ​​tim filmom
    sim_scores = sorted(
        sim_scores, key=lambda x: x[1], reverse=True
    )  # Sortira filmove prema parovima sličnosti
    sim_scores = sim_scores[1:11]  # dohvaća rezultate 10 najsličnijih filmova
    movie_indices = [i[0] for i in sim_scores]  # dohvaća filmske indekse
    return netflix_data.iloc[movie_indices]  # vraća top 10 najsličnijih filmova


from movieposters import get_poster, errors


def prikazi_filmske_postere(df):
    naslovi_filmova = df["title"].tolist()

    stupci = 3

    cols = st.columns(stupci)

    # Iterate over the movie titles and display their posters in the grid
    for index, film in enumerate(naslovi_filmova):
        try:
            # Fetch the poster URL for the movie
            poster_url = get_poster(film)

            cols[index % stupci].image(
                poster_url,
                caption=film,
                width=150,
            )
        except (errors.PosterNotFound, errors.MovieNotFound):
            cols[index % stupci].image("movieThumbnail.png", caption=film, width=150)


def nasumicni_filmovi_zanra(zanr):
    # Filtrira DataFrame prema danom zanru
    filtrirani_podaci = netflix_data[
        netflix_data["listed_in"].str.contains(zanr, case=False, na=False)
    ]

    # Ako postoji manje filmova od broja trazenih, vrati ih sve
    if len(filtrirani_podaci) < 6:
        return filtrirani_podaci["title"].tolist()

    # Nasumicno odabire 6 filmova i vraca njihove naslove
    return filtrirani_podaci.sample(n=6)["title"].tolist()


lista_naslova = netflix_data["title"].values
naslov_zanr = {}
for naslov, zanrovi in zip(netflix_data["title"], netflix_data["listed_in"]):
    naslov_zanr[naslov] = [zanr.strip() for zanr in zanrovi.split(",")]


####################################################################
# streamlit
####################################################################
import streamlit as st

# Konfiguracija aplikacije - ikona i tekst taba, About sekcija u meniju
st.set_page_config(
    page_title="Diplomski rad - Luka Bojka",
    page_icon="🎞️",
    menu_items={
        "About": "# Sustav preporuke filmova.\n"
        "Web-aplikacija napravljena za potrebe diplomskog rada na temu 'Razvoj sustava preporuke sadržaja i personalizacije korisničkog sučelja web-aplikacije korištenjem metoda umjetne inteligencije'."
    },
)

# --- User authentication ---
import streamlit as st
from pathlib import Path
import pickle
import streamlit_authenticator as stauth

imena = ["Luka Bojka", "Ivo Ivic", "Pero Peric", "Ana Anic"]
korImena = ["lbojka", "iivic", "pperic", "aanic"]

# Učitavanje hash lozinki
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

autentikator = stauth.Authenticate(
    imena, korImena, hashed_passwords, "filmIT", "abcdef", cookie_expiry_days=30
)
ime, autentikacija_status, korIme = autentikator.login("Prijava", "main")
if autentikacija_status == False:
    st.error("Korisničko ime ili lozinka su krivo uneseni!")
if autentikacija_status == None:
    st.warning("Unesite korisničko ime i lozinku!")


# Stranica
import base64
from streamlit_lottie import st_lottie
import json
from my_db import *
from personalization import *


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        mute = st.checkbox("Ugasi pozadinsku glazbu")
        if not mute:
            md = f"""
                <audio id="backgroundMusic" autoplay="true" loop>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )


def ucitaj_loattiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def stranica(autentikator, korIme):
    st.title("FilmIT")
    st.write("### Najbolja stranica za pregled filmova")
    st.sidebar.title(f"Dobrodošao {korIme}")
    autentikator.logout("Odjava", "sidebar")

    ostavi_zadnjih_20_zanrova_korisika(korIme)
    najgledaniji_zanr_korisnika = najgledaniji_zanr(korIme)

    if najgledaniji_zanr_korisnika:
        atributi = atributi_zanra.get(najgledaniji_zanr_korisnika)
        boja_pozadine = atributi["background_color"]
        datoteka_audio = atributi["audio_file"]
        datoteka_animacije = atributi["image_file"]

        with st.sidebar:
            autoplay_audio(datoteka_audio)

            lottie_coding = ucitaj_loattiefile(datoteka_animacije)
            st_lottie(
                lottie_coding,
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=220,
            )

        st.markdown(
            f"""
            <style>
                .main {{
                    background-color: {boja_pozadine} !important;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.write(
            f"Neki od filmova iz vašeg omiljenog žanra: {najgledaniji_zanr_korisnika}"
        )
        df_filmovi = pd.DataFrame(
            nasumicni_filmovi_zanra(najgledaniji_zanr_korisnika), columns=["title"]
        )
        prikazi_filmske_postere(df_filmovi)
    else:
        lottie_coding = ucitaj_loattiefile("Animations/welcome.json")
        st_lottie(
            lottie_coding, speed=1, reverse=False, loop=True, quality="low", height=220
        )

        st.write(
            "#### :red[Odaberite barem jedan film kako biste dobili personalizirani sadržaj.]"
        )

    odabrani_film = st.selectbox(
        "Napišite ili odaberite film iz padajućeg izbornika:", lista_naslova
    )

    if st.button("Prikaži preporuke"):
        odabrani_zanrovi = naslov_zanr[odabrani_film]
        for zanr in odabrani_zanrovi:
            umetni_red(korIme, zanr)

        preporuceni_filmovi = dohvati_preporuke(odabrani_film)

        prikazi_filmske_postere(preporuceni_filmovi)


if autentikacija_status == True:
    stranica(autentikator, korIme)
