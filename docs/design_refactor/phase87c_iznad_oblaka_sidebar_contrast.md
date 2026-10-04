# Phase 87c — Iznad oblaka: kontrast sidebar navigacije

## Opseg

Phase 87c popravlja samo kalendarske strelice i arhivsku poveznicu u dizajnu
`iznad_oblaka`. Ne mijenja druge P1 kontraste, tabletni raspored, post-action
mete, shared CSS ni Phase87b naslovne površine.

## Promjena

Obje mete koriste tamnu lokalnu tintu `#514956` na punoj pastelnoj površini
`#fff7fc`, uz diskretan unutarnji rub. Površina je foto-neovisna i zadržava
postojeće dimenzije kontrola, zaobljenja i raspored.

## Kontrast i stvarni preglednik

Phase87a izmjerio je 1,01:1 za kalendarsku navigaciju i 4,45:1 za arhivsku
poveznicu. Nakon Phase87c obje mete imaju **8,19:1**.

Blog i detail prikaz provjereni su na 320, 390, 768 i 1440 px, ukupno osam
stanja. Puna lokalna površina daje isti alpha-komponirani rezultat na stvarnom
svijetlom i tamnom dijelu svakog responsive cropa. Vizualni pregled na 390 i
1440 px potvrdio je očuvanu pastelnu fotografiju, desktop identitet i Phase87b
naslove.

Fizički dokumentni overflow ostaje `0 px`. Postojeći lokalni kalendarski
overflow na 768 px ostaje `177/150 px`, uz grid `161/118 px`, jer je geometrija
izvan opsega. Sigurni klikovi `Prethodni mjesec` i arhivska poveznica prošli su
bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase87c_iznad_oblaka_sidebar_contrast.py` potvrđuje:

- kalendarski i arhivski lokalni ugovor na blog/detail rutama;
- stabilnu tintu i punu pastelnu površinu;
- izolaciju od dizajna `zlatni_horizont`.

## Preostali nalazi

Phase87c namjerno ne rješava:

- P1 tijelo posta, autora i post akcije (3,84–4,24:1);
- P1 autora komentara (3,63:1);
- P2 kalendarski overflow na 768 px;
- P2 tabletne/desktop touch mete i krhku širinu naslova posta na 320 px.
