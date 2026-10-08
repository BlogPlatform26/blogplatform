# Phase 95c5 — Asfaltni plamen: kalendar, arhiva i desni stupac preko dima

## Nalaz i promjena

Prije promjene stvarni preglednik je na blogu i detalju pri 320/390/768/1440 px prikazivao `.calendar-box`, `.archive-box` i `.sidebar-box` na samo `rgba(24,17,13,.20)` preko fotografije. Profilna kartica bila je potpuno prozirna. To nije foto-neovisan dokaz čitljivosti svijetlog teksta na bijelom dimu. Sada su te četiri površine te `live-analytics-widget` lokalno podložene s `rgba(24,17,13,.85)`; profil ima 10/12 px unutarnjeg odmaka i zaobljene kutove. Izvan kartica panoramska fotografija automobila ostaje vidljiva, a sedmodnevni kalendar i desktop raspored nisu mijenjani.

## Stvarni preglednik i kontrast

Izolirana migrirana sintetička baza imala je autora, dvije javne objave u različitim mjesecima i komentar. Aplikacija je poslužena na portu 8032 s učitanim Bootstrapom. Blog i detalj su pregledani prije i poslije na 320/390/768/1440 px, ukupno osam stanja. U svih osam nakon promjene computed podloge kalendara, arhive, sidebara i profila su `rgba(24,17,13,.85)`, a `document` overflow je 0. Kalendar, arhiva, sidebar i profil imaju jednake `clientWidth` i `scrollWidth` na svakoj širini.

Izračun nad najnepovoljnijom potpuno bijelom fotografskom podlogom kompozitira computed alfa sloja u efektivnu podlogu `(58,65; 52,70; 49,30)`. Glavni naslovi u bočnim karticama imaju **6,58:1**, prigušeni dani u tjednu i oznake statistike **5,75:1**, arhivska poveznica uz vlastiti 2% bijeli sloj **7,80:1**, prigušeni naziv u profilu **6,69:1**, a obični kalendarski dan na svojoj tamnoj podlozi **9,16:1**. Na potpuno crnom foto-kadru vrijednosti su još veće. Tekstovi statistike/profila pregledani su kao stvarni tekstualni DOM elementi; zasebne kontrole i atribucija unutar karte zadržale su vlastitu svijetlu podlogu. Ovo nije zaključak izveden samo iz tamnog dijela fotografije.

Vizualna provjera pri 1440 px potvrdila je da kartice zadržavaju topli automobilski identitet, a fotografija ostaje izložena između njih. Zaseban sintetički profil s dugačkim neprekinutim imenom imao je `document` overflow 0 te jednake `clientWidth/scrollWidth` imena i kartice na 320/390/768/1440 px. Sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove; like i komentari nisu mutirani.

## Testovi i otvoreno

Lokalni regresijski test provjerava pravila na blogu i detalju te izostanak u `default` dizajnu: 2/2. `manage.py check` i `makemigrations --check --dry-run` su zeleni. Puni Django skup: **183/183**.

Ostaje uski 320px post/komentar, Kraljevska sidebar foto-kontrast, pojedini mobilni kalendarski dani od 27/31 px u drugim dizajnima te zajedničke tablet/desktop dodirne mete. Radni indeks 37 dizajna nije završna verifikacijska matrica. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
