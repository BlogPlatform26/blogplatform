# Phase 92c — Dimni akordi: like i uputa uz komentare

## Opseg

Phase92a izmjerio je Bootstrap like na tamnoj referentnoj podlozi oko
4,02:1. Anonimna uputa uz komentare bila je na prozirnoj fotografskoj
površini, pa njezin kontrast nije bio stabilan na svim kadrovima.
Ova uska faza popravlja samo te dvije mete.

Lokalni stil dizajna daje gumbu i uputi neprozirnu dimnu podlogu `#21130d`
i toplu boju teksta `#ffe0be`. Izračunati omjer iz stvarnih computed boja je
**14,32:1**. Zbog neprozirne podloge vrijedi na svijetlom i tamnom dijelu
fotografije. Pozadinska fotografija i trosupčani desktopni raspored ostaju.

## Browser provjera

Izolirana sintetička SQLite baza s javnom objavom u listopadu, arhivskom
objavom u rujnu i komentarom posluživana je na portu 8020. Bootstrap je
bio učitan. Stvarni preglednik provjerio je blog i detalj objave na
320/390/768/1440 px (**osam stanja**). U svakom stanju like i uputa imaju
computed `background-color: rgb(33,19,13)` i
`color: rgb(255,224,190)`. Širina dokumenta nije prešla viewport:
305/320, 375/390, 753/768 i 1425/1440 px na obje rute.

Like je na 320/390 visok 44 px, a na 768/1440 25 px; tabletne i desktopne
post-akcijske mete ostaju P2. Vizualni pregled pri 320 i 1440 px potvrdio je
da male neprozirne površine ne mijenjaju panoramski identitet. Sigurni klik
prethodnog mjeseca otvorio je `?year=2026&month=9`, dan s objavom slugged
detalj, a arhiva `?year=2026&month=10`. Like i komentar nisu mutirani.

## Gate i preostali rad

`blog/test_phase92c_dimni_action_contrast.py` provjerava lokalni CSS ugovor
na blogu i detalju te odsutnost u drugom dizajnu. Uska 2/2 testa,
`manage.py check`, `makemigrations --check --dry-run`, `git diff --check`
i puni Django skup **155/155** prošli su.

Nije riješen foto-neovisan kontrast naslova, tijela posta, autora, ostalih
akcija, teksta/autora komentara, kalendara i arhive. Phase92a mjeri autora
desktop komentara 3,51:1 na tamnoj referentnoj zoni. Mobilni dani kalendara
još su samo 27/31 px široki; dio tabletnih/desktopnih meta ostaje P2.
Izvorni `db.sqlite3`, media i port 8000 nisu korišteni.
