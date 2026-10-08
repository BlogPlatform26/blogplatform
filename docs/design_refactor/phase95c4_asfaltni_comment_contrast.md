# Phase 95c4 — Asfaltni plamen: foto-neovisan kontrast komentara

## Potvrđeni uzrok i opseg

Phase95a je izmjerio autora desktop komentara 3,81:1 čak na tamnoj referentnoj zoni. U stvarnom pregledniku prije ove promjene zajednički stil je na 768/1440 px davao `.comment-body` bijelu podlogu `rgba(255,255,255,.34)` preko kartice i fotografije, a na 320/390 px još prozirniji `color-mix(... 8%, transparent)`. Datum je na desktopu imao boju s alfom .72 i `opacity: .78`. Dakle, sama svijetla boja slova nije dokaz čitljivosti nad svijetlim dimom.

Samo komentari unutar post kartice ovog dizajna sada imaju toplu neprozirnu podlogu `#21140e`, tekst `#f0e4d7`, autora `#ffe1bd` i datum `#e3c7a6` pri opacity 1. Lokalni selektori nadjačavaju kasnije uključeni zajednički stil komentara na svim širinama. Automobilska fotografija ostaje izložena izvan malih površina komentara, a desktop tipografija i geometrija nisu mijenjane.

## Browser QA i kontrast

Izolirana migrirana sintetička SQLite baza imala je javnu objavu i dva komentara različitih autora. Aplikacija je poslužena na portu 8031 s učitanim Bootstrapom (`.blog-header-wrap > .row` = `flex`). Prije i poslije provjereni su blog i detalj na 320/390/768/1440 px, ukupno osam stanja. Nakon promjene computed podloga, tekst, autor i datum jednaki su u svih osam stanja, bez prozirnosti. Izravno iz njihovih computed RGB vrijednosti proizlazi **14,33:1** za tekst, **14,31:1** za autora i **11,09:1** za datum. Budući da je podloga neprozirna, ni najbjelji dio fotografije ne može smanjiti te omjere.

Document overflow je 0 na svih osam stanja. Komentar ima `clientWidth/scrollWidth` 104/104, 174/174, 536/536 i 504/504 px pri navedenim širinama, na blogu i detalju. Unutarnje riječi komentara zadržale su computed `rgb(240,228,215)`. Vizualni pregled desktop panorame potvrdio je da tople tamne kartice zamjenjuju prethodne sive i da automobil ostaje vidljiv. Sigurni klikovi mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove; like/komentari nisu mutirani.

## Testovi i ostatak

Novi lokalni regresijski test pokriva blog, detalj i izostanak pravila u `default` dizajnu: 2/2. `manage.py check` i `makemigrations --check --dry-run` su zeleni. Puni skup: **181/181**.

Arhiva i desni sidebar Asfaltnog plamena preko svijetle fotografije ostaju zasebno otvoreni, kao i 320px uski post/komentar, Kraljevska sidebar foto-kontrast te pojedine mobilne kalendarske i tablet/desktop dodirne mete. Ovo nije završna matrica kontrasta svih 37 dizajna. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
