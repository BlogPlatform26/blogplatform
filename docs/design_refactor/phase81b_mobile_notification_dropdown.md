# Phase 81b — mobilni izbornik obavijesti

Datum: 2026-09-26. Uski popravak zajedničkog izbornika obavijesti u `blog/base.html` i `dashboard_base.html`, preko jedinog zajedničkog partiala `blog/partials/_notification_dropdown.html`.

## Problem i opseg

Phase 81a je pri otvorenom izborniku izmjerio potpuno ili većinom skriven meni širine 300 px:

- blog baza: `-215..85` na 320 px i `-180..120` na 390 px;
- dashboard baza: `-268..32` na 320 px i `-208..92` na 390 px;
- akcije u zaglavlju bile su visoke 15 px, a red obavijesti 43 px;
- pri 768 i 1440 px meni je već bio unutar viewporta.

Popravak je zato ograničen na `@media (max-width: 600px)`: dropdownov omotač postaje statički sidren u navbaru, a meni dobiva lijevi i desni odmak 10 px, automatsku širinu i uklonjen transform. Akcije i red obavijesti dobivaju najmanje 44 px visine. Desktop pravila nisu promijenjena.

## Provjera

Korištena je izolirana kopija baze, prijavljeni `phase76_owner` i jedna sintetička nepročitana obavijest od `phase81b_sender`. Obavijest, „Označi pročitano” i „Vidi sve” nisu kliknuti.

- Interaktivni pregled blog baze na 320 px izmjerio je meni `10..294.67` unutar raspoložive širine dokumenta 305 px; obje akcije i red obavijesti imaju 44 px.
- Isto zajedničko pravilo renderira se na `/notifications/` (`blog/base.html`) i `/profile/edit/` (`dashboard_base.html`), što pokriva regresijski test sa stvarnom nepročitanom obavijesti.
- Na 390 px isto mobilno pravilo zadržava 10 px odmaka s obje strane. Na 768 i 1440 px media query se ne primjenjuje, pa ostaje ranije provjeren desktop raspored širine 300 px.
- Tijekom završnog serijskog očitanja kontrola preglednika prestala je odgovarati; zato nisu izmišljene dodatne piksel-koordinate. Ponašanje breakpointa dodatno je zaključano render-contract testom, a prvi stvarni mobilni prolaz potvrđuje computed layout.

Provjere: `manage.py check` bez problema, ciljani test 1/1 i puni Django suite 51/51. Izvorna baza, mediji, port 8000 i stanje obavijesti nisu mijenjani.
