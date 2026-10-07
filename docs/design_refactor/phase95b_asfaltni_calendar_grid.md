# Phase 95b — sedmodnevni kalendar Asfaltni plamen (`asfaltni_plamen`)

## Polazište i promjena

Phase95a je u stvarnom pregledniku pokazala `display:block` za `.calendar-weekdays` i `.calendar-grid` na blogu i detalju pri 320/390/768/1440 px. Mjesečni prikaz bio je vertikalna lista visoka 1054–1064 px, a cijeli kalendar 1285–1385 px. Ova faza lokalno vraća sedam stupaca `repeat(7, minmax(0, 1fr))`. Na mobitelu je razmak 2 px i visina dana s objavom najmanje 44 px. Na tabletu se stupci stranice slažu okomito, kalendar se može raširiti na 376 px, a navigacija i dani ostaju bez lokalnog horizontalnog preljeva. Fotografija automobila i desktopni karakter nisu mijenjani.

## Stvarni preglednik

Izolirana migrirana SQLite baza s dva javna posta u različitim mjesecima i komentarom posluživana je na portu 8027. Bootstrap je bio učitan (`.row` = `flex`). Blog i detalj provjereni su na 320/390/768/1440 px, ukupno osam stanja. Vrijednosti su jednake za obje rute; parovi su `clientWidth/scrollWidth`.

| Širina | Kalendar prije → poslije, visina | Mreža poslije | Dan s objavom poslije | Dokument poslije |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 1309 → 289 px | 199/199 px, sedam stupaca | oko 27×44 px | 305/305 px |
| 390 | 1309 → 289 px | 269/269 px, sedam stupaca | oko 37×44 px | 375/375 px |
| 768 | 1385 → 281 px | 351/351 px, sedam stupaca | oko 48×44 px | 753/753 px |
| 1440 | 1285 → 285 px | 227/227 px, sedam stupaca | oko 26×34 px | 1425/1425 px |

Na 768 px kalendarski okvir je 375/375 px, navigacija 351/351 px, bez lokalnog preljeva. Vizualno su pregledani mobilni, tabletni i desktopni prikaz; panoramska fotografija je očuvana. Na 390 px stvarni sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove (`?year=2026&month=9`, `/post/1/nocna-voznja-kroz-grad/`, `?year=2026&month=9`). Like i komentari nisu mutirani.

## Granica faze i provjera

Sedmodnevni raspored i visina mobilnog dana od 44 px jesu postignuti, ali širina dana na 320/390 px iznosi samo oko 27/37 px; puna meta 44×44 px nije postignuta. Desktop dan ostaje oko 26×34 px. To i ostale tablet/desktop post-akcije ostaju P2. Foto-neovisan kontrast naslova, posta, komentara i sidebara, kao i uski mobilni post/komentar, ostaju otvoreni P1/P2 iz Phase95a. Ova faza ih ne proglašava riješenima.

Regresijski test `blog/test_phase95b_asfaltni_calendar_grid.py` provjerava blog i detalj te izolaciju pravila od default dizajna. Uski testovi 2/2, `manage.py check`, `makemigrations --check --dry-run` i puni Django skup 173/173 prošli su. Izvorni `db.sqlite3`, mediji, port 8000, `main` i produkcija nisu korišteni.
