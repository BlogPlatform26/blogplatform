# Phase 92b — sedmodnevni kalendar Dimnih akorda

## Polazište i zahvat

Phase92a potvrdio je da `.calendar-weekdays` i `.calendar-grid` u
`dimni_akordi` imaju computed `display:block`: dani su u jednom stupcu,
kalendarski okvir visok 1285–1385 px na provjerenim širinama. Linkovi su
radili, ali raspored nije bio upotrebljiv kao mjesečni kalendar.

Lokalno pravilo dizajna sada eksplicitno daje objema mrežama sedam
`minmax(0,1fr)` stupaca. Na 320/390 px dani su visoki 44 px; uži razmak
od 2 px i `min-width:0` sprečavaju preklapanje susjednih linkova. Na
768–991,98 px tri se stupca slažu vertikalno, kalendar dobiva do 376 px,
a dani i navigacija najmanje 44 px visine. Desktopni raspored s tri
stupca i panoramska fotografija na 1440 px ostaju.

## Stvarni browser rezultat

Izolirana sintetička SQLite baza s javnom objavom i komentarom posluživana
je na portu 8019. Bootstrap CSS bio je učitan (computed `.row` = `flex`).
Stvarni browser provjerio je blog i slugged detalj na 320/390/768/1440 px
(**osam stanja**); tablica vrijedi za obje rute. Brojevi su
`clientWidth/scrollWidth`.

| Širina | Kalendar prije → poslije, visina | Mreža poslije | Klikabilni dan poslije | Navigacija | Dokument |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 320 | 1309 → 310 px | 199/199 px, 7 stupaca | ~27×44 px | 44 px | 305/320 px |
| 390 | 1309 → 310 px | 227/227 px, 7 stupaca | ~31×44 px | 44 px | 375/390 px |
| 768 | 1385 → 282 px | 351/351 px, 7 stupaca | ~48×44 px | 44 px | 753/768 px |
| 1440 | 1285 → 286 px | 227/227 px, 7 stupaca | ~26×34 px | 30 px | 1425/1440 px |

Nema lokalnog horizontalnog overflowa kalendara ni dokumentnog overflowa.
Vizualno su pregledani mobilni i tabletni kalendar te desktop fotografija,
post i komentari. Stvarni sigurni klik prethodnog mjeseca na sve četiri
širine otvorio je `?year=2026&month=9`; klik dana s objavom na 768 otvorio
je `/post/1/vecer-akorda-i-dima/`, a arhiva očekivani
`?year=2026&month=10`. Like i komentar nisu mutirani.

## Otvorene granice

Mobilni dani su nepreklapajući i 44 px visoki, ali zbog 199/227 px široke
mreže imaju samo **27/31 px širine**, a ne 44×44 px. Za 44 px širine sedam
dana bi tražilo barem 308 px bez razmaka i unutarnjih margina, što ne
stane u postojeći mobilni sidebar na 320 px. To ostaje P2 za širi
pristupačni zahvat; ne tvrdimo da je puna 44×44 meta zatvorena. Desktopni
dani i strelice također ostaju manji od 44 px. Foto-neovisan kontrast
naslova, posta, akcija, komentara, upute i sidebara iz Phase92a ostaje P1.
Shared tablet/desktop post-akcijske mete nisu dirane.

`blog/test_phase92b_dimni_calendar_grid.py` provjerava lokalni CSS
ugovor na blogu i detalju te odsutnost pravila u default dizajnu. Uski
test, `manage.py check`, `makemigrations --check --dry-run`, `git diff
--check` i puni Django skup (153/153) prošli su završni gate. Izolirana baza, server
i browser uklonjeni su po završetku.
