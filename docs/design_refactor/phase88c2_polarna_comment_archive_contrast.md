# Phase 88c2 — Polarna svjetlost: komentari i arhiva

## Opseg

Phase 88c2 završava preostali P1 kontrast komentara, autora komentara i
arhivske poveznice u `polarna_svjetlost`. Ne dira 88b akcije, 88c1 naslov i
sadržaj, ni tabletni calendar overflow.

## Promjena

Tekst i autor komentara te arhivska poveznica koriste punu `#f1fbff` površinu
s tintom `#123047`. Lokalni override uključuje nested mobilne word-spanove
comment renderera; time kasnije responsive pravilo više ne vraća svijetlu tintu
preko svijetle površine.

## Stvarni preglednik

Sve tri mete imaju **12,98:1** na blog i detail rutama pri 320, 390, 768 i
1440 px (osam stanja), uz document overflow `0 px`. Pune površine ostaju
stabilne na svijetlim i tamnim aurora cropovima. Sigurni klikovi `Prethodni
mjesec` i arhivske poveznice otvorili su očekivane query rute bez mutacije.

## Regresijska zaštita

`blog/test_phase88c2_polarna_comment_archive_contrast.py` pokriva lokalni
ugovor na blog/detail rutama i izolaciju od drugog dizajna.

## Preostalo

P1 kontrast javnog post shell-a za `polarna_svjetlost` zatvoren je kroz
Phase88b/c1/c2. Ostaje P2 tabletni calendar overflow i touch mete.
