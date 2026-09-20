# Phase 80c — mobilni live preview bez odrezanog sadržaja

Phase 80a izmjerio je višak širine preview okvira od približno 65 px na viewportu 320 te oko 16 px na 390/768/1440. Uzrok je bio dvostruk: skripta je nametala minimalnu dostupnu širinu od 320 px iako je sadržaj okvira na 320 px širok samo oko 255 px, a pri izračunu nije oduzimala oba unutarnja paddinga. Transformirani iframe ostajao je u normalnom rasporedu, pa je njegova neskalirana širina dodatno ulazila u scroll mjere. `overflow-x:hidden` je višak samo prikrivao.

Preview sada na mobitelu koristi stvarni blog pri prirodnoj širini 320 px, skaliran na raspoloživi sadržaj okvira; na 390 px ostaje u prirodnoj veličini. Iframe je apsolutno pozicioniran u ljusci koja čuva njegovu skaliranu visinu, a širina ljuske računa se iz korisne širine okvira. Horizontalni overflow okvira i stranice nije skriven, nego je postavljen na `auto` kako bi eventualni budući višak ostao dostupan. Na mobitelu su dodane dvije 44 px poveznice za skok od kontrola do previewa i natrag. Desktop i tablet zadržavaju široki prikaz bloga.

## Mjerenja u izoliranoj bazi

Magazin i Simple Uzorak na 320/390/768/1440 px dali su istu geometriju:

| Viewport | Prije: unutarnji višak | Poslije: unutarnji višak | Prirodni iframe | Vidljiva širina iframea | Širina dokumenta |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 320 | ≈65 px | 0 px | 320 px | 255 px | 305 px |
| 390 | ≈16 px | 0 px | 320 px | 320 px | 375 px |
| 768 | ≈16 px | 0 px | 1180 px | 703 px | 753 px |
| 1440 | ≈16 px | 0 px | 1180 px | 1037 px | 1425 px |

Na 320 px završno stanje sadržaja oba iframea imalo je `scrollWidth=innerWidth=320`; pri brzom prijelazu 1440→320 može se kratko očitati prethodna širina prije dovršetka browserova resize ciklusa, nakon kojeg se vraća na 320. Vizualno su provjereni mobilni Magazin i Simple Uzorak: naslov, zaglavlje i kalendar prikazuju se u stvarnom mobilnom rasporedu. Klikovi na skok do previewa i natrag radili su. Na oba dizajna nespremljena promjena slidera odmah je promijenila vidljivi naslov u iframeu s 32 na 64 px; na Simple Uzorku prebacivanje „Naslovi/Pozadine” ostalo je funkcionalno. Nijedna postavka nije spremljena.

`manage.py check` prolazi; uski regresijski test i puni Django suite 49/49 prolaze. Izvorna baza, mediji i port 8000 nisu dirani; probna baza uklonjena je nakon provjere. Phase 80d (settings podtabovi) ostaje zaseban zadatak.
