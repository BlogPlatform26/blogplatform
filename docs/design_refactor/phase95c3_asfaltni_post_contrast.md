# Phase 95c3 — Asfaltni plamen: foto-neovisan kontrast objave

## Opseg i promjena

Phase95a je za post naslov, tijelo te autora/akcije izmjerio dobar kontrast na tamnom dijelu fotografije, ali samo približno 1,35/1,24/1,02:1 u matematičkoj svijetloj granici. Skupno pravilo davalo je `.blog-post-entry` tek `rgba(24,17,13,.20)` preko dima. Prije izmjene stvarni preglednik potvrdio je tu vrijednost na blogu i detalju pri 320/390/768/1440 px.

Samo post kartica sada dobiva tamnu podlogu `rgba(24,17,13,.85)`; kalendar, arhiva, sidebar i komentari nisu ovim pravilom promijenjeni. Tamni topli sloj zadržava automobilsku panoramu oko kartice i njezin ton unutar kartice, a naslov/tijelo/autor/akcije više se ne oslanjaju na određeni kadar dima.

## Mjerenje u pregledniku

Izolirana migrirana sintetička SQLite baza sadržavala je autora, dvije javne objave u različitim mjesecima i dva komentara. Aplikacija je poslužena na portu 8030; Bootstrap CDN je učitan (`.blog-header-wrap > .row` = `flex`). U stvarnom pregledniku provjereni su blog i detalj pri 320/390/768/1440 px, ukupno osam stanja, prije i poslije. Nakon izmjene computed podloga kartice je u svih osam `rgba(24,17,13,.85)`, naslov `rgb(248,238,227)`, tijelo `rgb(240,228,215)`, poveznice autora i obične akcije `rgb(239,199,146)`; izmjereni `opacity` je 1.

Za najnepovoljniju potpuno bijelu fotografsku podlogu efektivna podloga je `(58,65; 52,70; 49,30)`, a WCAG kontrast naslova **10,58:1**, tijela **9,69:1**, autora i običnih akcijskih poveznica **7,65:1**. Na potpuno crnoj podlozi odgovarajući omjeri su 16,65/15,25/12,04:1. Račun kompozitira stvarnu computed prozirnost s krajnjim RGB vrijednostima pozadine; tamni fotografski kadar sam po sebi nije dokaz prolaza. Najniži omjer u ciljanom skupu ostaje iznad 4,5:1 s marginom.

U svih osam stanja `document` overflow je 0; post kartica, kalendarska kutija i grid imaju jednak `clientWidth` i `scrollWidth`. Na 320/390/768/1440 post kartica je 207/207, 277/277, 639/639 i 608/608 px, a kalendarski grid 199/199, 269/269, 351/351 i 227/227 px. Vizualno su provjereni mobilni raspored i desktop automobil/panorama. Sigurni klikovi prethodnog mjeseca, dana s objavom i arhive vode na očekivane URL-ove; like broj ostao je nula, bez mutacije komentara.

## Testovi i otvoreno

Lokalni regresijski test provjerava pravilo na blogu i detalju te izostanak u `default` dizajnu: 2/2. `manage.py check`, `makemigrations --check --dry-run` i puni skup **179/179** su zeleni.

Tekst i autor komentara (Phase95a autor desktop komentara 3,81:1), arhiva te sidebar preko svijetlog dima nisu zaključeni ovom fazom. Ostaju i uski 320px post/komentar, Kraljevska sidebar foto-kontrast te dio mobilnih kalendarskih i tablet/desktop touch meta. Radni indeks 37 dizajna nije završna verifikacijska matrica. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
