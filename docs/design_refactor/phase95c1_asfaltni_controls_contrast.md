# Phase 95c1 — Asfaltni plamen: kontrast malih kontrola

## Opseg i polazište

Phase95a izmjerio je na tamnoj referentnoj osnovi Bootstrap like **4,16:1**, kalendarsku strelicu **4,40:1** i dan s objavom/današnji dan **4,41:1**. Anonimna uputa uz komentare bila je na prozirnoj fotografskoj površini, pa nije imala stabilan kontrast na svim kadrovima. Ova uska faza popravlja te elemente, ne cijeli dizajn.

Lokalni CSS dizajna daje likeu, uputi, kalendarskoj navigaciji, danu s objavom i današnjem danu neprozirnu tamnu podlogu `#21140e` i topli tekst `#ffe1bd`. Izračun iz stvarnih computed boja daje **14,31:1**. Neprozirnost znači da omjer vrijedi i na svijetlom i na tamnom dijelu dimne fotografije. Ostatak fotografije, mobilni raspored i desktopna automobilska panorama nisu mijenjani.

## Stvarni preglednik

Izolirana migrirana SQLite baza s dva javna posta u različitim mjesecima i komentarom posluživana je na portu 8028. Bootstrap je bio učitan (`.row` = `flex`). Blog i detalj provjereni su na 320/390/768/1440 px, ukupno **osam stanja**. U svih osam like, anonimna uputa, prethodna kalendarska strelica, dan s objavom i današnji dan imali su `background-color: rgb(33,20,14)`, `color: rgb(255,225,189)` i omjer **14,31:1**. Dokument, kalendarski okvir i grid nisu imali vodoravni overflow.

| Širina | Dokument client/scroll | Kalendar client/scroll | Grid client/scroll | Visina likea / kalendarske strelice / dana |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 305/305 | 231/231 | 199/199 | 44 / 44 / 44 px |
| 390 | 375/375 | 301/301 | 269/269 | 44 / 44 / 44 px |
| 768 | 753/753 | 375/375 | 351/351 | 25 / 44 / 44 px |
| 1440 | 1425/1425 | 259/259 | 227/227 | 25 / 30 / 34 px |

Vrijednosti su jednake za blog i detalj. Vizualni pregled pri 390 i 1440 px potvrdio je da male neprozirne površine ne prekrivaju automobilsku fotografiju. Na 390 px sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove (`?year=2026&month=9`, `/post/1/nocna-voznja-kroz-grad/`, `?year=2026&month=9`). Like i komentar nisu mutirani.

## Granica i provjera

Nisu još riješeni foto-neovisan kontrast naslova/podnaslova, post naslova/tijela/autora/ostalih akcija, teksta i autora komentara te arhive i sidebara. Phase95a mjeri autora desktop komentara 3,81:1 već na tamnoj referentnoj zoni. Uski 320 px post/komentar te 27/37 px širina mobilnih kalendarskih dana i tabletne/desktopne dodirne mete također ostaju otvoreni. Ova faza ne tvrdi da je kontrast svih 37 dizajna zatvoren.

Regresijski test `blog/test_phase95c1_asfaltni_controls_contrast.py` provjerava lokalna pravila na blogu i detalju te njihovu odsutnost u default dizajnu. Uski testovi 2/2, `manage.py check`, `makemigrations --check --dry-run` i puni Django skup **175/175** prošli su. Izvorni `db.sqlite3`, mediji, port 8000, `main` i produkcija nisu korišteni.
