# Phase 93f — mobilna objava i komentar u dizajnu Sjene ulice

## Opseg

Isključivo mobilni raspored `sjene_ulice` do 575,98 px: kartica koristi punu širinu s manjim unutarnjim razmakom, datum je ispod naslova, naslov objave i naslov komentara imaju mobilnu gornju granicu veličine, a avatar komentara je iznad tijela komentara. Tipografija i raspored na 768/1440 px ostali su isti; noćna fotografija i kontrastna podloga iz Phase93d nisu dirnute.

## Browser provjera

Izolirana baza `db_phase93f_trial.sqlite3` s objavom i komentarom, lokalni server 127.0.0.1:8026, učitan Bootstrap. Blog i detalj objave provjereni su prije/poslije na 320/390/768/1440 (osam stanja svake strane).

| Širina | Kartica prije (client/scroll) | Kartica poslije | Naslov komentara prije | Poslije | Tekst komentara prije → poslije |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 320 | 209/347 | 233/233 | 161/323 | 201/201 | 78 → 172 px |
| 390 | 279/347 | 303/303 | 231/323 | 271/271 | 148 → 242 px |
| 768 | 641/641 | 641/641 | 593/593 | 593/593 | 432 → 432 px |
| 1440 | 615/615 | 615/615 | 567/567 | 567/567 | 405 → 405 px |

`documentElement.scrollWidth == clientWidth` u svih osam stanja. Mobilni naslov objave je 24/27,3 px, naslov komentara 24 px; na 768/1440 oba su ostala 64 px prema postojećoj korisničkoj prilagodbi. Komentar se vizualno čita u punijoj širini bez odsijecanja teksta. Na 390 px sigurno su kliknuti prethodni mjesec i dan s objavom; oba vode na očekivani URL, a like/komentari nisu mutirani.

Uski regresijski testovi za Phase93d/e/f: 6/6. `manage.py check`, `makemigrations --check --dry-run`, puni suite 167/167 i `git diff --check` prolaze.

## Otvoreno

P2 mobilni kalendarski dani 27/31 px, pojedine desktop kalendarske mete i shared tablet/desktop post-action mete ostaju. Kraljevska sidebar foto-kontrast, audit `mjesecev_ples`/`asfaltni_plamen` i završna matrica svih 37 s komentarima/fotografskim zonama također ostaju.
