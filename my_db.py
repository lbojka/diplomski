import sqlite3

conn = sqlite3.connect("diplomski.db", check_same_thread=False)

c = conn.cursor()


def umetni_red(korIme, zanr):
    c.execute("INSERT INTO aktivnost values (?,?)", (korIme, zanr))
    conn.commit()


def isprazni_tablicu():
    c.execute("DELETE FROM aktivnost")
    conn.commit()


def najgledaniji_zanr(korIme):
    c.execute(
        """
    SELECT zanr, COUNT(*) AS broj_gledanja
    FROM aktivnost
    WHERE korIme = ?
    GROUP BY zanr
    ORDER BY broj_gledanja DESC
    LIMIT 1;
    """,
        (korIme,),
    )
    najgledaniji_zanr = c.fetchone()

    if najgledaniji_zanr:
        return najgledaniji_zanr[0]  # vrati samo zanr
    else:
        return None


def ostavi_zadnjih_20_zanrova_korisika(korIme):
    c.execute("SELECT COUNT(*) FROM aktivnost WHERE korIme = ?", (korIme,))
    broj_redova = c.fetchone()[0]

    redova_za_obrisat = max(0, broj_redova - 20)

    if redova_za_obrisat > 0:
        c.execute(
            f"""
                DELETE FROM aktivnost 
                WHERE rowid IN (
                    SELECT rowid
                    FROM aktivnost
                    WHERE userId = ?
                    ORDER BY rowid ASC
                    LIMIT {redova_za_obrisat}
                );
            """,
            (korIme,),
        )
        conn.commit()
