# Phase 96a — Dimni akordi: mobilni kalendarski dani 44×44 px

## Nalaz i lokalni popravak

Phase92b je vratio sedmodnevnu mrežu, ali je mobilni sidebar ostavljao samo 214/226 px za sedam stupaca. Stvarni preglednik s učitanim Bootstrapom izmjerio je na 320/390 px najmanji klikabilni dan **28,9×44 / 30,6×44 px**. Dodirna meta nije dosezala 44×44 px, iako nije bilo preljeva.

Samo u dizajnu `dimni_akordi` ispod 768 px kalendar je centriran i može se proširiti do 376 px, a na 320 px doseže točno širinu zaslona. Bočni padding je 2 px i razmak stupaca 1 px; dan ima minimalnu širinu i visinu 44 px. To čuva sedam dana u retku bez vodoravnog skrolanja ili preklapanja. Tabletni raspored, desktop fotografija glazbenice i zadimljeni identitet nisu mijenjani. Namjerno širi kalendar na 320 px nije document overflow: njegov okvir je unutar 0–320 px.

## Browser prije/poslije

Izolirana migrirana sintetička SQLite baza imala je autora, dvije javne objave u različitim mjesecima i komentar. Lokalni server radio je na portu 8034. Stvarni Chrome s učitanim Bootstrapom (`.blog-header-wrap > .row` = `flex`) pregledao je blog i detalj na 320/390/768/1440 px, ukupno osam stanja prije i osam poslije. Tablica vrijedi za obje rute.

| Širina | Okvir kalendara prije → poslije | Mreža prije → poslije | Najmanji dan prije → poslije |
| ---: | ---: | ---: | ---: |
| 320 px | 248 → 320 px | 214 → 314 px | 28,9×44 → **44×44 px** |
| 390 px | 260 → 376 px | 226 → 370 px | 30,6×44 → **52×44 px** |
| 768 px | 376 → 376 px | 350 → 350 px | 48,3×44 → 48,3×44 px |
| 1440 px | 260 → 260 px | 226 → 226 px | 26,3×34 → 26,3×34 px |

Nakon promjene su `document`, kalendar i grid imali 0 px vodoravnog preljeva u svih osam stanja. Vizualno su pregledani mobilni kalendar i panoramski desktop. Sigurni klikovi prethodnog mjeseca, dana s objavom i arhive na svih osam stanja otvorili su očekivane lokalne URL-ove. Likeova je ostalo 0, komentara 1; nijedna mutirajuća kontrola nije kliknuta.

## Regresijski gate i otvoreno

Postojeći test sedmodnevnog grida usklađen je s novom minimalnom širinom, a novi lokalni test potvrđuje mobilno pravilo na blogu i detalju te njegov izostanak u `default` dizajnu: **4/4**. `manage.py check`, `makemigrations --check --dry-run` i puni Django skup **189/189** su zeleni. Izolirana baza, server i privremene slike uklonjeni su nakon provjere.

Ovo ne zatvara mobilne kalendarske mete drugih dizajna (`sjene_ulice`, `mjesecev_ples`, `asfaltni_plamen`) ni desktop dane/strelice od 26–34 px i zajedničke tablet/desktop post-akcije od 21–25 px. Uski mobilni post/komentar Mjesečeva plesa također ostaje. Radni indeks 37 dizajna nije završna verifikacijska matrica kontrasta komentara i fotografskih zona. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
