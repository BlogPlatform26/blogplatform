# Phase 89a — audit: Zlatno polje, Neonski grad i Polje lavande

## Opseg i metoda

Audit obuhvaća `zlatno_polje`, `neonski_grad` i `polje_lavande`, javni blog i detail pojedine objave na 320, 390, 768 i 1440 px: ukupno **24 stvarna browser stanja**. Korištena je izolirana, migrirana SQLite kopija sa svježim autorima, objavama, komentarima i arhivom. Originalni `db.sqlite3`, media i mutirajuće kontrole nisu korišteni.

Svaki dizajn ima fotografiju na `body::before` i barem dio prozirnih površina. Omjeri ispod izmjereni su prema deklariranoj neprozirnoj osnovi tijela (`body` fallback), s computed bojama koje browser stvarno primjenjuje. To je provjerljiva referenca, ali **nije foto-neovisan minimum**: svjetliji ili tamniji crop ispod prozirne kartice može omjer dodatno sniziti. Sjenu teksta ne računam kao pouzdanu kontrastnu površinu. Vizualni pregled napravljen je na mobilnom i desktop cropu svake fotografije.

Sigurni klikovi na 390 px nisu mijenjali podatke: `Prethodni mjesec` vodi na odgovarajući `?year=2026&month=9`, a dan s objavom na slugged detail rutu za sva tri dizajna.

## Raspored, overflow i mete

| Dizajn | Blog/detail overflow na 320 / 390 / 768 / 1440 px | Nalaz |
| --- | --- | --- |
| Zlatno polje | `0 / 0 / 1 / 0 px` u obje rute | Rubni 1 px na tabletu, bez vidljivog odsijecanja. |
| Neonski grad | `0 / 0 / 2 / 0 px` u obje rute | Rubni 2 px na tabletu, bez vidljivog odsijecanja. |
| Polje lavande | `0 / 0 / 19 / 0 px` u obje rute | Vidljivi horizontalni scroll i odrezano dugo ime u desnom profilnom panelu. |

Na 320/390 px strelice kalendara i like imaju `44×44 px`, dan s objavom `46×46 px`, a link komentara približno `97–99×44 px`. Na 768/1440 px post akcije se vraćaju na visinu oko `21–30 px`, a kalendarske strelice na `30 px` na desktopu: P2 za touch, bez blokiranja miša/trackpada.

Tabletni overflow Lavande nije kalendarski: `blog-main-right-column` je širok oko `172 px`, dok dugo sintetičko ime (`phase89a_lavender`) daje profilnom identitetu `scrollWidth` oko `159 px` unutar dostupnih `81 px`. Red ima `scrollWidth 776 px` unutar približno `729 px` sadržaja. To je naslijeđeni profilni ugovor koji se može pojaviti u svakom dizajnu s duljim korisničkim imenom.

## Zlatno polje

Computed boje su tamne preko zlatne fotografije i poluprozirnog `--panel-bg: rgba(255, 248, 224, .14)`. Referentni omjeri prema `#d9a63a` su:

| Meta | Boja | Referentni omjer |
| --- | --- | --- |
| naslov bloga | `#5a3605` | 4,82:1 |
| naslov objave | `#4b2d05` | 5,65:1 |
| tijelo / autor | `#5f3d10` | 4,38:1 |
| komentar | `#4d3212` | 5,32:1 |
| archive link | `rgba(97,62,14,.92)` | 4,30:1 |
| link autora | `#7c4f0f` | 3,17:1 |
| akcija komentara | `#6c4410` | 3,83:1 |

Desktop crop pokazuje autora, akcije i tekst objave izravno na svijetloj pšenici/prozirnoj kartici; vrijednosti ispod 4,5:1 nisu foto-neovisne. Poruka neprijavljenome ostaje Bootstrap `rgba(33,37,41,.75)`; kompozit prema osnovi je 4,26:1 i također ovisi o cropu.

## Neonski grad

Glavni sadržaj je na tamnoj gradijentnoj kartici (`rgba(17,10,39,.58)` prema `rgba(11,8,29,.46)`), pa su referentni omjeri prema `#17082f` vrlo dobri: naslov bloga 16,82:1, naslov objave 17,45:1, tijelo/komentar/autor 15,51:1, link autora 13,19:1 i akcija komentara 11,87:1. Vizualni mobilni i desktop crop to potvrđuju za naslov, tijelo, autora, akcije i komentar.

Iznimka je poruka neprijavljenome: nije lokalno stilizirana i browser joj daje `rgba(33,37,41,.75)`. Kompozit prema tamnoj osnovi je samo **1,15:1**; na desktop cropu je pri dnu kartice praktično nečitljiva.

## Polje lavande

Kartice i post entry su transparentni, pa tekst prelazi preko svijetlog neba, cvijeta i tamnijeg reda lavande. Referentni omjeri prema `#d9b0ee` su: naslov bloga 6,25:1, naslov objave 6,72:1, tijelo/autor/komentar 5,35:1 i arhiva 5,35:1. To nije zajamčeno na fotografiji. Link autora i akcija komentara koriste `#7c44a1`, samo **3,56:1** prema osnovi. Mobilni i desktop crop potvrđuju da su tijelo, autor i akcije izloženi jako različitim zonama slike; osobito se post tekst i meta stapaju s ljubičastim cvijetom.

Poruka neprijavljenome ima isti nenaslijeđeni Bootstrap mutni tekst. Njen kompozit prema osnovi iznosi 4,73:1, ali i ona je na prozirnoj fotografiji.

## Prioriteti

### P0

Nema potvrđenog P0: obje rute se renderiraju za sva tri dizajna, nema mobilnog ili desktop document overflowa, a sigurna kalendarska i post navigacija rade.

### P1

1. `neonski_grad`: lokalno obojiti poruku neprijavljenome (`.small.text-muted`) prema postojećoj tamnoj kartici. Trenutačnih 1,15:1 je jasan kontrastni kvar, iako su ostali ciljevi dobri.
2. `zlatno_polje`: lokalna stabilna površina ili tamnija tinta za link autora, akcije i arhivu; referentnih 3,17–4,30:1 preko svijetle i promjenjive fotografije nije dovoljno.
3. `polje_lavande`: lokalna stabilna površina ili konzervativnija tinta za akcije/link autora (3,56:1), uz isti ugovor za tijelo i autorovu metu preko fotografije.
4. Dugi korisnički identitet u desnom profilnom stupcu: pri 768 px dopustiti lomljenje unutar profila (`min-width: 0` / `overflow-wrap:anywhere`) i potvrditi na svim dizajnima prije shared promjene. Ne skrivati horizontalni overflow kao zamjenu za čitljivo ime.

### P2

- Rubni 1–2 px tabletni scroll u Zlatnom polju i Neonskom gradu provjeriti zajedno s općim profilnim ugovorom; nije vizualno vidljiv u ovom fixtureu.
- Post akcije na 768/1440 px i desktop strelice kalendara imaju manje od preporučenih 44 px touch meta.

## Najmanji sljedeći popravak

Najmanji izolirani P1 je `neonski_grad` poruka neprijavljenome: lokalno joj dodijeliti svijetlu boju koja pripada postojećoj tamnoj kartici i testirati je na 320, 390, 768 i 1440 px. Taj popravak ne dira shared layout, fotografiju, kalendarski ugovor ni identitet drugih dizajna. Nakon toga odvojeno riješiti foto-neovisni kontrast Zlatnog polja i Polja lavande.
