# Phase 92a — audit Dimnih akorda

## Opseg i metoda

Izolirana migrirana SQLite baza `db_phase92_trial.sqlite3` sadržavala je
autora s dizajnom `dimni_akordi`, javnu objavu i komentar drugog korisnika.
Stvarni preglednik provjerio je blog i detalj na 320/390/768/1440 px
(**osam stanja**); Bootstrap CSS bio je učitan (computed `.row` = `flex`).
Pregledane su mobilna, tabletna i desktop fotografija, post, komentar,
kalendar i arhiva. Izvorni `db.sqlite3`, media i port 8000 nisu korišteni;
like i druge mutirajuće kontrole nisu kliknute.

`manage.py check`, `makemigrations --check --dry-run` i puni Django skup
(**151/151**) prošli su. Ova faza samo dokumentira nalaze; nema izmjene
izvršnog koda ili CSS-a.

## P1 — kalendar nije sedmodnevna mreža

U svih osam stanja computed `.calendar-weekdays` i `.calendar-grid` imaju
`display:block`, a ne `grid`. Sedam naziva dana i 31 datum prikazani su
jedan ispod drugoga. Na 320/390/768/1440 px visina kalendara iznosi
otprilike **1309/1309/1385/1285 px**; sama lista datuma 1064 px na prve
tri širine i 1054 px na desktopu. Klikabilni dan ima samo **34 px** visine.
To je stvarno vidljivo na blogu i detalju, nije samo numerički overflow.
U zajedničkom `blog_design_styles.html` sedmostupčani grid dolazi u
pravilima za druge grupe dizajna, ali se za `dimni_akordi` ne ispisuje;
lokalna tema postavlja razmak i izgled dana bez `display:grid` ili
`grid-template-columns` za mrežu. To je potvrđen zajedničko-tematski P1
prikaza kalendara, uz P2 visinu dodirne mete dana.

| Širina | Dokument / viewport | Kalendar client/scroll | Mreža client/scroll | Najmanji dan |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 305/320 | 231/231 | 199/199 | 34 px |
| 390 | 375/390 | 259/259 | 227/227 | 34 px |
| 768 | 753/768 | 147/147 | 115/115 | 34 px |
| 1440 | 1425/1440 | 259/259 | 227/227 | 34 px |

Nema dokumentnog horizontalnog overflowa niti lokalnog horizontalnog
overflowa kalendara, ali to **ne** znači da je kalendar ispravan: njegov je
raspored vertikalno pogrešan. Na 768 px strelice/naslov se dodatno lome.

## P1 — kontrast preko fotografije i Bootstrap like

Computed sloj post-kartice i kalendara je samo `rgba(31,17,12,.18)` nad
fotografijom. Komentar na 768/1440 dodaje 34% bijeli sloj, a na 320/390
8% svijetli sloj. Naslov/podnaslov nemaju neprozirnu podlogu. Zato se
kontrast mijenja s položajem i svjetlinom foto-kadra, uključujući tekst
posta, autora/akcije, komentar i njegova autora, kalendar/arhivu te
anonimnu uputu. Tekstualna sjena nije uračunana kao pouzdana podloga.

Sljedeći omjeri su iz computed boja i alfa-kompozicije, uz tamnu osnovu
`#21130d` i **teorijsku bijelu foto-zonu**. Bijela granica nije tvrdnja da
konkretan piksel fotografije jest bijel, nego pokazuje da prozirni sloj ne
jamči čitljivost na svijetlom kadru.

| Element | Tamna osnova | Svijetla granica |
| --- | ---: | ---: |
| naslov bloga `#f6dfc0`, bez zaštitne podloge | 13,95:1 | 1,29:1 |
| tijelo posta `#f1dfd1` na 18% tamnoj kartici | 13,98:1 | 1,14:1 |
| naslov posta `#f8e8d3` na istoj kartici | 15,07:1 | 1,23:1 |
| autor/akcije `#efc08f` na istoj kartici | 10,87:1 | 1,13:1 |
| Bootstrap like `#0d6efd` na istoj kartici | **4,02:1** | 3,06:1 |
| desktop tekst komentara na dodatnih 34% bijele | 4,52:1 | 1,01:1 |
| desktop autor komentara na istoj podlozi | **3,51:1** | 1,30:1 |
| anonimna uputa, 72% svijetli tekst | 7,68:1 | 1,10:1 |
| kalendarska strelica na 26% bijeloj podlozi | 4,81:1 | 1,22:1 |
| arhiva na 2% bijeloj podlozi | 11,05:1 | 1,24:1 |

Like i autor desktop komentara padaju ispod 4,5:1 već na tamnoj
referentnoj osnovi. Mobilni komentar na pregledanom tamnom kadru izgleda
čitljivo, ali njegov 8% svijetli sloj također nije foto-neovisan dokaz.
Fotografija i smeđe-zlatni desktop karakter trebaju ostati vidljivi pri
lokalnim kontrastnim popravcima.

## P2 — dodirne mete i uski sadržaj

Na 320/390 px kalendarske strelice, arhivski link te like/komentar/otvori
post imaju oko 44 px visine. Datum s objavom ima samo 34 px, uz pogrešan
jednostupčani raspored. Na 768/1440 px like je 25 px, post-akcijske
poveznice 21 px; desktop strelice su 30 px, a arhiva 34 px. Tabletna
arhiva može se prelomiti na 51 px, ali to ne rješava ostale mete.

Na 320 px naslov posta ima `scrollWidth` 74 naspram 67 px `clientWidth`,
no `overflow` je vidljiv i pregled u pregledniku pokazuje čitljiv naslov
u više redaka. To nije proglašeno potvrđenim odsijecanjem. Mobilni komentar
je vrlo uzak zbog avatara i unutarnjeg razmaka (oko 105 px kartice na 320),
pa tekst teče gotovo riječ po riječ; to je P2 čitljivosti rasporeda.

## Sigurni klikovi i daljnji redoslijed

Na 390 px stvarni klik `Prethodni mjesec` otvorio je očekivani
`?year=2026&month=9`; klik dana `6` otvorio je slugged detalj
`/post/1/vecer-akorda-i-dima/`; arhivski link otvorio je
`?year=2026&month=10`. Nije bilo mutacije likea ni komentara.

1. Vratiti sedmostupčani kalendar u Dimnim akordima na svim širinama,
   s prikladnim mobilnim metama i bez tabletnih/desktop regresija.
2. U zasebnim malim fazama osigurati foto-neovisan kontrast likea,
   autora komentara, naslova, sadržaja, akcija, upute i sidebara.
3. Riješiti preostale tablet/desktop dodirne mete i uski komentar.

Tri dizajna (`sjene_ulice`, `mjesecev_ples`, `asfaltni_plamen`) još čekaju
pojedinačni audit. Završna matrica svih 37, uključujući komentare i
fotografske zone, nije gotova.
