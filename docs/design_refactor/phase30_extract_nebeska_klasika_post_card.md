# Phase 30 — extract `nebeska_klasika` post card component

## Cilj

Izdvojiti postojeći prikaz jednog posta iz `nebeska_klasika.html` bez promjene DOM strukture, CSS klasa ili ponašanja.

## Promjene

- Dodana je tanka komponenta `blog/templates/blog/components/special_designs/nebeska_klasika_post_card.html`.
- Loop ostaje u `nebeska_klasika.html` i uključuje komponentu za svaki post.
- Komponenta nastavlja koristiti postojeće `post_meta`, `post_body`, `post_actions` i `post_comments` komponente.
- Empty-state, paginacija, sidebar, kalendar i arhiva nisu mijenjani.

## Provjere

- Django template/static provjere
- `manage.py check`
- cijeli postojeći Django test suite
- desktop i mobilni smoke-test dizajna kada su lokalni probni podaci dostupni
