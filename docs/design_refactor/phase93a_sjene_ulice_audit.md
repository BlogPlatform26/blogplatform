# Phase 93a — audit Sjene ulice (`sjene_ulice`)

## Opseg

Izolirana migrirana SQLite baza sadržavala je autora s dizajnom `sjene_ulice`, naslovom i podnaslovom bloga, dvije javne objave u različitim mjesecima te komentar drugog korisnika. Stvarni preglednik provjerio je blog i detalj na 320, 390, 768 i 1440 px (**osam stanja**) uz učitan Bootstrap (`.row` = `flex`). Pregledane su gradska fotografija, kartica objave, komentar, kalendar i arhiva. Nisu mijenjani izvršni kod, izvorni `db.sqlite3`, mediji ni port 8000; like i druge mutirajuće kontrole nisu kliknute.

`manage.py check`, `makemigrations --check --dry-run` i puni Django skup (157/157) prošli su. Faza je samo audit: ne mijenja izgled ni funkcionalnost.

## P1 — kalendar je vertikalna lista

Na svih osam prikaza computed `.calendar-weekdays` i `.calendar-grid` imaju `display:block`, umjesto sedmodnevne mreže. Sedam naziva dana i 31 datum idu jedan ispod drugoga. Kalendar je visok približno 1383/1383/1435/1321 px na 320/390/768/1440 px; sama lista dana oko 1064 px (1054 desktop). Na 768 px okvir lokalno prelijeva `149/162 px` (`clientWidth/scrollWidth`) i navigacija se lomi. Ovo je vidljiv P1 rasporeda, a ne samo brojčani višak.

| Širina | Dokument / viewport | Kalendar client/scroll | Mreža client/scroll | Dan s objavom |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 305/320 | 233/233 | 201/201 | 44×44 px |
| 390 | 375/390 | 259/259 | 227/227 | 44×44 px |
| 768 | 753/768 | 149/162 | 117/117 | 44×44 px |
| 1440 | 1425/1440 | 259/259 | 227/227 | 227×34 px, jer nema mreže |

## P1 — nedostatan i foto-ovisan kontrast

Computed kartica objave, kalendar, arhiva i bočne kartice imaju samo `rgba(19,16,14,.34)` preko fotografije. Naslov i podnaslov su prozirni. Komentar je na 320/390 dodatno 8% svijetli sloj, a na 768/1440 34% bijeli sloj. Sljedeći omjeri izračunati su kompozicijom computed boja na tamnoj osnovi `#161210` te na krajnje svijetloj mogućoj zoni `#ffffff`. Svijetla granica nije tvrdnja da je konkretan foto-piksel bijel; pokazuje da prozirni slojevi ne jamče čitljivost pri promjeni kadra. Sjena teksta nije uračunana kao pouzdana pozadina.

| Element | Tamna osnova | Svijetla granica |
| --- | ---: | ---: |
| naslov bloga `#ff9500`, bez podloge | 8.47:1 | 2.20:1 |
| podnaslov, ista boja s opacity .82 | 6.02:1 | 1.93:1 |
| naslov posta `#ff8000` na kartici .34 | 7.44:1 | 1.13:1 |
| tijelo posta `#ece1d7` na kartici .34 | 14.56:1 | 1.73:1 |
| autor i akcijske poveznice `#d8b084` | 9.33:1 | 1.11:1 |
| Bootstrap like `#0d6efd` | **4.16:1** | 2.03:1 |
| komentar na desktopu, bijeli sloj .34 | 6.05:1 | 1.65:1 |
| autor komentara na desktopu | **3.01:1** | 1.22:1 |
| mobilni tekst komentara, sloj .08 | 15.77:1 | 2.12:1 |
| mobilni autor komentara | 7.86:1 | 1.05:1 |
| anonimna uputa, 68% svijetli tekst | 7.16:1 | 1.47:1 |
| kalendarski naslov preko kartice | 7.51:1 | 1.12:1 |
| kalendarska strelica, dodatnih 26% bijele | **3.25:1** | 1.41:1 |
| arhivska veza, dodatnih 2% bijele | 9.65:1 | 1.60:1 |

Like, autor desktop komentara i kalendarska strelica ne prolaze 4,5:1 već na tamnoj osnovi. Foto-neovisnu zaštitu naslova, posta, komentara, upute i sidebara treba izvesti bez gubitka gradske panorame i tamnog desktop karaktera.

## Uski naslov i dodirne mete

Za reprezentativan naziv „Sjene ulice” u svih osam stanja nema dokumentnog horizontalnog overflowa; `documentElement.scrollWidth` je 15 px ispod `innerWidth` zbog trake za pomicanje. Međutim, zaseban stres-prolaz s neprekinutim naslovom `phase93aauthor` pokazao je **542/320 i 542/390 px** dokumentnog overflowa: naslov na 320 px imao je `scrollWidth` 518 u 257 px. To je potvrđen P1 uskog zaglavlja za dopušteni dugi naziv/fallback username, a ne nalaz iz reprezentativnog kratkog naslova.

Na 320/390 px sama post-kartica ima lokalni `scrollWidth` 347 px u okviru od 209/279 px. Pregled je pokazao da su veliki naslov objave i posebno naslov „Komentari” stisnuti/prekinuti; komentar je čitljiv, ali mu je tekst uzak (oko 106 px na 320 px). To je P2 geometrije za zaseban popravak. Mobilni like, akcijske veze, arhiva, kalendarska strelica i dan s objavom imaju oko 44 px visine. Na 768/1440 px like je 25 px, akcijske veze 21 px; desktop kalendarska strelica 30 px i arhiva 34 px. Te touch mete ostaju P2.

## Sigurni klikovi i sljedeći koraci

Na 390 px klik `Prethodni mjesec` otvorio je `?year=2026&month=9`, dan s objavom `14` otvorio je njezin detalj, a arhivska veza za listopad vratila očekivanu objavu. Like/komentar nisu mutirani.

1. Vratiti sedmodnevnu kalendarsku mrežu na svim širinama, s 44 px mobilnim danima i bez tabletne regresije.
2. Odvojeno osigurati foto-neovisan kontrast i potvrđene nedostatke likea, autora komentara i strelica, uz pregled oba prikaza na sve četiri širine.
3. Riješiti dugi neprekinuti naziv bloga i usko zaglavlje/komentar bez promjene desktop identiteta.

`mjesecev_ples` i `asfaltni_plamen` još čekaju pojedinačni audit. Kraljevska sidebar foto-varijacija i zajedničke tablet/desktop dodirne mete ostaju otvorene. Završna matrica svih 37, uključujući kontrast komentara na fotografijama, još nije gotova.
