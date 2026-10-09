# Phase 99b — kontrast autorske poveznice u šest osnovnih varijanti

Phase 99a potvrdila je efektivni kontrast autorske poveznice ispod 4,5:1 u `default`, `dark`, `classic` i njihovim desnim varijantama. Uzrok je bila neprozirnost `.post-author-link` od 0,8 odnosno 0,6, koja je ublažavala inače dovoljno kontrastnu boju teme. Lokalno, samo za tih šest registriranih ključeva, neprozirnost je sada 1. Boje, tipografija, kartice, fotografije i raspored nisu mijenjani. Tri `simple_*` varijante nisu zahvaćene jer je njihov prethodni rezultat konzervativna foto-granica, a ne potvrđen pikselni pad.

| Varijante | Prije, najmanje | Poslije, najmanje |
| --- | ---: | ---: |
| `default`, `default_right` | 4,16:1 | **5,78:1** |
| `dark`, `dark_right` | 3,29:1 | **7,19:1** |
| `classic`, `classic_right` | 3,93:1 | **5,34:1** |

Izolirana migrirana sintetička baza sadržavala je po autora, objavu i komentar za svih šest dizajna. Chrome/Playwright s učitanim Bootstrapom ponovio je blog i detalj na 320/390/768/1440 px (**48 stanja**). Omjeri su računati iz stvarnih computed boja poveznice i neprozirne podloge objave, uključujući efektivnu neprozirnost predaka; najmanji je naveden u tablici. Nigdje nije bilo document ni lokalnog horizontalnog overflowa post kartice, komentara ili kalendara. Tabletna akcijska poveznica ostala je najmanje 44 px visoka. Snimke osnovne, tamne i klasične teme na 320 px pregledane su vizualno; desktop identitet ostaje. Sigurni klikovi za otvaranje objave prošli su za svih šest blogova na 390 px, a ciljna autorska poveznica dodatno 12/12 puta na 390/1440 px, bez mutacije sadržaja.

Uski Django test 2/2, `manage.py check`, `makemigrations --check --dry-run` i puni suite **201/201** prošli su bez pogreške. Ova faza ne zaključuje da su `simple_*` autorske poveznice ili kalendarski gradijent osnovne teme verificirani, niti da je završna matrica svih 37 dovršena.
