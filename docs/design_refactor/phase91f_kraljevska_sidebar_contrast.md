# Phase 91f — Kraljevska pozornica: foto-neovisan kontrast sidebara

## Potvrđeni nalaz

Post i komentari bili su zaštićeni u Phase91d, a 768px kalendar geometrijski popravljen u Phase91e. Kalendar, arhiva, profil i statistička bočna kartica još su imali samo `rgba(24,8,12,.34)` preko pozornice. Prije promjene stvarni preglednik potvrdio je tu computed podlogu na blogu i detalju pri 320/390/768/1440 px. Oznake dana imale su tek `.62` alfa. To nije stabilan dokaz čitljivosti preko svijetlog reflektora.

Lokalno pravilo sada podlaže te kartice s `rgba(24,8,12,.90)` i povećava alfa oznaka dana na `.82`, bez promjene sedmodnevnog grida ili geometrije. Vizualni pregled desktopa potvrdio je da kazališna fotografija, zavjese i središnja scena ostaju izložene između kartica. Prvi pregled nakon promjene otkrio je još jednu stvarnu grešku: Bootstrap `text-muted` davao je tamnu boju oznaci spremljenih točaka i objašnjenju ispod karte. To je lokalno nadjačano s `#f4ddd1`, uključujući broj unutar oznake.

## Preglednik, kontrast i navigacija

Izolirana migrirana sintetička SQLite baza imala je dvije objave u različitim mjesecima i komentar. Aplikacija je poslužena na portu 8033 uz učitan Bootstrap. Blog i detalj provjereni su prije i poslije na 320/390/768/1440 px, ukupno osam stanja. Nakon promjene computed podloge sve četiri kartice su `rgba(24,8,12,.9)`, `calendar-weekdays` je `rgba(244,221,209,.82)`, a `text-muted` u statistici `rgb(244,221,209)` na svih osam. Document overflow je 0; kalendar, arhiva, sidebar i profil imaju jednaki `clientWidth/scrollWidth` u svakom stanju.

Na matematički najnepovoljnijoj potpuno bijeloj fotografskoj podlozi efektivna boja kartice je `(47,1; 32,7; 36,3)`. Iz computed boja slijedi kontrast naslova kartica **11,41:1**, oznaka dana **8,42:1**, arhivske poveznice **11,53:1**, prigušenog naziva profila **8,08:1** i oznaka statistike **7,39:1**. Na potpuno tamnom kadru ti su omjeri veći. Svijetla matematička granica jamči da se zaključak ne oslanja na izabrani tamni foto-piksel; dekorativne točkice pseudo-elementa ne služe kao podloga za tekst.

Sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove. Like i komentar nisu mutirani. Sedmodnevni 768px grid te desktop raspored i fotografija ostali su očuvani.

## Testovi i otvoreno

Lokalni regresijski test pokriva blog, detalj i izostanak pravila u `default` dizajnu: 2/2. `manage.py check` i `makemigrations --check --dry-run` su zeleni. Puni Django skup: **185/185**.

Preostaju P2 uski mobilni kalendarski dani u drugim dizajnima, zajedničke tablet/desktop dodirne mete i uski post/komentar Asfaltnog plamena. Radni indeks 37 dizajna nije završna verifikacijska matrica. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
