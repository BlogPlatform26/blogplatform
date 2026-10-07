# Phase 95c2 — Asfaltni plamen: foto-neovisan naslov bloga

## Opseg

Phase95a utvrdio je da naslov/podnaslov bez podloge imaju 15,39:1 na tamnoj referentnoj zoni, ali matematički samo 1,22:1 nad potpuno svijetlom zonom dima. U ovoj uskoj fazi zaštićeni su **samo naslov i podnaslov bloga**, ne cijeli dizajn. Provjera prije promjene na blogu i detalju pri 390 i 1440 px potvrdila je prozirnu podlogu i podnaslov opacity 0,82.

Lokalni CSS daje tekstu usku, neprozirnu toplu podlogu `#21140e`, zadržava postojeći topli tekst `#f4e7d8` te podnaslov prikazuje punom neprozirnošću. Panoramska fotografija automobila ostaje izložena oko naslovnih površina; nema pune tamne trake preko fotografije. Dugi neprekinuti naslov može se prelomiti unutar površine.

## Stvarni preglednik

Izolirana migrirana SQLite baza s autorom, podnaslovom, dvije javne objave u različitim mjesecima i komentarom posluživana je na portu 8029. Bootstrap je učitan (`.row` = `flex`). Nakon promjene pregledani su blog i detalj na 320/390/768/1440 px (**osam stanja**). Computed naslov, poveznica naslova i podnaslov imaju tekst `rgb(244,231,216)` na neprozirnoj podlozi `rgb(33,20,14)`, odnosno **14,75:1**. Podnaslov ima opacity 1. Budući da je podloga neprozirna, omjer ne ovisi o svijetlom ili tamnom foto-kadru; nije izveden iz izabrane tamne fotografijske točke.

| Širina | Dokument client/scroll | Kalendar client/scroll | Grid client/scroll |
| ---: | ---: | ---: | ---: |
| 320 | 305/305 | 231/231 | 199/199 |
| 390 | 375/375 | 301/301 | 269/269 |
| 768 | 753/753 | 375/375 | 351/351 |
| 1440 | 1425/1425 | 259/259 | 227/227 |

Vrijednosti su jednake na blogu i detalju. Vizualni pregled na 1440 i 390 px potvrdio je očuvanu automobilsku panoramu i mobilni raspored. Zaseban sintetički slučaj s neprekinutim dugim naslovom na 320 px imao je naslov client/scroll 257/257 i dokument 305/305. Na 390 px sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove; like i komentari nisu mutirani.

## Provjera i otvoreno

Regresijski test provjerava lokalna pravila na blogu i detalju te da se ne pojavljuju u `default` dizajnu. Uski testovi 2/2, `manage.py check` i `makemigrations --check --dry-run` prošli su. Puni Django skup: **177/177**.

Foto-neovisan kontrast post naslova/tijela/autora/ostalih akcija, teksta/autora komentara, arhive i bočnih kartica **nije** zatvoren ovom fazom. Phase95a je izmjerio autora desktop komentara samo 3,81:1 čak na tamnoj referentnoj zoni. Uski 320 px post/komentar te mobilni kalendarski dani i tablet/desktop dodirne mete ostaju otvoreni. Ova faza ne potvrđuje ukupni kontrast svih 37 dizajna. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
