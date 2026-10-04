# Phase 87b — Iznad oblaka: naslovne površine

## Opseg

Phase 87b foto-neovisno štiti samo naslov bloga, tagline i naslov posta u
dizajnu `iznad_oblaka`. Ne mijenja akcije, kalendar, komentare, tijelo posta,
tabletni raspored ni shared CSS.

## Promjena

Tri naslovne mete dobile su punu lokalnu površinu `#514956`, prilagođenu
stvarnoj širini teksta, uz malo zaobljenje i diskretan unutarnji rub. Površina
ne dodaje layout padding pa ostaje kompaktna i ne mijenja postojeću geometriju
kartice. Pastelna fotografija ostaje vidljiva izvan samih redaka teksta.

## Kontrast i stvarni preglednik

Phase 87a izmjerio je najniže vrijednosti 1,00:1 za naslov bloga i tagline te
1,02:1 za naslov posta. Nakon Phase87b:

- naslov bloga: **7,65:1**;
- tagline: **7,65:1**;
- naslov posta: **8,04:1**.

Rezultati su isti na blog i detail prikazu na 320, 390, 768 i 1440 px, ukupno
osam stvarnih browser stanja. Budući da je površina puna, rezultat je isti na
svijetlim i tamnim zonama stvarnog responsive cropa i ima sigurnu marginu iznad
cilja 4,5:1.

Vizualni pregled na 390 i 1440 px potvrdio je da su površine kompaktne, da
fotografija ostaje dominantna te da desktop identitet nije promijenjen. Fizički
dokumentni overflow ostaje `0 px`. Sigurne navigacije `Prethodni mjesec` i
`Otvori post` prošle su bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase87b_iznad_oblaka_titles.py` potvrđuje:

- ugovor za naslov bloga, tagline i naslov posta na blog/detail rutama;
- punu lokalnu površinu;
- izolaciju od dizajna `zlatni_horizont`.

## Preostali nalazi iz Phase87a

Phase87b namjerno ne rješava:

- P1 kontrast kalendarske navigacije (1,01:1);
- P1 kontrast tijela posta, autora i akcija (3,84–4,24:1);
- P1 kontrast autora komentara (3,63:1) i arhive (4,45:1);
- P2 lokalni kalendarski overflow na 768 px (`177/150`, grid `161/118`);
- P2 tabletne/desktop touch mete i krhku širinu naslova posta na 320 px.
