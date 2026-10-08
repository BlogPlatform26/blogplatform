# Phase 96c — Mjesečev ples: mobilni dani kalendara 44×44 px

## Nalaz i lokalni popravak

Sedmodnevni kalendar iz Phase94b na 320/390 px imao je dan s objavom širok samo **28,9/30,6 px**, iako visok 44 px. Dokument i kalendar nisu se prelijevali, ali dodirna meta nije bila dovoljno široka. Samo u temi `mjesecev_ples`, ispod 768 px, kalendar sada izlazi iz uskog sidebar stupca do najviše 376 px i centriran je unutar viewporta. Unutarnji rub je 2 px, stupčani razmak 1 px, a dan je najmanje 44×44 px. Tablet i desktop nisu mijenjani.

## Stvarni browser prije/poslije

Migrirana izolirana sintetička SQLite baza imala je autora, dvije javne objave u različitim mjesecima i komentar. Chrome je pregledao blog i detalj na 320/390/768/1440 px prije i poslije (po osam stanja), s učitanim Bootstrapom (`.blog-header-wrap > .row` = `flex`). Mjere su jednake za obje rute.

| Širina | Okvir prije → poslije | Grid prije → poslije | Dan s objavom prije → poslije |
| ---: | ---: | ---: | ---: |
| 320 px | 248 → 320 px | 214 → 314 px | 28,9×44 → **44×44 px** |
| 390 px | 260 → 376 px | 226 → 370 px | 30,6×44 → **52×44 px** |
| 768 px | 376 → 376 px | 350 → 350 px | 48,3×44 → 48,3×44 px |
| 1440 px | 260 → 260 px | 226 → 226 px | 26,3×34 → 26,3×34 px |

Na svakoj širini i ruti `document.scrollWidth == clientWidth`; kalendarski okvir i grid imaju 0 px lokalnog vodoravnog overflowa. Vizualno su pregledani mobilni blog i desktop od 1440 px: noćna panorama i desktop trostupčani identitet ostaju. Stvarni sigurni klikovi prethodnog mjeseca, dana s objavom i arhive na svih osam stanja otvorili su očekivane lokalne URL-ove. Likeova je ostalo 0, komentara 1; nije kliknuta mutirajuća kontrola.

## Testovi i otvoreno

Postojeći Phase94b test sedmodnevnog grida i novi lokalni test blog/detail/izolacije teme: **4/4**. `manage.py check`, `makemigrations --check --dry-run` i puni Django skup **193/193** su zeleni. Izolirana baza, server i privremene slike uklonjeni su nakon provjere.

Ovo ne rješava potvrđeni uski mobilni naslov/komentar Mjesečeva plesa, mobilne kalendarske mete `asfaltni_plamen`, desktop kalendarske dane/strelice ni zajedničke tablet/desktop post-akcije. Radni indeks 37 dizajna nije završna verifikacijska matrica kontrasta komentara i fotografskih zona. Izvorni `db.sqlite3`, media, port 8000, `main` i produkcija nisu dirani.
