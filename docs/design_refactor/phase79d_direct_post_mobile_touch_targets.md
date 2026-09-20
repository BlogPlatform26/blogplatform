# Phase 79d — dodirne mete zasebnih obrazaca

Na rutama `/new/` i `/post/<id>/edit/` mobilne kontrole bile su visoke oko 30–37 px. Ova faza ograničava nova pravila na `#createPostForm` i `#editPostForm` pri širini do 575,98 px: standardna polja, datoteke, datum, glavne akcije i CKEditor gumbi imaju najmanje 44 px visine; CKEditor gumbi imaju i najmanje 44 px širine. Kontrola razmaka redaka i redovi kategorija/komentara također dobivaju mobilnu visinu za dodir. Desktop pravila nisu mijenjana. U obrascu za uređivanje mobilna mreža panela sada može stati u uski stupac (`minmax(0, 1fr)`), čime je uklonjen unutarnji preljev koji je prije dosezao x=452 pri viewportu 320 px.

Mjerenja u izoliranom pregledniku sa sintetičkim draftom:

| Ruta | Širina | Polja | Glavne akcije | CKEditor gumbi | Dokument / unutarnji preljev |
| --- | ---: | ---: | ---: | ---: | --- |
| novi i uredi | 320 | 44 px | 44 px | najmanje 44 × 44 px | širina dokumenta 305; nema preljeva obrasca |
| novi i uredi | 390 | 44 px | 44 px | najmanje 44 × 44 px | širina dokumenta 375; nema preljeva obrasca |
| novi | 768/1440 | 37 px | 37 px | postojeći 30 px | bez promjene desktop/tablet izgleda |
| uredi | 768/1440 | 30 px | 31 px | postojeći 30 px | bez promjene desktop/tablet izgleda |

Na obje rute pri 320 px klik/fokus naslova i otvaranje CKEditorova izbornika naslova uspješno su isprobani bez slanja obrasca. Kontrola slike nije otvorila sistemski dijalog, a akcije objave/brisanja nisu kliknute. `manage.py check` prolazi, kao i puni Django suite 45/45. Izvorna baza i mediji nisu dirani.
