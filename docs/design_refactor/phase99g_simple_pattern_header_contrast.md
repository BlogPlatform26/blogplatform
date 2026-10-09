# Phase 99g — kontrast zaglavlja dizajna Simple uzorak

Phase 99f potvrdila je u stvarnom Chromeu da zadani naslov i podnaslov na svijetložutoj ploči padaju na **1,41:1** i **1,32:1**. Ovaj uski popravak čuva ploču, uzorak knjiga i desktop raspored, a samo za zadanu kombinaciju `simple_pattern` + bijeli naslov + jednobojna `#ffd561` ploča postavlja neprozirni tamnosmeđi tekst `#3f3128`. Korisnički izmijenjena paleta i drugi jednostavni dizajni ne nasljeđuju pravilo.

U izoliranoj sintetičkoj bazi s javnom objavom i komentarom stvarni Chrome s učitanim Bootstrapom provjerio je blog i detalj na **320/390/768/1440 px** (osam stanja). Computed tekst je `rgb(63,49,40)`, a ploča `rgb(255,213,97)` u svakom stanju. Nakon privremenog skrivanja samo glifova u QA pregledniku, devet piksela pod svakim elementom dalo je minimalni efektivni kontrast **8,89:1** i za naslov i za podnaslov. `document` i zaglavlje imaju 0 px horizontalnog overflowa. Otvaranje objave s 390px bloga prošlo je bez mutiranja likeova ili komentara.

Uska regresija **2/2**, `check`, `makemigrations --check --dry-run` i puni suite **209/209** su zeleni. Izvorni `db.sqlite3`, `media`, port 8000, `main` i produkcija nisu korišteni. Ovo nije završna verifikacija svih 37 dizajna: Simple retro još treba efektivno browser-mjerenje; desktop kalendarske i post-action dodirne mete P2 te završna matrica ostaju otvoreni.
