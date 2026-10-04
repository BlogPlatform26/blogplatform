# Phase 86c — Zlatni horizont: kontrast naslova i tijela posta

## Opseg

Phase 86c popravlja samo čitljivost naslova i tijela posta preko fotografske
podloge u dizajnu `zlatni_horizont`. Naslov i tagline bloga nisu mijenjani.
Postojeći tabletni omjer stupaca i drugi P2 rasporedni problemi ostaju izvan
opsega. Pravila iz Phase 86b ostaju aktivna.

## Promjena

Naslov i tijelo posta dobili su kompaktne, tamne lokalne površine s blagim
zaobljenjem i sjenom. Površine su neovisne o svijetlim i tamnim zonama
fotografije, ali ne prekrivaju niti mijenjaju sunset kompoziciju izvan sadržaja
posta. Naslov koristi `fit-content`, dok tijelo zadržava postojeću širinu.

## Kontrast i preglednik

Početno mjerenje iz Phase 86a pokazalo je minimum 1,90:1 za naslov posta i
1,46:1 za tijelo. Nakon promjene, efektivni kontrast je 15,79:1 za naslov i
13,60:1 za tijelo na lokalnoj površini `#1b0d07`, što daje jasnu marginu iznad
cilja 4,5:1.

Provjereni su blog i detail prikaz na širinama 320, 390, 768 i 1440 px, ukupno
osam stanja, uključujući svijetle i tamne zone fotografije. Nije pronađen
overflow dokumenta. Poznati tabletni raspored 169/117 px na 768 px nije
mijenjan. Naslov i tagline bloga ostali su transparentni i nepromijenjeni.

Vizualna provjera na 390 i 1440 px potvrdila je da lokalne površine ostaju
diskretne te da zalazak i refleksija i dalje dominiraju kompozicijom. Sigurne
navigacije `Otvori post` i `Prethodni mjesec` prošle su bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase86c_zlatni_post_contrast.py` potvrđuje:

- prisutnost Phase 86c ugovora na blog i detail prikazu;
- odvojene pune površine za naslov i tijelo;
- izolaciju od dizajna `iznad_oblaka`.

Završni gateovi uključuju ciljane testove, `manage.py check`, provjeru migration
drifta i puni Django test suite.
