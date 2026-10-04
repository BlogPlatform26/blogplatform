# Phase 86d — Zlatni horizont: kontrast naslova i taglinea

## Opseg

Phase 86d foto- i crop-neovisno štiti samo naslov bloga i tagline u dizajnu
`zlatni_horizont`. Ne mijenja Phase 86c površine naslova i tijela posta, Phase
86b kontrole kartice niti poznati tabletni P2 raspored.

## Promjena

Naslov i tagline dobili su zasebne kompaktne površine `#1b0d07`, prilagođene
stvarnoj širini teksta, s malim unutarnjim razmakom, zaobljenjem i blagom
sjenom. Puna lokalna površina uklanja ovisnost o svijetlim i tamnim dijelovima
fotografije, dok ostatak neba, zalazak i refleksija ostaju nepokriveni.

## Kontrast i stvarni preglednik

Phase 86a zabilježio je minimum 2,06:1 za naslov i 1,45:1 za tagline. Nakon
promjene oba cilja imaju efektivni kontrast **16,92:1**, s velikom marginom
iznad cilja 4,5:1.

Provjereni su blog i detail prikaz na 320, 390, 768 i 1440 px, ukupno osam
stanja. U svim stanjima dobivena je puna površina `rgb(27, 13, 7)`, bez
dokumentnog overflowa. Vizualni pregled na 390 i 1440 px potvrdio je da su
površine kompaktne i da sunset desktop kompozicija ostaje prepoznatljiva.

Phase 86c post površina ostala je `rgb(27, 13, 7)`. Poznati lokalni tabletni
calendar omjer 169/117 px na 768 px nije mijenjan. Sigurne navigacije `Otvori
post` i `Prethodni mjesec` prošle su bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase86d_zlatni_header_contrast.py` potvrđuje:

- Phase 86d ugovor na blog i detail prikazu;
- ciljane selektore za naslov i tagline;
- izolaciju od dizajna `iznad_oblaka`.

Završni gateovi uključuju ciljane testove, `manage.py check`, provjeru migration
drifta i puni Django test suite.
