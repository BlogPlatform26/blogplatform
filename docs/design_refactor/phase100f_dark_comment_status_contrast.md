# Phase 100f — statusne poruke komentara u tamnim temama

## Potvrđeni uzrok

U `dark` i `dark_right` izravne statusne poruke komponente komentara koristile su Bootstrap `.text-muted`: `rgba(33,37,41,0.75)` na neprozirnoj `#111111` podlozi, uz opacity 1 svih roditelja i bez intervenientne slike. Nakon alpha compositinga kontrast je **1.15:1**. To uključuje poruku gostu o registraciji; isti markup koristi obavijest o praznom popisu, ograničenju i isključenim komentarima.

## Uska izmjena

Unutar postojeće dark/dark_right grane `blog_design_styles.html` dodano je `[id^="comments-"] > .small.text-muted { color:#bbb !important; }`. Boja prati postojeći sekundarni tekst tamne teme. `!important` je potreban protiv Bootstrap utility pravila. Selektor ne mijenja tekst komentara, autora, formu, druge dijelove stranice ili svijetle teme. Nema promjene dozvola, markup logike ni podataka aplikacije.

## Dokazi

- Browser prije/poslije: obje teme, blog i detail, 320/390/768/1440 px — po **16 stanja**. Nova computed boja svugdje `rgb(187,187,187)` na `#111111`: **9.84:1**, document overflow 0.
- Dodatna sintetička objava bez komentara i privremeno isključeno komentiranje provjereni na 390/1440 px; poruke „Nema komentara” i „Komentiranje je isključeno” također koriste #bbb. Sintetička postavka zatim vraćena.
- Classic kontrolni prikaz na 390/1440 px zadržava originalnu computed boju; pravilo ne curi iz tamne grane.
- Sigurno otvaranje objave i skok na komentare provjereni za obje teme. Mobilni dark i desktop dark_right vizualno pregledani. Nema slanja komentara ni lajkova.
- Ograničeni prijavljeni korisnik nije zasebno browser testiran u ovoj fazi; statički koristi isti neposredni p.small.text-muted. Ovo nije tvrdnja o novoj provjeri prava pristupa.
- `manage.py check` bez problema; `makemigrations --check --dry-run` bez promjena. Puni suite **214/214** prošao u 99.546 s.

Korištena je samo izolirana `.qa100e.sqlite3` na portu8017. Originalni repozitorij, db.sqlite3, media, port8000 i main nisu mijenjani. Završna matrica drugih 28 dizajna, potpuni tvornički Default, lokalni overflow i preostale touch mete i dalje su otvoreni.
