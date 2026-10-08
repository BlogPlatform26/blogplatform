# Phase 97a — Mjesečev ples, uski mobilni post i komentar

## Opseg

Isključivo prikaz posta i komentara u dizajnu `mjesecev_ples` na telefonima do 575.98px. Ostali dizajni, tablet i desktop nisu stilski mijenjani. Korištena je izolirana sintetička baza `.qa_phase97a.sqlite3` s dvije objave i jednim komentarom; izvorni `db.sqlite3` i `media` nisu dirani.

## Browser provjera

Stvarni Chrome/Playwright, s učitanim Bootstrapom, blog i detail na 320, 390, 768 i 1440px (osam stanja prije i poslije). Na 320px post-kartica se proširila s 224 na 248px, naslov s 82 na 214px, a tekst komentara s 90 na 184px. Lokalni `scrollWidth` naslova pao je sa 128/82 na 214/214px. Na 390px kartica je proširena s 294 na 318px, naslov sa 152 na 284px, a tekst komentara sa 160 na 254px. Naslov i datum više ne dijele uski red; avatar i tijelo komentara slažu se jedan ispod drugoga. Čitljiv sadržaj i noćna fotografija ostali su vidljivi.

Na 768 i 1440px izmjerene dimenzije kartice, naslova i komentara prije/poslije bile su iste. `documentElement.scrollWidth/clientWidth` je 320/320, 390/390, 768/768 i 1440/1440 na obje rute. Pregledane su mobilne i desktop snimke. Kalendarska navigacija sigurno je kliknuta na svih osam stanja bez mutiranja posta/komentara (ostalo 2/1 u izoliranoj bazi).

## Verifikacija i ostatak

Uski regresijski testovi 2/2, `manage.py check`, `makemigrations --check --dry-run` i puni suite 197/197 zeleni. Promjena ne zatvara druge otvorene P2 touch mete, niti predstavlja završnu verifikacijsku matricu svih 37 dizajna.
