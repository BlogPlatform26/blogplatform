# Phase 21 — shared customization hooks

Izrađeno: 2026-07-04 09:03:42

## Cilj

Dodati stabilne CSS hook klase na zajedničke komponente, bez promjene izgleda.

Ova faza ne dira dizajne, ne dira `base.html`, ne mijenja boje, razmake, bannere, kalendar ni arhivu.

## Promijenjene datoteke

- `blog\templates\blog\components\post_card.html` — Dodane stabilne hook klase za post card/naslov posta.
- `blog\templates\blog\components\blog_box.html` — Dodane stabilne hook klase za blog box/naslov/sadržaj.

## Dodane klase

- `blog-post-card` na vanjski wrapper posta, ako postoji `blog-post-entry`
- `blog-post-title` na naslov posta
- `blog-box` na zajednički box
- `blog-box-title` na naslov boxa
- `blog-box-content` na sadržaj boxa

## Zašto

Kasnije korisničke postavke mogu ciljati ove zajedničke klase umjesto da svaki dizajn ima poseban CSS za iste stvari.

## Test

Provjeriti da se izgled nije promijenio:

- naslovna
- `default`
- `classic`
- `simple`
- `nebeski_mir`
- `zlatno_polje`

Backup: `_backup_design_refactor_phase21_customization_hooks_20260704_090342`
