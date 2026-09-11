# Phase 31 — extract `ponocna_elegancija` post card component

## Cilj

Izdvojiti postojeći prikaz jednog posta iz `ponocna_elegancija.html` bez promjene DOM strukture, CSS klasa ili ponašanja.

## Promjene

- Dodana je tanka komponenta `blog/templates/blog/components/special_designs/ponocna_elegancija_post_card.html`.
- Loop ostaje u `ponocna_elegancija.html` i uključuje komponentu za svaki post.
- Komponenta nastavlja koristiti postojeće `post_meta`, `post_body`, `post_actions` i `post_comments` komponente.
- Empty-state, paginacija, sidebar, kalendar i arhiva nisu mijenjani.
- Postojeći CSS naslova nije mijenjan.

## Provjere

- Django template/static provjere
- `manage.py check`
- cijeli postojeći Django test suite
- desktop i mobilni smoke-test dizajna kada su lokalni probni podaci dostupni
