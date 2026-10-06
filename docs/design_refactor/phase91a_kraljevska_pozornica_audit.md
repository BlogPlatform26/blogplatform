# Phase 91a — audit Kraljevske pozornice

## Opseg i metoda

Izolirana migrirana SQLite baza sadržavala je autora s dizajnom
`kraljevska_pozornica`, javnu objavu i komentar. Stvarni preglednik provjerio
je blog i detalj na 320/390/768/1440 px (**osam stanja**), uključujući
stvarnu fotografiju pozornice i komentare. Nisu mijenjani izvršni kod,
izvorni `db.sqlite3`, media ni port 8000; mutirajuće kontrole nisu kliknute.

`manage.py check`, `makemigrations --check --dry-run`, `git diff --check`
i puni Django skup (**146/146**) prošli su završni gate.

Computed boje i površine izmjerene su u pregledniku. Donja dva kontrastna
scenarija su matematičke granice za deklarirane prozirne slojeve: tamna
osnova `#16070b` te najsvjetlija moguća foto-zona `#ffffff`. Potonja nije
tvrdnja da konkretan piksel fotografije ima upravo tu boju, nego dokaz da
postojeći sloj **ne jamči** dovoljan kontrast pri promjeni kadra. Tekstualna
sjena i blur nisu uračunani kao pouzdana kontrastna podloga.

| Element | Computed sloj/boja | Tamna osnova | Svijetla granica |
| --- | --- | ---: | ---: |
| naslov bloga i podnaslov | prozirno; `#fff0d9`, podnaslov opacity .82 | naslov 17,50:1 | naslov 1,12:1 |
| tijelo posta | kartica `rgba(24,8,12,.38)`, tekst `#f4ddd1` | 15,03:1 | 1,95:1 |
| autor i akcijske poveznice | kartica .38, tekst `#ffcf9f` | 13,70:1 | 1,77:1 |
| komentar na 768/1440 | dodatna bijela površina .34, tekst `#f4ddd1` | 5,00:1 | 1,37:1 |
| autor komentara na 768/1440 | ista površina, `#ffcf9f` | 4,55:1 | 1,25:1 |
| Bootstrap like | `#0d6efd` na kartici .38 | **4,35:1** | 1,77:1 |
| anonimna uputa | `rgba(33,37,41,.75)` na kartici .38 | **1,18:1** | 3,83:1 |

Na 320/390 komentar koristi drugi, samo 8% svijetli sloj; na 768/1440
computed `comment-body` postaje 34% bijel. Mobilni komentar na pregledanom
tamnom kadru izgleda čitljivo, ali niti njegova foto-neovisna granica nije
potvrđena. Naslov/podnaslov su na 390 i 768 px vizualno iznad svijetlog
lustera; desktop zadržava impresivnu panoramu, no položaj fotografije mijenja
zonu iza teksta. Zato su zaštita naslova i kartičnog/komentarskog teksta P1,
uz očuvanje kazališne fotografije i desktop identiteta. Uputa i like su
deterministički potvrđeni P1 i na tamnoj osnovi.

Kalendarska navigacija i arhivska poveznica izgledaju čitljivo na pregledanim
tamnim kadrovima, ali su također na prozirnim 26%/2% svijetlim površinama
preko kartice od samo 34% tame. Njihov kontrast na svijetloj zoni nije
foto-neovisno dokazan; uključiti ih u ciljanu provjeru/zahvat, ne proglasiti
zatvorenima samo na temelju tamnog kadra.

## Geometrija i sigurni klikovi

Na blogu i detalju svih širina nema dokumentnog horizontalnog overflowa
(`documentElement.scrollWidth` je 15 px manji od `innerWidth` zbog vertikalne
trake za pomicanje). `body` koristi `overflow-x:hidden`, stoga je pregledan i
lokalni `scrollWidth`. Na 768 px kalendar ima **149/184 px**
(`clientWidth/scrollWidth`), a mreža dana **117/168 px**: potvrđen P2
lokalni overflow s prelomljenim naslovom i strelicama te odsječenom mrežom.
Na 320/390 px okvir i mreža stanu (233/233 i 201/201 te 259/259 i
227/227 px); strelice su 44×44 px, klikabilni dan oko 46×46 px, arhiva 44 px.
Na 1440 px okvir/mreža stanu (259/259 i 227/227 px), ali je strelica
30×30 px, dan oko 28×35 px i arhiva 34 px. Tablet/desktop post akcije su
21–25 px visoke; mobilne su 44 px. To su otvorene P2 touch mete.

Na 390 px stvarni klik `Prethodni mjesec` otvorio je očekivani
`?year=2026&month=9`; klik dana s objavom otvorio je slugged detalj;
arhivski link otvorio je `?year=2026&month=10`. Like, komentiranje i druge
mutirajuće kontrole nisu kliknuti. Na 320 px naslov posta ima numerički
`scrollWidth` 104 px u 83 px širokom h4 uz datumsku pločicu, ali je
vizualno bio čitljiv u dva retka; to nije proglašeno potvrđenim odsijecanjem.

## Redoslijed daljnjeg rada

1. Uski popravak anonimne upute i like boje/podloge na >=4,5:1 s marginom.
2. Zasebno zaštititi naslov/podnaslov te post/komentar/autor/akcije od
   svijetlih zona fotografije, uz ponovno mjerenje na 320/390/768/1440.
3. Zasebno riješiti 768 px lokalni kalendarski overflow bez smanjivanja
   klikabilnih dana ispod 44 px; tablet/desktop akcijske mete ostaju otvorene.

Četiri dizajna (`dimni_akordi`, `sjene_ulice`, `mjesecev_ples`,
`asfaltni_plamen`) još čekaju pojedinačni audit. Završna matrica svih 37,
uključujući fotografske zone i komentare, nije gotova.
