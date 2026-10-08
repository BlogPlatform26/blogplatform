# Phase 96b — Sjene ulice: mobilni kalendarski dani 44×44 px

## Potvrđeni nalaz i opseg

Sedmodnevni kalendar iz Phase93b nije se prelijevao, ali je okvir u uskom lijevom sidebaru dopuštao danu s objavom samo **29,1×44 px na 320 px** odnosno **30,6×44 px na 390 px**. To je P2 dodirna meta, ne kvar sedmodnevne mreže. Lokalni CSS samo u `sjene_ulice` na širinama ispod 768 px centrira kalendar do 376 px (na 320 px točno u širini zaslona), daje 2 px unutarnjeg ruba i 1 px razmaka stupaca, te zahtijeva dan najmanje 44×44 px. Tabletni/desktop raspored i noćna panoramska fotografija nisu mijenjani.

## Stvarni preglednik prije/poslije

Izolirana migrirana sintetička SQLite baza imala je autora, dvije javne objave u različitim mjesecima i komentar. Lokalni server bio je na portu 8035. Chrome s učitanim Bootstrapom (`.blog-header-wrap > .row` = `flex`) provjerio je blog i detalj na 320/390/768/1440 px, ukupno osam stanja prije i osam poslije. Mjere su jednake na obje rute.

| Širina | Kalendar prije → poslije | Grid prije → poslije | Dan s objavom prije → poslije |
| ---: | ---: | ---: | ---: |
| 320 px | 250 → 320 px | 216 → 314 px | 29,1×44 → **44×44 px** |
| 390 px | 260 → 376 px | 226 → 370 px | 30,6×44 → **52×44 px** |
| 768 px | 376 → 376 px | 350 → 350 px | 48,3×44 → 48,3×44 px |
| 1440 px | 260 → 260 px | 226 → 226 px | 26,3×34 → 26,3×34 px |

Nakon promjene `document.scrollWidth == clientWidth`, a kalendarski okvir i grid nemaju lokalni vodoravni overflow u svih osam stanja. Vizualno su pregledani mobilni blog i 1440 px desktop. Sigurni klikovi prethodnog mjeseca, dana s objavom i arhive na blogu i detalju pri sve četiri širine otvorili su očekivane lokalne URL-ove. Likeova je ostalo 0, komentara 1; mutirajuće kontrole nisu kliknute.

## Regresijski gate i otvoreno

Postojeći Phase93b test sedmodnevne mreže usklađen je s novom minimalnom širinom. Novi test potvrđuje lokalno mobilno pravilo na blogu i detalju te njegov izostanak u `default` dizajnu; uski skup **4/4** je zelen. `manage.py check` i `makemigrations --check --dry-run` su zeleni. Puni skup: **191/191**.

Ovo ne zatvara mobilne kalendarske mete dizajna `mjesecev_ples` i `asfaltni_plamen`, niti desktop kalendarske dane/strelice ili zajedničke tablet/desktop post-akcije od 21–25 px. Uski mobilni post/komentar Mjesečeva plesa također ostaje. Radni indeks 37 dizajna nije završna verifikacijska matrica komentara i fotografskih zona. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
