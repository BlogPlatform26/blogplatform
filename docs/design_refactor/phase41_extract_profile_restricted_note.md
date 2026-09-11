# Phase 41 — centralize restricted profile note

## Cilj

Centralizirati samo postojeći auth/owner/restricted uvjet i identičan tekst profilne poruke za Magazin, Studio i zajednički profilni sidebar.

## Granice

- Nova komponenta renderira isti jedan `div` i prima postojeću CSS klasu callera.
- Caller zadržava položaj poruke i sav okolni profilni markup.
- CSS, analytics layout, kalendar, arhiva, postovi, komentari i drugi dizajni nisu mijenjani.

## Regresijska provjera

Za sva tri callera provjeravaju se anonymous, owner, unrestricted viewer i restricted viewer. Samo restricted viewer smije dobiti poruku s identičnim elementom, klasom i tekstom.

## Rezultat provjera

- svih 12 semantičkih prije/poslije DOM rendera identično je baselineu
- ciljani restricted-note test prolazi
- template/static provjera i `manage.py check` prolaze
- cijeli postojeći Django suite prolazi
- Magazin, Studio i Nebeska klasika prolaze desktop i mobilni UI smoke-test
