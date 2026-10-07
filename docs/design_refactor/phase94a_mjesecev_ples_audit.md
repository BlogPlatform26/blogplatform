# Phase 94a — audit Mjesečev ples (`mjesecev_ples`)

## Opseg i metoda

Izolirana migrirana SQLite baza sadržavala je autora s dizajnom `mjesecev_ples`, objavu i komentar drugog korisnika. Stvarni preglednik provjerio je blog i detalj objave na 320, 390, 768 i 1440 px (osam stanja), uz učitan Bootstrap (`.row` = `flex`). Fotografija Mjesečeva plesa, naslov, kartica objave, komentar, kalendar, arhiva i navigacija pregledani su bez klikanja mutirajućih kontrola. Ova faza ne mijenja izvršni kod ni izgled.

`manage.py check`, `makemigrations --check --dry-run` i puni Django skup testova prošli su (167/167).

Kontrast je izračunat iz computed boja i alfa-kompozicije na tamnoj osnovi `#15110f` te krajnje svijetloj mogućoj podlozi `#ffffff`. Potonja je **granica osjetljivosti na fotografiju**, a ne tvrdnja da je izmjereni foto-piksel bijel. Vizualni pregled na desktopu potvrđuje da fotografija prolazi kroz karticu i komentar; sjena teksta nije računata kao stabilna podloga. Sljedeća faza mora izmjeriti efektivni kontrast nakon zaštite na stvarnim svijetlim i tamnim kadrovima.

## P1 — kalendar nije sedmodnevna mreža

Computed `.calendar-weekdays` i `.calendar-grid` imaju `display:block` u svih osam stanja. Nazivi dana i datumi idu jedan ispod drugoga; sam grid visok je oko 1064 px (1054 na desktopu), a kalendar 1285–1385 px. Dan s objavom i navigacijske veze ostaju klikabilni, ali mjesečni pregled nije funkcionalno čitljiv kao kalendar.

| Širina | Dokument client/scroll | Kalendar client/scroll; visina | Grid client/scroll | Dan s objavom |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 305/305 | 231/231; 1309 px | 199/199 | 44×44 px |
| 390 | 375/375 | 259/259; 1309 px | 227/227 | 44×44 px |
| 768 | 753/753 | 147/147; 1385 px | 115/115 | 44×44 px |
| 1440 | 1425/1425 | 259/259; 1285 px | 227/227 | 227×34 px |

Nema dokumentnog ni lokalnog horizontalnog overflowa u reprezentativnom sadržaju, ali odsutnost preljeva ne znači da je raspored ispravan.

## P1 — kontrast ovisi o fotografiji

Kartica objave, kalendar i arhiva koriste samo `rgba(24,18,15,.22)` preko fotografije. Naslov i podnaslov bloga nemaju neprozirnu podlogu. Komentar na 320/390 ima dodatnih 8% svijetlog sloja, a na 768/1440 34% bijelog sloja. Računske granice su:

| Element | Tamna osnova | Svijetla granica |
| --- | ---: | ---: |
| naslov/podnaslov bloga bez podloge | 15.20:1 | 1.23:1 |
| naslov objave na kartici | 15.88:1 | 1.37:1 |
| tijelo objave | 15.04:1 | 1.30:1 |
| autor i akcijske veze | 12.01:1 | 1.04:1 |
| Bootstrap like `#0d6efd` | **4.16:1** | 2.78:1 |
| tekst desktop komentara | 4.86:1 | 1.09:1 |
| autor desktop komentara | **3.88:1** | 1.14:1 |
| tekst / autor mobilnog komentara | 12.62 / 10.08:1 | 1.27 / 1.02:1 |
| anonimna uputa uz komentar | 7.68:1 | 1.16:1 |
| kalendarska strelica | 5.64:1 | 1.01:1 |
| dan s objavom | 4.54:1 | 2.64:1 |
| arhivska veza | 11.61:1 | 1.37:1 |

Like i autor desktop komentara ne dostižu 4,5:1 već na tamnoj referentnoj osnovi; dan s objavom ima gotovo nikakvu marginu. Prozirne površine ne daju foto-neovisno jamstvo za naslov, sadržaj, komentare, uputu i sidebar. Vidljivi desktop kadar ima i tamno nebo i svjetlije oblake/horizont, pa je problem realan za postojeću fotografiju, iako svijetla granica nije mjerenje pojedinačnog piksela.

## P2 — geometrija i dodirne mete

Na 320 px naslov posta ima 77 px unutarnjeg `scrollWidth` u 67 px širine zbog skučenog retka uz datum, bez dokumentnog preljeva. Tekst komentara je u vrlo uskom okviru (tijelo komentara oko 105 px); na 390 px okvir je oko 175 px. Mobilni like, akcije, navigacijske strelice i dan s objavom visoki su 44 px. Na 768 i 1440 px like je samo 25 px, akcijske veze približno 21 px; desktop kalendarska strelica je 30 px, a dan s objavom 34 px. To su zasebne P2 mete nakon P1 popravaka.

## Sigurni klikovi i ostatak

Na 390 px `Prethodni mjesec` otvorio je `?year=2026&month=9`, dan `7` otvorio je detalj `/post/1/…/`, a arhivska veza za listopad otvorila je filtrirani blog `?year=2026&month=10`. Like i komentari nisu mutirani. Izvorni `db.sqlite3`, mediji i port 8000 nisu korišteni.

Sljedeće faze: (1) vratiti sedmodnevni grid bez gubitka mobilnih 44 px i bez tabletne regresije; (2) odvojeno osigurati foto-neovisan kontrast, osobito like, komentar/autora i sidebar, uz stvarne svijetle/tamne foto-zone; (3) doraditi uski naslov/komentar i shared tablet/desktop dodirne mete. `asfaltni_plamen` još nije auditiran. Kraljevska sidebar foto-varijacija, pojedine druge P2 mete i završna matrica svih 37 dizajna ostaju otvoreni.
