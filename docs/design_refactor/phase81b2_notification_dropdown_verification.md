# Phase 81b2 — završna verifikacija izbornika obavijesti

Datum: 2026-09-26. Ova uska faza zatvara verifikacijsku rupu iz Phase 81b stvarnim browser mjerenjima oba zaglavlja na svim dogovorenim širinama. Aplikacijski kod nije mijenjan jer kvar nije pronađen.

## Testni uvjeti

- izolirana kopija baze `db_phase81b2_trial.sqlite3`;
- prijavljeni `phase76_owner` i jedna sintetička nepročitana obavijest od `phase81b2_sender`;
- otvoreno zvonce na `/notifications/` (`blog/base.html`) i `/profile/edit/` (`dashboard_base.html`);
- viewporti 320×844, 390×844, 768×900 i 1440×900;
- obavijest, „Označi pročitano” i „Vidi sve” nisu kliknuti.

## Izmjerena matrica

Koordinate menija su `left..right`; granica za uspjeh je `0 <= left` i `right <= clientWidth`.

| Zaglavlje | Viewport | clientWidth | Meni left..right | Širina menija | Akcije | Red | Rezultat |
|---|---:|---:|---:|---:|---:|---:|---|
| `blog/base.html` | 320 | 305 | 10.00..294.67 | 284.67 | 44 px | 44 px | prolaz |
| `blog/base.html` | 390 | 375 | 10.00..364.67 | 354.67 | 44 px | 44 px | prolaz |
| `blog/base.html` | 768 | 753 | 148.55..448.55 | 300 px | 14.53 px | 43.35 px | prolaz; desktop nepromijenjen |
| `blog/base.html` | 1440 | 1440 | 835.89..1135.89 | 300 px | 14.53 px | 43.35 px | prolaz; desktop nepromijenjen |
| `dashboard_base.html` | 320 | 320 | 10.00..310.00 | 300 px | 44 px | 44 px | prolaz |
| `dashboard_base.html` | 390 | 390 | 10.00..380.00 | 370 px | 44 px | 44 px | prolaz |
| `dashboard_base.html` | 768 | 768 | 169.89..469.89 | 300 px | 14.53 px | 43.35 px | prolaz; desktop nepromijenjen |
| `dashboard_base.html` | 1440 | 1440 | 835.89..1135.89 | 300 px | 14.53 px | 43.35 px | prolaz; desktop nepromijenjen |

Razlika između `innerWidth` i `clientWidth` na blog bazi pri 320/390/768 dolazi od vertikalnog scrollbara; meni je pravilno prilagođen stvarno raspoloživoj širini dokumenta. Mobilni zahtjev od približno 44 px ispunjen je u oba zaglavlja. Desktop vrijednosti ostaju one iz pravila iznad mobilnog breakpointa.

Nakon mjerenja potvrđeno je da sintetička obavijest i dalje ima `is_read=False`. Izvorni `db.sqlite3`, mediji, port 8000 i grana `main` nisu dirani.
