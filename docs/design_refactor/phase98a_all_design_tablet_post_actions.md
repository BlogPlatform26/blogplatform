# Phase 98a — tabletne akcijske mete za svih 37 dizajna

## Uzrok i opseg

Zajednički `post_actions.html` prikazuje lajk kao tipku, a komentar i otvaranje objave kao poveznice. Prethodno pravilo od najmanje 44px na 576–991.98px bilo je ograničeno na devet osnovnih dizajna. U reprezentativnim prilagođenim dizajnima na 768px poveznice su bile visoke 21px, a tipka 26px. Jednako tabletno pravilo sada dolazi iz zajedničkog `base.html` i vrijedi za sve registrirane dizajne. Ne mijenja mobitel do 575.98px ni desktop od 992px naviše.

## Stvarni preglednik

U izoliranoj migriranoj sintetičkoj SQLite bazi napravljeni su objava i autor za svaki od 37 ključeva. Chrome/Playwright s učitanim Bootstrap CDN-om provjerio je blog i detalj svakog dizajna na 768px: **74/74 stanja** imaju lajk i vidljive akcijske poveznice visoke najmanje 44px te `documentElement.scrollWidth == clientWidth`. Na 37 blog-stranica sigurno je kliknuto „Otvori post”, bez slanja lajka ili komentara. Dodatnih 36 mobilnih/desktop stanja u šest reprezentativnih dizajna (ukupno 110) potvrdilo je da su postojeće mobilne mete zadržane i da je 1440px geometrija ostala 21px poveznica/26px tipka. Pregledane su snimke osnovnog i automobilskog dizajna na 768/1440; panoramski desktop izgled ostaje isti.

Odvojeni nalaz, **ne uzrokovan tablet pravilom**: sintetički dugački neprekinuti naslovi bloga na 320px prelijevaju se u `vodopad_u_magli` (376/320px) i `mjesecev_ples` (331/320px). DOM dijagnostika označila je `.blog-link` naslov, ne akcijske kontrole. To ostaje otvoreno za zaseban mobilni popravak. Desktop akcijske mete i pojedine kalendarske mete također ostaju zaseban P2 zadatak.

## Testovi

Novi regresijski test prolazi kroz svih 37 dizajna na blogu i detalju. Uski test 1/1, `manage.py check`, `makemigrations --check --dry-run` i puni Django suite **198/198** su zeleni. Izvorni `db.sqlite3`, `media`, port 8000, `main` i produkcija nisu dirani.
