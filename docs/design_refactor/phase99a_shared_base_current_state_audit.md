# Phase 99a — aktualni audit prvih devet dizajna

Ovo je djelomična završna provjera, **ne** završna matrica svih 37 dizajna. Izolirana migrirana sintetička baza sadržavala je devet autora, po jednu objavu i komentar za `default`, `dark`, `classic`, njihove desne varijante te `simple_pattern`, `simple_image` i `simple_retro`. Chrome/Playwright s učitanim Bootstrapom otvorio je blog i detalj na 320, 390, 768 i 1440 px: **72 stanja**. Poveznica za otvaranje objave sigurno je kliknuta za svaki blog na 390 px, bez mutacije sadržaja. Izvorni DB, media i port 8000 nisu korišteni.

Omjeri su minimumi kroz osam stanja po dizajnu. Mjerenje `autor objave` uključuje efektivnu neprozirnost elementa i predaka, za razliku od samog CSS `color`. Za `simple_*` redove algoritam konzervativno omeđuje pozadinsku fotografiju crnom i bijelom; njihovi rezultati zato su **donje granice, ne potvrđeni pikselni padovi**. `simple_pattern` i `simple_image` imaju i vlastitu neprozirnu karticu objave pa ta granica može biti prestroga. Proračun gradijenta kalendarskog dana u osnovnoj temi također nije pikselno verificiran.

| Dizajn | Autor objave | Akcija | Komentar / autor | Arhiva | Kalendar, dan s objavom | Overflow |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `default` | **4,16** | 5,78 | 15,26 / 4,97 | 7,01 | neodređeno, gradijent | 0 |
| `dark` | **3,29** | 7,19 | 5,48 / 5,06 | 11,04 | 5,34 | 0 |
| `classic` | **3,93** | 5,34 | 13,04 / 4,58 | 7,97 | 5,78 | 0 |
| `default_right` | **4,16** | 5,78 | 15,26 / 4,97 | 7,01 | neodređeno, gradijent | 0 |
| `dark_right` | **3,29** | 7,19 | 5,48 / 5,06 | 11,04 | 5,34 | 0 |
| `classic_right` | **3,93** | 5,34 | 13,04 / 4,58 | 7,97 | 5,78 | 0 |
| `simple_pattern` | 3,57† | 5,58 | 6,72 / 4,96 | 4,98 | 5,09 | 0 |
| `simple_image` | 3,57† | 5,58 | 6,72 / 4,96 | 4,98 | 5,09 | 0 |
| `simple_retro` | 3,45† | 6,03 | 6,19 / 5,37 | 6,55 | 6,30 | 0 |

† Konzervativna donja granica preko pozadinske slike; stvarni efektivni kontrast autorske poveznice još treba provjeriti pikselno i prema kartičnoj podlozi.

Nije nedostajao nijedan tekst/autorska poveznica komentara. Nije nađen document ni lokalni horizontalni overflow post kartice, komentara ili kalendara u 72 stanja. Najmanja izmjerena visina tabletne like kontrole bila je 44 px.

## Potvrđeni nalaz i granice

**P1:** Poveznica autora objave u šest `default`/`dark`/`classic` varijanti pada ispod 4,5:1. U osnovnoj i klasičnoj obitelji `.post-author-link` ima `opacity: .8`, u tamnoj `.6`; taj je gubitak stvaran na njihovim karticama. Raniji Phase 84a red za A/Ax ne predstavlja trenutno mjerenje same autorske poveznice s kompozicijom neprozirnosti. Sljedeća uska faza treba ukloniti taj gubitak u tih šest dizajna i ponovno provjeriti kontrast i testove. Prije promjene tri `simple_*` dizajna treba zasebno provjeriti njihov stvarni pikselni/kartični kontrast; konzervativni rezultat nije dovoljan dokaz za zahvat.

**Otvoreno za završnu matricu:** osnovni gradijent dana s objavom zahtijeva provjeru stvarnih pikselnih boja; ovaj audit nije dokazao post-body, naslov bloga, desktop sitne kalendarske mete ni sve foto-kadrove. Broj `1:1` iz konzervativnog crno-bijelog omeđenja gradijenta nije stvarno izmjereni kontrast njegova piksela. Nije opravdano iz ovog djelomičnog audita zaključiti da je svih 37 dizajna završeno.

`manage.py check`, `makemigrations --check --dry-run` i puni Django suite **199/199** prošli su bez pogreške. Nije mijenjan produkcijski kod.
