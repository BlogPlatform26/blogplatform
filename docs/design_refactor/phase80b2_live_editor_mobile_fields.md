# Phase 80b2 — mobilne kontrole polja live editora

Nastavak Phase 80b ograničen je na zasebni `design_live_editor.html`. Pri viewportu do 575,98 px selecti, kontrole boje, brojčana polja i interaktivni okvir slidera imaju visinu 44 px. Mobilni slider više se ne smanjuje transformacijom `scale(.88)`, pa se ne smanjuje ni njegov klikabilni okvir. Boje, tipografija i logika editora nisu mijenjane. Desktop pravila na 768/1440 px ostaju izvorna.

| Kontrola | Prije 320/390 | Poslije 320/390 | 768/1440 |
| --- | ---: | ---: | ---: |
| Select font/način/efekt | 36 px | 44 px | 36 px |
| Boja | 36 px | 44 px | 36 px |
| Brojčana veličina | 36 px | 44 px | 36 px |
| Slider, okvir za interakciju | ≈21 px | 44 px | ≈21 px |

Mjereno u izoliranoj probnoj bazi na Magazinu (`Naslovi`: pet selecta, četiri boje, četiri brojčana polja i četiri slidera) i Simple Uzorku (`Pozadine`: dva selecta i četiri boje). Na 320/390/768/1440 px širina dokumenta bila je 305/375/753/1425 px; nijedan element bočne ploče nije prešao desni rub. Klik/fokus font-selecta, boje i slidera na Magazinu te selecta i boje na Simple Uzorku radio je bez spremanja. Promjena slidera ažurirala je povezano brojčano polje samo u nespremljenom prikazu. Izvorna baza i mediji nisu dirani, a probna baza uklonjena je nakon pregleda.

Uski render regresijski test dodan je u postojeći live-editor test. `manage.py check` prolazi; puni Django suite 48/48.

Preostaje Phase 80c: unutarnji preljev i raspored mobilnog previewa. Settings podtabovi iz Phase 80a ostaju zaseban Phase 80d.
