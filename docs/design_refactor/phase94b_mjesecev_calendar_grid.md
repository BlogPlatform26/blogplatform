# Phase 94b — sedmodnevni kalendar Mjesečeva plesa (`mjesecev_ples`)

## Polazište i promjena

Phase94a potvrdio je da blog i detalj Mjesečeva plesa na 320/390/768/1440 px prikazuju nazive dana i datume kao vertikalnu listu (`display:block`), visoku oko 1285–1385 px. U lokalni CSS teme dodana je izričita sedmostupčana mreža `repeat(7,minmax(0,1fr))` za nazive dana i datume, s istim razmakom radi poravnanja.

Mobilni dan s objavom zadržao je 44 px visine. Na 768–991,98 px tri glavna stupca slažu se okomito, a kalendar se može proširiti do 376 px; navigacija i dani imaju najmanje 44 px visine. Desktopna fotografija, boje i trostupčani raspored na 1440 px nisu mijenjani. Pravila su samo u predlošku `mjesecev_ples`.

## Stvarni preglednik

Izolirana sintetička migrirana baza s javnom objavom i komentarom bila je posluživana na zasebnom portu 8028. Bootstrap se učitao (`.row` = `flex`). Blog i detalj pregledani su na sve četiri širine (**osam stanja**); vrijednosti su jednake za obje rute. `clientWidth/scrollWidth`:

| Širina | Kalendar prije → poslije, visina | Mreža poslije | Dan s objavom poslije | Dokument poslije |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 1309 → 289 px | 199/199 px, sedam stupaca | oko 27×44 px | 305/305 px |
| 390 | 1309 → 289 px | 227/227 px, sedam stupaca | oko 31×44 px | 375/375 px |
| 768 | 1385 → 281 px | 351/351 px, sedam stupaca | oko 48×44 px | 753/753 px |
| 1440 | 1285 → 285 px | 227/227 px, sedam stupaca | oko 26×34 px | 1425/1425 px |

Tabletni kalendarski okvir sada je 375/375 px, bez lokalnog overflowa. Tjedna zaglavlja i datumi imaju istih sedam stupaca i jednak razmak. Vizualni pregled potvrdio je čitljiv mjesečni raspored s očuvanom noćnom fotografijom. Na 390 px stvarni klikovi `Prethodni mjesec`, dana s objavom `7` i arhive otvorili su odgovarajuće rute; like i komentar nisu mutirani.

## Provjera i otvoreni nalazi

Regresijski testovi `blog/test_phase94b_mjesecev_calendar_grid.py` provjeravaju blog i detalj te izolaciju lokalnih pravila od default dizajna. Uski testovi (2/2), `manage.py check`, `makemigrations --check --dry-run` i puni Django skup (169/169) prošli su bez pogreške.

Zbog prostora za sedam stupaca u mobilnom sidebaru dani su široki samo 27/31 px, premda su visoki 44 px; puni 44×44 dodirni cilj ostaje P2. Desktop dan/strelica te zajedničke tablet/desktop post-akcije također ostaju P2. Phase94a P1 foto-neovisan kontrast naslova, posta, komentara i sidebara te potvrđeni like 4,16:1 i autor desktop komentara 3,88:1 **nisu** riješeni ovom fazom. Uski naslov/komentar na 320 px ostaju za zasebnu geometrijsku provjeru. `asfaltni_plamen` još nije auditiran, a završna matrica svih 37 nije gotova.
