# Phase 36 — extract `vecer_uz_jezero` post card component

## Cilj

Izdvojiti postojeći prikaz jednog posta iz `vecer_uz_jezero.html` bez promjene DOM strukture, CSS klasa, uvjeta ili ponašanja.

## Sigurnosna analiza

- Kartica koristi samo postojeći `post` kontekst, standardni datum `d.m.Y` i naslov.
- Nema posebnih uvjeta, dinamičkih atributa ni ovisnosti o `forloop` stanju.
- Postojeće `post_meta`, `post_body`, `post_actions` i `post_comments` komponente ostaju nepromijenjene.

## Granice promjene

- Loop, empty-state i paginacija ostaju u `vecer_uz_jezero.html`.
- Sidebar, kalendar/arhiva, navbar, skripte i drugi dizajni nisu mijenjani.

## Provjere

- Django template/static provjere
- `manage.py check`
- cijeli postojeći Django test suite
- desktop i mobilni smoke-test dizajna nad probnom bazom
