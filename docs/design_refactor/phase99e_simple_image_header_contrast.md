# Phase 99e — naslov na zlatnoj ploči dizajna Simple slika

Phase 99d ostavila je vizualnog kandidata, bez tvrdnje o kontrastu. U izoliranoj sintetičkoj bazi s javnim blogom i objavom, stvarni Chrome s učitanim Bootstrapom potvrdio je uzrok: zadana zaglavna ploča je neprozirna `#c8b16b`, a naslov bijel (`#fff`) te podnaslov bijel s opacity `0.82`. Efektivni omjeri su **2,11:1** za naslov i **1,87:1** za podnaslov. Vanjska fotografija police nije uzrok jer je ploča neprozirna.

Zadana kombinacija `simple_image` + bijela naslovna boja + jednobojna zlatna ploča sada dobiva tamnosmeđu `#3f3128` za naslov i podnaslov, a podnaslov punu neprozirnost. Omjer oba teksta je **5,92:1**. Odstupajuće korisničke boje/načini zaglavlja i drugi jednostavni dizajni ne nasljeđuju to pravilo. Zlatna ploča, pozadinska fotografija i desktop raspored ostaju.

Provjeren je javni blog i detalj na **320/390/768/1440 px** (osam stanja prije i osam poslije). Prije je potvrđena ista neprozirna boja ploče i bijela computed boja teksta na svih osam stanja; CDN Bootstrap tada nije bio dostupan izoliranom pregledniku, no izmjereni kontrast samog teksta i ploče ne ovisi o njemu. Poslije, uz stvarno učitan Bootstrap, u svih osam stanja computed boja oba teksta bila je `rgb(63, 49, 40)`, ploča `rgb(200, 177, 107)`, a document overflow 0. Vizualno je pregledan 320px blog; otvaranje objave na 390px bilo je sigurno i uspješno, bez mutacije. Ovo ne potvrđuje sve ostale površine triju jednostavnih dizajna niti završnu matricu 37 dizajna.

Izvorni `db.sqlite3`, `media`, port 8000 i `main` nisu korišteni. Uski testovi **2/2**, `check`, `makemigrations --check --dry-run` i puni suite **207/207** zeleni su.
