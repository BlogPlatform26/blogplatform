# Phase 35 — extract `studio` post card component

## Cilj

Izdvojiti cijeli postojeći prikaz jednog Studio posta bez promjene DOM strukture, CSS klasa, uvjeta ili ponašanja.

## Sigurnosna analiza

- Studio kartica ima poseban dvostruki prikaz datuma i dinamične `post_date_style` / `post_date_effect` klase i atribute.
- Cijeli Studio-specifični blok premješten je doslovno, uključujući završni `<hr>`.
- Kartica ovisi samo o postojećem `post` i `blog_preferences` kontekstu; nema ovisnosti o `forloop` stanju.
- Postojeće `post_meta`, `post_body`, `post_actions` i `post_comments` komponente ostaju semantički i sadržajno nepromijenjene.

## Granice promjene

- Loop, empty-state i paginacija ostaju u `studio.html`.
- Sidebar, kalendar/arhiva, navbar, skripte i drugi dizajni nisu mijenjani.

## Provjere

- Django template/static provjere
- `manage.py check`
- cijeli postojeći Django test suite
- desktop i mobilni smoke-test Studio dizajna nad probnom bazom
