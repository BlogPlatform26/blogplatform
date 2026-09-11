# Phase 29 — extract `misticno_jezero` post card component

## Cilj

Izdvojiti postojeći prikaz jednog posta iz `misticno_jezero.html` bez promjene DOM strukture, CSS klasa ili ponašanja.

## Promjene

- Dodana je tanka komponenta `blog/templates/blog/components/special_designs/misticno_jezero_post_card.html`.
- Loop ostaje u `misticno_jezero.html` i uključuje komponentu za svaki post.
- Komponenta nastavlja koristiti postojeće `post_meta`, `post_body`, `post_actions` i `post_comments` komponente.
- Empty-state i paginacija nisu mijenjani.

## Provjere

- Django template/static provjere
- `manage.py check`
- cijeli postojeći Django test suite
- desktop i mobilni smoke-test dizajna kada su lokalni probni podaci dostupni
