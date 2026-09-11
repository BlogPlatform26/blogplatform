# Phase 32 — extract `ruzicasti_vrt` post card component

## Cilj

Izdvojiti postojeći prikaz jednog posta iz `ruzicasti_vrt.html` bez promjene DOM strukture, CSS klasa ili ponašanja.

## Promjene

- Dodana je tanka komponenta `blog/templates/blog/components/special_designs/ruzicasti_vrt_post_card.html`.
- Loop ostaje u `ruzicasti_vrt.html` i uključuje komponentu za svaki post.
- Komponenta nastavlja koristiti postojeće `post_meta`, `post_body`, `post_actions` i `post_comments` komponente.
- Empty-state, paginacija, sidebar, kalendar i arhiva nisu mijenjani.

## Provjere

- Django template/static provjere
- `manage.py check`
- cijeli postojeći Django test suite
- desktop i mobilni smoke-test dizajna kada su lokalni probni podaci dostupni
