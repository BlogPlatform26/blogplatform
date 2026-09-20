# Phase 80b — mobilne akcijske mete live editora

Ograničeni popravak odnosi se samo na zasebni `design_live_editor.html`: pri viewportu do 575,98 px tabovi „Naslovi/Pozadine”, kartični „Vrati” i donji save/restore gumbi imaju najmanje 44 px visine. Selektori su vezani uz njihove postojeće klase i atribute; desktop CSS i JavaScript nisu mijenjani.

## Provjera u izoliranom pregledniku

Za Magazin su izmjereni tabovi 30→44 px, četiri kartična „Vrati” gumba 27→44 px i „Spremi promjene” / „Vrati sve naslove” 30→44 px na 320 i 390 px. Za Simple Uzorak dostupni „Pozadine” tab i njegove akcije također mjere 44 px. Na 768 i 1440 px ostaju izvorne visine 30/27/30 px. Širina dokumenta na četiri viewporta ostala je 305/375/753/1425 px; nijedan kontrolni element bočne ploče nije prešao njezin desni rub.

Stvarni klikovi „Naslovi” i „Pozadine” na Simple Uzorku prebacili su vidljivi panel. Kartični reset, ukupni restore i spremanje nisu kliknuti, pa nijedna postavka nije trajno promijenjena. Izvorna baza, mediji i port 8000 nisu dirani; probna baza uklonjena je nakon provjere.

`manage.py check` prolazi; novi uski regresijski test uključen je u puni Django suite, koji prolazi 47/47.

## Preostalo, izvan ovog popravka

- Phase 80b2: boje, selecti, brojčana polja i slideri (trenutačno približno 21–36 px).
- Phase 80c: unutarnji preljev i raspored mobilnog live previewa iz Phase 80a.
- Phase 80d: dodirne mete settings dizajnerskih i ugođaj podtabova.
