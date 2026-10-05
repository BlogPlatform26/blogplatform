# Phase 87e — Iznad oblaka: tabletni kalendar u sidebaru

## Opseg

Phase 87e rješava samo stvarni lokalni overflow kalendara dizajna
`iznad_oblaka` između 768 i 991,98 px. Ne mijenja shared mobilna pravila,
podatke, postove, kontrastne površine iz Phase87b/c/d ni desktop i mobilni
raspored.

## Uzrok i promjena

Globalno mobilno pravilo daje linku dana s objavom `min-width: 44px !important`.
U tablet sidebaru s 118 px sadržajne širine to je prisililo prvu od sedam grid
kolona na 44 px i proizvelo lokalni overflow.

Lokalni media query zato vrijedi samo za tabletni raspon: kalendar dobiva manje
unutarnje rubove, naslov se raspoređuje u tri kontrolirane grid kolone, a
kalendar i dani koriste sedam `minmax(0, 1fr)` kolona s manjim razmakom. Za
link dana se samo u tom uskom rasponu poništava prisilna minimalna širina.
Strelice prethodnog/sljedećeg mjeseca ostaju 44 × 44 px.

## Stvarni preglednik

Prije promjene na 768 px blog ruta imala je kalendar `176/150 px`
scroll/client i grid `160/118 px`. Nakon promjene blog i detail ruta imaju
kalendar `150/150 px` i grid `134/134 px`; fizički document overflow ostaje
`0 px`.

Provjereni su blog i detail na 320, 390, 768 i 1440 px, ukupno osam stanja.
Na 320/390 px ostaju mobilne mete (dan približno 45,76 px širok, strelica
44 × 44 px), a na 1440 px ostaju postojeće desktop dimenzije (dan približno
28,52 × 35,36 px i strelica 30 × 30 px). Samo na 768 px dani ravnomjerno
stanu u sidebar (oko 18,15 × 35,36 px), dok strelice ostaju 44 × 44 px.
To je namjerni prostorni kompromis za uski postojeći tabletni sidebar; veće
tabletne touch mete ostaju zaseban P2 layout zadatak.

Vizualni pregled na 768 px potvrdio je uredan kalendar bez lokalnog izlaska iz
sidebara. Sigurni klikovi `Prethodni mjesec` i dana s objavom otvorili su
očekivani mjesečni query odnosno slugged detail, bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase87e_iznad_oblaka_calendar_fit.py` potvrđuje:

- lokalni tabletni CSS ugovor na blog i detail rutama;
- tri kontrolirane navigacijske kolone i shrink-safe grid;
- izolaciju od dizajna `zlatni_horizont`.

## Preostali nalazi

Preostaju P2 tabletne/desktop touch mete za kalendarske dane i post akcije te
krhka širina naslova posta na 320 px. Phase87e ih namjerno ne širi u ovaj
geometrijski popravak.
