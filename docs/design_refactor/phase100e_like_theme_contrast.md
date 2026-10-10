# Phase 100e — kontrast gumba za lajk

## Uzrok i promjena

Stvarni `.post-actions button.btn-link` nasljeđivao je Bootstrapovu boju `#0d6efd`; pravila teme obuhvaćala su poveznice i spanove, ali ne gumb obrasca. `blog_design_styles.html` sada uključuje `.btn-link` u postojeću Simple i Retro paletu te dodjeljuje boju akcijskih poveznica dark/classic/default obiteljima. Nema promjene markupa, ponašanja obrasca, rasporeda niti spremljenih korisničkih preferencija.

## Provjera u pregledniku

Izolirana `.qa100e.sqlite3`, server 127.0.0.1:8017, sintetički autori 2301–2309 izvan legacy ID-a 1. Sedam pogođenih dizajna provjereno je prije i nakon promjene na blogu i detalju, na 320/390/768/1440 px (56 stanja po prolazu); dodatno su nakon promjene provjerene dvije Default varijante (16 stanja). Bootstrap je učitan: početni computed color gumba bio je rgb(13,110,253).

Mjerenje koristi stvarnu computed boju gumba i prvi neprozirni pozadinski sloj iza njega, nakon provjere da intervenientni slojevi nemaju sliku i imaju opacity 1. Podloga gumba u ovim tvorničkim konfiguracijama nije fotografija. Nakon CSS izmjene server je ponovno pokrenut radi cached template loadera; raniji prolaz sa starim predloškom nije korišten kao dokaz popravka.

| Dizajn | Boja gumba | Neprozirna podloga | Kontrast nakon |
| --- | --- | --- | ---: |
| dark / dark_right | #4da3ff | #111111 | 7.19:1 |
| classic / classic_right | #7a2cff | #f6f6f4 | 5.34:1 |
| simple_pattern / simple_image | #3d6d86 | #fffefb | 5.58:1 |
| simple_retro | #2f6870 | #fbfaf6 | 6.03:1 |
| default / default_right | #7a2cff | #ffffff | 5.78:1 |

Svih 72 prikaza nakon promjene nema horizontalni document overflow. Siguran klik „Otvori post” na 390 px potvrđen za svih devet: odredišni detalj prikazuje komentare. Nisu slani lajkovi ni komentari. Mobilni dark i desktop default_right vizualno pregledani. Ova provjera ne dokazuje kontrast proizvoljnih korisničkih paleta, hover/focus stanja niti kompletnu završnu matricu.

`manage.py check`: bez problema. `makemigrations --check --dry-run`: bez promjena. Puni postojeći suite: **214/214**, 96.549 s. `git diff --check`: prolaz.

## Preostalo

Završna matrica ostalih 28 dizajna i potpuna tvornička Default provjera ostaju otvorene; ovdje je Default provjeren samo za gumb, overflow i navigaciju. Touch mete i lokalni Simple overflow iz Phase100a nisu ovim zahvatom riješeni. Mobilni dark screenshot pokazuje dodatnog kandidata: poruka „Za komentiranje je potrebna registracija” vrlo je tamna na tamnoj podlozi; potrebno zasebno computed mjerenje i provjera ostalih tema.

Izvorni repozitorij, db.sqlite3, media, port 8000 i main nisu mijenjani. Rad se nastavlja u zadatku 01a12503-35e7-78d1-a949-a3fc146b4eb0; prethodni zadatak i fork su pauzirani.
