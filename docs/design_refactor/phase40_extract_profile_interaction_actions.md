# Phase 40 — centralize profile interaction actions

## Cilj

Centralizirati samo auth/owner i follow/unfollow/restrict/block akcijsku jezgru koju koriste Magazin, Studio i postojeći zajednički profilni sidebar, bez promjene njihovih identity prikaza ili položaja.

## Granice

- Caller zadržava avatar, ime, brojače, author link, restricted poruku i okolni profilni markup.
- Komponenta prima samo postojeće klase za actions wrapper, dropdown, toggle, menu, dodatnu follow-button klasu i veličinu ikone.
- CSS, kalendar, arhiva, analytics i ostali dizajni nisu mijenjani.

## Regresijska provjera

Za Magazin, Studio i zajednički profilni sidebar provjeravaju se anonymous, owner, neprateći, following i restricted scenariji. Provjera obuhvaća DOM elemente, redoslijed klasa, form action URL-ove, tekstove, ikonu i disabled stanje.

## Rezultat provjera

- svih 15 semantičkih prije/poslije DOM rendera identično je baselineu
- ciljani regresijski testovi prolaze
- template/static provjera i `manage.py check` prolaze
- cijeli postojeći Django suite prolazi
- Magazin, Studio i Nebeska klasika prolaze desktop i mobilni UI smoke-test s autenticiranim akcijama
