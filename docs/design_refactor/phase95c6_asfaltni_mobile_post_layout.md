# Phase 95c6 — Asfaltni plamen: uski naslov objave i komentar

## Uzrok i promjena

Phase95a je na 320 px našao uski naslov i komentar bez document overflowa. Stvarni preglednik s učitanim Bootstrapom potvrdio je da tri uzastopna mobilna uvlaka (`.blog-main-layout-row`, sadržajni stupac i `.blog-posts-shell`) ostavljaju kartici objave samo 224 px. Unutarnjih 24 px bočnog paddinga, paralelni datumski blok te avatar i razmak komentara potom ostavljaju naslovu 82 px, a tekstu komentara 90 px. Pregled s neuspjelim CDN učitavanjem odbačen je kao nevažeći baseline.

Lokalno samo za `asfaltni_plamen` ispod 576 px sadržajni stupac i shell uklanjaju suvišno bočno uvlačenje, kartica koristi 14 px bočnog paddinga, datum dolazi ispod naslova, a avatar iznad komentara. Naslov i autor komentara mogu lomiti dugačke neprekinute riječi. Boje, neprozirna zaštita kontrasta i panoramska fotografija nisu mijenjani; pravila za 768/1440 px ostaju netaknuta.

## Stvarni preglednik

Izolirana migrirana sintetička SQLite baza sadržavala je autora, dvije javne objave u različitim mjesecima i komentar drugog korisnika. Lokalni server radio je na portu 8033; Bootstrap CDN je uspješno učitan (`.blog-header-wrap > .row` ima computed `display:flex`). Blog i detalj pregledani su prije i poslije pri 320/390/768/1440 px, ukupno osam stanja po prolazu.

| Širina | Kartica prije → poslije | Naslov prije → poslije | Tekst komentara prije → poslije |
| --- | ---: | ---: | ---: |
| 320 px | 224 → 272 px | 82 → 242 px | 90 → 212 px |
| 390 px | 294 → 342 px | 152 → 312 px | 160 → 282 px |
| 768 px | 656 → 656 px | 514 → 514 px | 444 → 444 px |
| 1440 px | 609 → 609 px | 467 → 467 px | 397 → 397 px |

Na 320 px obični naslov pada sa 113 na 57 px visine, na 390 px s 57 na 28 px. Document overflow je **0** na blogu i detalju pri sve četiri širine; kartica, naslov i komentar nakon izmjene nemaju lokalni vodoravni overflow. Sintetički dugačak neprekinuti naslov i korisničko ime na 320/390 px također imaju 0 px document/title/author overflowa. Vizualno su pregledani mobilni tekst i desktop automobilska panorama; desktop raspored ostao je jednak.

Sigurni klikovi prethodnog mjeseca, dana s objavom i arhive na svih osam stanja otvorili su očekivane lokalne URL-ove. Broj likeova ostao je 0, komentara 1; ništa od toga nije mutirano klikovima.

## Testovi i otvoreno

Lokalni regresijski test potvrđuje pravilo na blogu i detalju te njegov izostanak u `default` dizajnu: 2/2. `manage.py check`, `makemigrations --check --dry-run` i puni Django skup **187/187** su zeleni. Izolirana baza, server i privremeni preglednički artefakti uklonjeni su nakon provjere.

Otvorene su P2 mete: pojedini mobilni kalendarski dani drugih dizajna široki 27/31 px i zajedničke tablet/desktop post-action kontrole od 21–25 px. Radni indeks 37 dizajna nije završna matrica koja dokazuje kontrast komentara i fotografskih zona svih dizajna. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
