# Phase 100a — aktualna verifikacija prvih devet dizajna

Ovo je **prva serija** završne matrice, ne potvrda svih 37 dizajna. U izoliranoj sintetičkoj bazi svaki od devet registriranih ključeva imao je autora, javnu objavu i komentar. Stvarni Chrome s primijenjenim Bootstrapom otvorio je blog i detalj na 320/390/768/1440 px: **72 stanja**. Za tekst su uzorkovani stvarni pikseli ispod prikazanih glifova (privremeno obojenih prozirno samo u QA pregledniku), uz computed boju i neprozirnost. To je uklonilo lažne padove koje bi dalo uzorkovanje praznog dijela širokog elementa. Svaki blog imao je sigurno otvaranje objave na 390 px, bez like/comment mutacije.

Tablica prikazuje najmanji izmjereni omjer kroz osam stanja svakog dizajna. `Komentar` je tekst / autor komentara; sve vrijednosti su prema stvarno prikazanoj podlozi, ali ne dokazuju svaku moguću korisnički učitanu fotografiju ili prilagođenu paletu.

| Dizajn | Naslov / podnaslov bloga | Naslov posta | Autor posta | Like | Komentar tekst / autor | Kalendar dan / arhiva | Document / lokalni overflow |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `default` | 12,49 / 7,09 | 15,57 | 5,16 | 4,50 | 15,27 / 4,98 | 5,78 / 7,01 | 0 / 0 px |
| `dark` | 18,88 / 12,74 | 7,69 | 7,19 | **4,20** | 5,45 / 5,05 | 5,34 / 11,06 | 0 / 0 px |
| `classic` | 17,45 / 10,51 | 15,00 | 4,73 | **4,16** | 13,07 / 4,58 | 5,78 / 7,97 | 0 / 0 px |
| `default_right` | 12,49 / 7,09 | 17,74 | 5,78 | 4,50 | 15,27 / 4,98 | 5,78 / 7,01 | 0 / 0 px |
| `dark_right` | 18,88 / 12,74 | 18,88 | 7,19 | **4,20** | 5,45 / 5,05 | 5,34 / 11,06 | 0 / 0 px |
| `classic_right` | 17,45 / 10,51 | 15,23 | 5,34 | **4,16** | 13,07 / 4,58 | 5,78 / 7,97 | 0 / 0 px |
| `simple_pattern` | **2,97 / 3,16** | **3,93** | 5,58 | **4,46** | 6,75 / 4,98 | 5,09 / 4,98 | 0 / 2 px |
| `simple_image` | 5,92 / 5,92 | **4,31** | 5,58 | **4,46** | 6,75 / 4,98 | 5,09 / 4,98 | 0 / 2 px |
| `simple_retro` | 6,18 / 6,18 | **3,11** | 6,03 | **4,31** | 6,20 / 5,38 | 6,30 / 6,55 | 0 / 0 px |

Obični post tekst, akcijske poveznice i kalendarska navigacija u ovoj seriji također su iznad 4,5:1; najmanji izmjereni omjeri tih triju skupina bili su **6,95**, **5,26** i **7,16**. Tekst i autor komentara svih devet prolaze u testiranom kadru. `simple_image` je imao stvarnu sistemsku pozadinsku fotografiju, ali tekst posta je na kartici; druge foto-varijacije nisu time iscrpljene.

## Potvrđeni ostaci

- **P1:** Zadani *svježi* `simple_pattern` profil iz `blog/services.py` koristi narančasti gradijent `#d98a37` / `#b8641e` s bijelim naslovom; na njemu je naslov/podnaslov 2,97/3,16:1. Phase99g je popravila zasebnu postojeću/snimljenu svijetložutu konfiguraciju `#ffd561`, pa ovaj put još treba zaštitu. Nije razlog za mijenjanje prilagođenih paleta.
- **P1:** Naslovi postova `simple_pattern`, `simple_image` i `simple_retro` su 3,93/4,31/3,11:1. `like` je ispod 4,5:1 u tamnim, klasičnim i trima simple varijantama (4,16–4,46:1); osnovni/desni default stoje na samoj granici 4,50:1 bez margine. Popravci trebaju biti lokalni i ponovno izmjereni.
- **P2:** Vidljive like kontrole imaju najmanje 26 px visine, obične post-akcije 21 px, kalendarske strelice 30 px, a dani 31,5–37,4 px u ovoj seriji. To je ispod cilja 44×44 px; širine treba zasebno provjeriti. `simple_pattern` i `simple_image` imaju mali 2 px **lokalni**, ali ne dokumentni, overflow; izvor treba izolirati prije zahvata.

Ovaj batch ne znači da su ostalih 28 dizajna aktualno verificirana. Sljedeće uske faze trebaju prvo zatvoriti potvrđene P1 ovdje, zatim mjeriti preostale serije i završne touch/overflow regresije. Izvorni `db.sqlite3`, `media`, port 8000 i `main` nisu korišteni.

`manage.py check`, `makemigrations --check --dry-run` i puni suite **211/211** prošli su. Nije mijenjan aplikacijski kod; sintetički server i baza uklonjeni su nakon mjerenja.
