# Phase 88c1 — Polarna svjetlost: naslov i sadržaj objave

## Opseg

Phase 88c1 foto-neovisno popravlja naslov bloga, tagline, naslov objave,
tijelo objave i autora objave u `polarna_svjetlost`. Ne mijenja komentar,
autora komentara, arhivu ni tabletni kalendar; to ostaje za Phase88c2.

## Promjena

Naslovi dobivaju kompaktne tamne površine `#123047` s tekstom `#f1fbff`.
Sadržaj i autor dobivaju obrnutu svijetlu površinu s tamnom tintom. Sve su
površine pune i lokalne uz tekst, pa aurora ostaje dominantna izvan njih.
Pair je isti kao Phase88b action ugovor.

## Stvarni preglednik

Prije 88c1 audit je za transparentne mete zabilježio referentnih 3,55–3,82:1
prema osnovnoj pozadini, s još manjim mogućim minimumom preko fotografije.
Nakon promjene naslov, tagline, naslov posta, tijelo i autor imaju
**12,98:1** na blog i detail rutama pri 320, 390, 768 i 1440 px (osam stanja).
Pune površine zadržavaju vrijednost na svijetlim i tamnim aurora cropovima.

Document overflow ostaje `0 px`. Vizualni pregled na 390 px potvrđuje očuvan
aurora identitet. Sigurni klikovi `Prethodni mjesec` i `Otvori post` vode na
očekivane rute bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase88c1_polarna_post_contrast.py` provjerava lokalni ugovor na
blog/detail rutama i izolaciju od drugog dizajna.

## Otvoreno za Phase88c2

Komentar, autor komentara i arhivska poveznica ostaju prozirni preko aurora
fotografije. Tabletni calendar overflow također nije dio ovoga opsega.
