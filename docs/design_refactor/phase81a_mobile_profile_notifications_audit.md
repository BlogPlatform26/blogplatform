# Phase 81a — mobilni audit profila i obavijesti

Datum: 2026-09-20. Audit bez aplikacijskog popravka. Korištena je izolirana kopija sintetičke baze, prijavljeni `phase76_owner` i jedna sintetička nepročitana obavijest. Nije kliknuta obavijest (njezin GET je označava pročitanom), „Označi pročitano”, spremanje profila ni podrška. Izvorna baza, mediji i port 8000 nisu dirani.

## Stvarne rute i predlošci

- `/profile/` samo preusmjerava na `/blog/<username>/`; profil je korisnikov blog u aktivnom dizajnu (`user_blog`, ne zasebni `profile.html`). Mjeren je sintetički zadani dizajn; to nije pokriće svih 37 dizajnova.
- `/profile/edit/` koristi `blog/edit_profile.html` nad `dashboard_base.html`.
- `/notifications/` koristi `blog/notifications.html` nad `blog/base.html`.
- Zvonce koristi zajednički `blog/partials/_notification_dropdown.html` u oba bazna zaglavlja. `/notification/<id>/` mijenja `is_read` te namjerno nije otvaran.

## Nalazi

1. **P0 — izbornik obavijesti je većinom izvan mobilnog zaslona.** Na `/notifications/` (blog baza), otvoreni meni širine 300 px pri viewportu 320 stoji od x=-215 do x=85; na 390 od x=-180 do x=120. Na `/profile/edit/` (dashboard baza) još je lošije: -268..32 na 320 i -208..92 na 390. Na 768/1440 meni je unutar viewporta. Dokument nema horizontalni scroll, pa `overflow-x:hidden` i pozicioniranje praktično skrivaju akcije i sadržaj. Sintetički red postoji u meniju; njegov hit target je 43 px, dok su „Označi pročitano” i „Vidi sve” visoki samo 15 px. Screenshot u pregledniku potvrdio je da se pri 320 px vidi tek desni komadić menija. Sljedeća najmanja faza: popraviti *zajednički* dropdown tako da se na mobilnom pozicionira unutar viewporta u oba bazna zaglavlja, bez promjene desktopa; zasebno povećati akcijske mete i provjeriti 320/390/768/1440 uz otvoren meni i stvarnu obavijest. Ne popravljati samo `blog/base.html`.
2. **P1 — uređivanje profila ima male dodirne mete.** Na 320 i 390 četiri vidljiva tekstualna polja (`username`, `email`, `blog_name`, `blog_tagline`) i „Spremi promjene” mjere 37 px. Dokument je širok točno 320/390 px bez horizontalnog preljeva. Klik/fokus polja korisničkog imena uspio je bez predaje obrasca. Profilni dropdown je unutar viewporta (x=76..308 na 320), ali njegove četiri navigacijske stavke mjere 32 px, a pozdrav je unutar vlastitog okvira skraćen za oko 10 px. Uski sljedeći popravak nakon P0: mobilni 44 px polja/gumb i profilne stavke u `dashboard_base.html`, bez diranja blog dizajna.
3. **P1 — gustoća teksta u dropdownu.** Sintetički red obavijesti koristi sitan tekst (oko 12 px pri mjerenju) i praktično nečitljive akcije od 15 px. Potrebno ga je pregledati zajedno s P0 pozicioniranjem.
4. **Niži prioritet — korisnički blog i puna lista.** Na default blogu dokumentne širine bile su 305/375/753/1425 za viewport 320/390/768/1440; karta ima vlastiti interni višak širine oko 180 px, ali ne stvara dokumentni preljev. Na `/notifications/` dokumentne širine također su 305/375/753/1425. Gumb „Označi sve pročitano” na 320/390/768 se prelama na 51 px visine i ostaje unutar prikaza; na 1440 je 30 px. Red obavijesti je pri 320 visok 90 px i u cijelosti vidljiv. Pomoć/podrška u zajedničkoj bazi ima dodatna mala polja i gumb, ali nije predmet ovog uskog audita.

Profilni dropdown i zvonce otvoreni su bez aktiviranja poveznica ili mijenjanja obavijesti. `manage.py check` prijavljuje 0 problema. Puni test suite nije ponovno pokrenut jer je ovo dokumentacijski audit bez aplikacijskih izmjena; prethodna Phase 80d provjera bila je 50/50.
