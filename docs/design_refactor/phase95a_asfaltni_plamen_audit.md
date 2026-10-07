# Phase 95a — audit Asfaltni plamen (`asfaltni_plamen`)

## Opseg i metoda

Izolirana migrirana SQLite baza sadržavala je autora s dizajnom `asfaltni_plamen`, naslovom i podnaslovom bloga, dvije objave u različitim mjesecima te komentar drugog korisnika. Stvarni preglednik provjerio je blog i detalj objave na 320, 390, 768 i 1440 px (osam stanja), uz učitan Bootstrap (`.row` = `flex`). Pregledani su naslov, panoramska fotografija, post, komentar, kalendar, arhiva i bočne kartice. Ova faza mijenja samo dokumentaciju, ne izgled ni izvršni kod.

`manage.py check`, `makemigrations --check --dry-run` i puni Django skup prošli su (171/171). Izvorni `db.sqlite3`, mediji, port 8000, `main` i produkcija nisu korišteni.

Kontrast je izračunat iz computed boja i alfa-kompozicije svih roditeljskih podloga na tamnoj osnovi `#17110d` te na krajnje svijetloj mogućoj zoni `#ffffff`. Svijetla vrijednost **granica je osjetljivosti na fotografiju**, a ne mjerenje bijelog piksela postojeće fotografije. Vizualni desktop pregled potvrđuje da se u kadru izmjenjuju gotovo crn automobil/tlo i svijetao dim. Tekstualna sjena nije računata kao stabilna kontrastna podloga.

## P1 — kalendar nije sedmodnevna mreža

Computed `.calendar-weekdays` i `.calendar-grid` imaju `display:block` na blogu i detalju na sve četiri širine. Dani u tjednu i datumi prikazuju se jedan ispod drugoga; grid je visok 1054–1064 px, a cijeli kalendar 1285–1385 px. Nema horizontalnog document ni lokalnog overflowa u reprezentativnom sadržaju, ali je mjesečni prikaz funkcionalno nečitljiv kao kalendar.

| Širina | Dokument client/scroll | Kalendar client/scroll; visina | Grid client/scroll | Dan s objavom |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 305/305 | 231/231; 1309 px | 199/199 | 44×44 px |
| 390 | 375/375 | 259/259; 1309 px | 227/227 | 44×44 px |
| 768 | 753/753 | 147/147; 1385 px | 115/115 | 44×44 px |
| 1440 | 1425/1425 | 259/259; 1285 px | 227/227 | 227×34 px |

Ove vrijednosti jednake su na blogu i detalju. Na 768 px uzani bočni stupac dodatno otežava kalendarsku navigaciju, iako njezin horizontalni okvir ne prelijeva dokument.

## P1 — kontrast nije foto-neovisan

Naslov i podnaslov bloga nemaju neprozirnu podlogu. Kartica posta, kalendar, arhiva i bočne kartice koriste `rgba(24,17,13,.20)` preko fotografije; komentar na desktopu dodatno ima 34% bijeli sloj. Dobiveni računski omjeri:

| Element | Tamna osnova | Svijetla granica |
| --- | ---: | ---: |
| naslov/podnaslov bloga | 15,39:1 | 1,22:1 |
| naslov objave | 16,32:1 | 1,35:1 |
| tijelo objave | 14,95:1 | 1,24:1 |
| autor i obične akcijske veze | 11,80:1 | 1,02:1 |
| Bootstrap like `#0d6efd` | **4,16:1** | 2,91:1 |
| tekst komentara na 768/1440 | 4,83:1 | 1,06:1 |
| autor komentara na 768/1440 | **3,81:1** | 1,20:1 |
| tekst/autor komentara na 320/390 | 14,95 / 11,80:1 | 1,24 / 1,02:1 |
| anonimna uputa | 7,92:1 | 1,15:1 |
| kalendarski naslov | 10,15:1 | 1,19:1 |
| kalendarska strelica | **4,40:1** | 1,34:1 |
| dan s objavom / današnji dan | **4,41:1** | 2,69:1 |
| arhivska veza | 11,61:1 | 1,32:1 |
| tekst bočne kartice | 7,92:1 | 1,15:1 |

Like, autor desktop komentara, kalendarska strelica i dan s objavom ne dosežu 4,5:1 već na tamnoj referentnoj osnovi. Bijela granica pokazuje da prozirni slojevi ne mogu jamčiti čitljivost pri promjeni foto-kadra. Potrebna je lokalna zaštita uz očuvanje automobilskog kadra i toplog tamnog desktop identiteta. Jedna profilna veza ima vlastitu svijetlu podlogu i nije dokaz da ostatak sidebara prolazi.

## P2 — geometrija i dodirne mete

Na 320 px naslov objave ima unutarnji `scrollWidth` 69 px u širini 67 px, bez dokumentnog preljeva; na 390 px je 137/137 px. Komentar je vrlo uzak: okvir 104 px na 320 px te 174 px na 390 px, s prelomljenom rečenicom riječ po riječ. Kartica objave ne prelijeva vodoravno, ali uski naslov/komentar traže zasebnu mobilnu doradu.

Na 320/390 px like, akcijske veze, kalendarske strelice, arhiva i dan s objavom imaju 44 px visine. Na 768/1440 px like ima 25 px, akcijske veze 21 px; na desktopu kalendarska strelica ima 30 px, dan s objavom 34 px, a arhivska veza 34 px. To su otvorene P2 mete, odvojene od P1 kalendarskog rasporeda i kontrasta.

## Sigurni klikovi i ostatak

Na 390 px `Prethodni mjesec` otvorio je `?year=2026&month=9`, dan s objavom otvorio je detalj `/post/1/nocna-voznja-kroz-grad/`, a arhivska veza za rujan filtrirani blog `?year=2026&month=9`. Like i komentari nisu mutirani.

Ovim je posljednji od 37 dizajna pojedinačno auditiran, **ne** i popravljen. Sljedeće faze trebaju: (1) vratiti sedmodnevni grid bez gubitka mobilnih 44 px i bez tabletne regresije; (2) osigurati foto-neovisan kontrast navedenih elemenata; (3) doraditi uski post/komentar i shared tablet/desktop dodirne mete. Kraljevska sidebar foto-varijacija, mobilni dani 27/31 px u drugim dizajnima i završna matrica svih 37, uključujući kontrast komentara preko fotografija, ostaju otvoreni.
