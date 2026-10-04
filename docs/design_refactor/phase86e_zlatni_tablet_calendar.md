# Phase 86e — Zlatni horizont: tabletni kalendar

## Opseg

Phase 86e uklanja lokalni overflow kalendara u dizajnu `zlatni_horizont` samo
između 768 i 991,98 px. Mobilni raspored na 320/390 px, desktopna tri stupca na
1440 px, shared tablet post-action P2 i Phase 86b/c/d kontrastna pravila nisu
mijenjani.

## Početno stanje

Phase 86a izmjerio je na 768 px grid `169/117 px` i sadržaj kalendara
`185/149 px` (`scrollWidth/clientWidth`). Četvrtinski lijevi stupac nije mogao
smjestiti sedam dana bez lokalnog preljeva.

## Promjena

Na tablet rasponu lijevi kalendarski rail i sadržaj koriste po 50% retka, dok
se desni profilni rail prelama u puni sljedeći red. Kalendar je ograničen na
376 px, s kompaktnim paddingom i sedam stupaca minimalne širine 44 px. Razmaci
između dana uklonjeni su samo na tabletu, a današnji dan zadržava vertikalni
naglasak bez skaliranja koje bi stvaralo zadnji piksel preljeva.

Ništa se ne skriva i klikabilni dani nisu smanjeni.

## Stvarni preglednik

Blog i detail prikaz provjereni su na 320, 390, 768 i 1440 px, ukupno osam
stanja. Konačno mjerenje na 768 px za obje rute:

- kalendar: `321/321 px`;
- grid: `311/311 px`;
- lijevi rail: `344/344 px`;
- minimalni dan: `44 × 44 px`;
- dokumentni overflow: `0 px`.

Mobilna geometrija ostala je na postojećem rasporedu, uključujući poznato
jednopikselno grid zaokruživanje unutar potpuno sadržanog kalendara. Desktopni
raspored ostao je tri stupca, uz kalendar i grid bez overflowa. Vizualni pregled
320/390, 768 i 1440 px potvrdio je očuvanu fotografiju i Phase 86b/c/d izgled.

Sigurni klikovi `Prethodni mjesec`, kalendarski dan s postom i `Otvori post`
prošli su bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase86e_zlatni_tablet_calendar.py` potvrđuje tabletni media ugovor,
sedam minimalnih 44 px stupaca, 44 px visinu dana, uklonjeni gap i izolaciju od
dizajna `iznad_oblaka`.
