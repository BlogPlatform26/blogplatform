# Phase 37 — extract `vecer_zaljubljenih` post card component

## Cilj

Izdvojiti postojeći prikaz jednog posta iz `vecer_zaljubljenih.html` bez promjene DOM strukture, CSS klasa, uvjeta ili ponašanja.

## Sigurnosna analiza

- Kartica koristi postojeći `post` kontekst, standardni datum `d.m.Y`, dizajnerski divider i naslov.
- Nema posebnih uvjeta, dinamičkih atributa ni ovisnosti o `forloop` stanju.
- Postojeće `post_meta`, `post_body`, `post_actions` i `post_comments` komponente ostaju nepromijenjene.

## Granice promjene

- Loop, empty-state i paginacija ostaju u `vecer_zaljubljenih.html`.
- Sidebar, kalendar/arhiva, navbar, skripte i drugi dizajni nisu mijenjani.

## Provjere

- Django template/static provjere
- `manage.py check`
- cijeli postojeći Django test suite
- desktop i mobilni smoke-test dizajna nad probnom bazom
