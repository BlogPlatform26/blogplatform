# Phase 93b — sedmodnevni kalendar Sjene ulice (`sjene_ulice`)

## Polazište i promjena

Phase93a dokazao je da `sjene_ulice` prikazuje nazive dana i datume kao vertikalnu listu (`display:block`) na blogu i detalju pri 320/390/768/1440 px. Kalendar je bio visok približno 1321–1435 px, a na tabletu je imao lokalni horizontalni overflow 149/162 px.

Lokalni CSS teme sada za `.calendar-weekdays` i `.calendar-grid` izričito definira sedam stupaca `repeat(7,minmax(0,1fr))`. Mobilni razmak je 2 px, a dan s objavom visok najmanje 44 px. Na 768–991,98 px tri stupca stranice slažu se okomito; kalendar se može raširiti do 376 px, navigacija ima dva bočna stupca po 44 px, a dani najmanje 44×44 px. Desktopna fotografija, trostupčani raspored i boje nisu mijenjani.

## Stvarni preglednik

Izolirana sintetička baza s dva javna posta i komentarom posluživana je na zasebnom portu 8023. Bootstrap CSS bio je učitan (`.row` = `flex`). Blog i detalj pregledani su na 320/390/768/1440 px (**osam stanja**); vrijednosti su jednake za obje rute. `clientWidth/scrollWidth`:

| Širina | Kalendar prije → poslije, visina | Mreža poslije | Dan s objavom poslije | Dokument |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 1383 → 363 px | 201/201 px, sedam stupaca | oko 27×44 px | 305/320 px |
| 390 | 1383 → 363 px | 227/227 px, sedam stupaca | oko 31×44 px | 375/390 px |
| 768 | 1435 → 281 px | 351/351 px, sedam stupaca | oko 48×44 px | 753/768 px |
| 1440 | 1321 → 321 px | 227/227 px, sedam stupaca | oko 26×34 px | 1425/1440 px |

Tabletni kalendarski okvir sada je 375/375 px bez lokalnog overflowa. Nema dokumentnog overflowa na reprezentativnom naslovu „Sjene ulice”. Vizualni pregled potvrdio je ponovno čitljiv mjesečni raspored; fotografski identitet ostao je vidljiv. Na 390 px stvarni sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove. Like i komentar nisu mutirani.

## Ograničenja i provjera

Mobilni dani imaju 44 px visine, ali zbog samo 201/227 px prostora za sedam stupaca širina je oko 27/31 px. Nije postignuta puna meta 44×44 px; to ostaje P2. Desktop dan i strelica imaju oko 26×34 i 30×30 px. Shared tablet/desktop post-akcije ostaju 21–25 px. Lokalni višak sadržaja post-kartice i uski naslov komentara iz Phase93a nisu bili opseg ove promjene.

Foto-neovisan kontrast naslova, posta, autora, akcija, komentara i sidebara iz Phase93a ostaje P1. Dugi neprekinuti naslov bloga na 320/390 px također ostaje P1. Preostala dva neauditirana dizajna i završna matrica svih 37 nisu ovime zatvoreni.

Regresijski testovi `blog/test_phase93b_sjene_calendar_grid.py` provjeravaju blog i detalj te odsutnost lokalnih pravila u default dizajnu. Uski testovi 4/4, `manage.py check`, `makemigrations --check --dry-run` i puni Django skup 159/159 prošli su.
