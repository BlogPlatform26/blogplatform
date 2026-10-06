# Phase 90d — Čarobna ljubičasta: kalendar na tabletu

## Nalaz i promjena

Phase 90a potvrdila je lokalno prelijevanje kalendara na 768 px: okvir je imao
150 px vidljive i 184 px sadržajne širine, a mreža dana 117/168 px. Dokument
nije imao horizontalni overflow, no dio kalendara izlazio je iz uskog stupca.

Za raspon 768–991,98 px tri stupca ovog dizajna slažu se vertikalno, a
kalendar je centriran i ograničen na 376 px. Navigacija mjeseci i poveznice
dana imaju najmanje 44 × 44 px; sedam stupaca mreže stane u kalendar. Pravilo
je lokalno za Čarobnu ljubičastu i ne mijenja raspored na 320/390 ili 1440 px.

## Provjera u pregledniku

Izolirana sintetička SQLite baza s objavom, stvarni blog i detalj objave na
320/390/768/1440 px (osam stanja). Prije/poslije na 768 px: okvir 150/184 →
375/375 px (`clientWidth/scrollWidth`), mreža 117/168 → 351/351 px. Poveznica
dana nakon promjene mjeri približno 50 × 46 px, a strelice 44 × 44 px.
Na 320 px okvir/mreža ostaju 233/233 i 201/201 px; na 390 px 303/303 i
271/271 px. Na 1440 px 259/259 i 227/227 px. Document overflow je 0 px u
svih osam stanja. Vizualni pregled 768 px pokazao je cijeli kalendar, arhivu
i objavu u vertikalnom toku te očuvanu fotografiju.

Siguran klik prethodnog mjeseca na 768 px otvorio je očekivani
`?year=2026&month=9`, a klik dana s objavom otvorio je detalj objave.
Mutirajuće kontrole nisu korištene. Izvorni `db.sqlite3`, media i port 8000
nisu dirani.

## Testovi i preostalo

`blog/test_phase90d_carobna_tablet_calendar.py` provjerava lokalni render
pravila na blogu i detalju te odsutnost u drugom dizajnu. Ciljani test,
`manage.py check`, provjera migracija, `git diff --check` i puni Django skup
(**146/146**) prošli su završni gate.

Touch mete post-akcija na tabletu, pojedine desktop kalendarske mete i audit
preostalih pet dizajna ostaju otvoreni; završna matrica svih 37 nije gotova.
