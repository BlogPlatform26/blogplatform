# Phase 96d — Asfaltni plamen: mobilni kalendarski dani 44×44 px

## Potvrđeni nalaz i promjena

Sedmodnevni kalendar iz Phase95b nije imao vodoravni overflow, ali je dan s objavom u stvarnom browseru bio širok samo **28,9 px na 320 px** i **38,9 px na 390 px**, uz visinu 44 px. Lokalni CSS samo u `asfaltni_plamen` na širinama ispod 768 px centrira kalendar do 376 px i na 320 px smješta ga točno u granice viewporta. Unutarnji rub je 2 px, razmak između stupaca 1 px, a dan ima minimalnu metu 44×44 px. Tablet i desktop nisu promijenjeni.

## Browser prije/poslije

Izolirana migrirana sintetička SQLite baza sadržavala je autora, dvije javne objave u različitim mjesecima i komentar. Chrome je s učitanim Bootstrapom (`.blog-header-wrap > .row` = `flex`) pregledao blog i detalj na 320/390/768/1440 px prije i poslije, po osam stanja. Vrijednosti su jednake na obje rute.

| Širina | Okvir kalendara prije → poslije | Grid prije → poslije | Dan s objavom prije → poslije |
| ---: | ---: | ---: | ---: |
| 320 px | 248 → 320 px | 214 → 314 px | 28,9×44 → **44×44 px** |
| 390 px | 318 → 376 px | 284 → 370 px | 38,9×44 → **52×44 px** |
| 768 px | 376 → 376 px | 350 → 350 px | 48,3×44 → 48,3×44 px |
| 1440 px | 260 → 260 px | 226 → 226 px | 26,3×34 → 26,3×34 px |

`document.scrollWidth == clientWidth` i kalendarski okvir/grid nemaju lokalni vodoravni overflow u svih osam stanja. Vizualno pregledani mobilni blog i desktop na 1440 px čuvaju automobilsku panoramu i postojeći trostupčani identitet. Stvarni klikovi prethodnog mjeseca, dana s objavom i arhive na blogu i detalju pri sve četiri širine otvorili su očekivane lokalne rute. Likeova je ostalo 0, komentara 1; mutirajuće kontrole nisu kliknute.

## Regresijski gate i preostalo

Postojeći Phase95b test sedmodnevnog grida usklađen je s novom minimalnom širinom. Novi lokalni test provjerava blog, detalj i izostanak pravila u `default` temi: **4/4**. `manage.py check`, `makemigrations --check --dry-run` i puni Django skup **195/195** su zeleni. Izolirana baza, server i privremene slike uklonjeni su nakon provjere.

Desktop kalendarski dani/strelice i zajedničke tablet/desktop post-akcije ostaju P2, kao i potvrđeni uski mobilni post/komentar Mjesečeva plesa i Asfaltnog plamena. Radni indeks 37 dizajna nije završna verifikacijska matrica komentara i fotografskih zona. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
