# tsoha-chat
Keskustelusovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.


Nykytilanne:

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. 

Käyttäjä näkee sovelluksen etusivulla listan alueista sekä ketjujen määrän sekä viimeksi lähetetyn viestin ajankohdan. 

Käyttäjä voi luoda uuden alueen, keskustelun tai lähettää viestin. 


Tavoite:

Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.

Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.

Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.

Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.

Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.

Ylläpitäjä voi lisätä ja poistaa keskustelualueita.

Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.


Käynnistysohje:

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL=<tietokannan-paikallinen-osoite>

SECRET_KEY=<salainen-avain>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run
