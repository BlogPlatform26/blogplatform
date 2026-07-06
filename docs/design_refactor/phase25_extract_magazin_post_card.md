# Phase 25 — extract `magazin` post card component
Izrađeno: 2026-07-05 12:24:17
## Cilj
Izdvojiti postojeći prikaz jednog posta iz `magazin.html` u posebnu komponentu bez promjene HTML strukture, CSS-a ili izgleda.
## Promjene
- Izmijenjeno: `blog\templates\blog\designs\magazin.html`
- Dodano: `blog\templates\blog\components\special_designs\magazin_post_card.html`
- Backup: `_backup_design_refactor_phase25_magazin_post_card_20260705_122417`

## Što je izdvojeno
- Originalni `{% for post in page_obj %}` počeo je oko linije **675**.
- Izdvojeno linija: **35**.
- Loop je ostao u `magazin.html`, ali sada unutar loopa poziva komponentu.

## Provjere
- `target_contains_include`: da
- `component_contains_article`: da
- `component_contains_post_body`: da
- `component_contains_post_actions`: da
- `component_contains_post_comments`: da
- `target_still_has_loop`: da

## Napomena
Ova faza ne dira CSS, sidebar, komentare ni globalni navbar. Cilj je samo smanjiti kopirani HTML u posebnom dizajnu i pripremiti postupni refaktor.

## Testirati
- `magazin` dizajn s jednim i više postova
- naslov posta
- datum
- meta podaci
- sadržaj posta
- akcije posta
- komentari
- paginacija / empty stanje ako nema postova
