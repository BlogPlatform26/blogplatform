# Phase 81c — mobilne mete uređivanja profila

Datum: 2026-09-26. Uski popravak mobilnih dodirnih meta na `/profile/edit/`, bez promjene funkcionalnosti obrasca ili desktop izgleda.

## Opseg

- četiri polja profila: `username`, `email`, `blog_name` i `blog_tagline`;
- gumb „Spremi promjene”;
- četiri navigacijske stavke profilnog dropdowna u `dashboard_base.html`;
- pravila vrijede samo u `@media (max-width: 600px)`.

Dodane su specifične klase `bp-profile-edit-form`, `bp-profile-save` i `bp-profile-menu`. Time se pravila ne prelijevaju na druge obrasce ili dropdownove.

## Stvarna browser mjerenja

Korištena je izolirana kopija baze i prijavljeni `phase76_owner`. Na svakoj širini izmjereno je sva četiri polja; vrijednosti u tablici jednake su za sva četiri. Profilni dropdown je otvoren, ali njegove poveznice nisu aktivirane.

| Viewport | Polja prije → poslije | Gumb prije → poslije | Stavke menija prije → poslije | Dokument | Rezultat |
|---:|---:|---:|---:|---:|---|
| 320 | 37,33 → 44 px | 37,33 → 44 px | 32 → 44 px | 320 px bez preljeva | prolaz |
| 390 | 37,33 → 44 px | 37,33 → 44 px | 32 → 44 px | 390 px bez preljeva | prolaz |
| 768 | 37,33 → 37,33 px | 37,33 → 37,33 px | 32 → 32 px | 768 px bez preljeva | desktop nepromijenjen |
| 1440 | 37,33 → 37,33 px | 37,33 → 37,33 px | 32 → 32 px | 1440 px bez preljeva | desktop nepromijenjen |

Na 320 i 390 px izvršen je stvarni klik na polje korisničkog imena; `document.activeElement.id` bio je `id_username`. Nije unesena vrijednost, obrazac nije predan i nijedan podatak računa nije promijenjen.

Regresijski test potvrđuje da `/profile/edit/` renderira specifične klase, mobilni breakpoint i 44 px ugovor. Izvorni `db.sqlite3`, mediji, port 8000 i grana `main` nisu dirani.
