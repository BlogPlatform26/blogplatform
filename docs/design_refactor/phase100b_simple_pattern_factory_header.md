# Phase 100b — tvornički narančasti Simple uzorak

Phase100a izmjerila je P1 na `simple_pattern` profilu bez legacy preferencija: bijeli naslov/podnaslov na tvorničkom narančastom gradijentu `#d98a37` / `#b8641e` imaju samo **2,97/3,16:1**. Phase99g je ranije zaštitila zasebnu spremljenu svijetložutu (`#ffd561`) varijantu, ali ne ovaj tvornički put.

Samo točna tvornička kombinacija gradijenta i bijelog naslova sada dobiva potpuno neproziran crni tekst. Narančasti gradijent, uzorak pozadine, tipografija i desktop raspored ostaju. Izmijenjene korisničke palete ne nasljeđuju pravilo, a ranije popravljena žuta ploča ostaje neovisna.

Izolirani QA korisnik s ID-em 1001 namjerno je izvan sedam legacy JSON ID-jeva; `get_blog_preferences` potvrdio je tvorničke vrijednosti prije browser testa. Stvarni Chrome s primijenjenim Bootstrapom provjerio je blog/detalj na **320/390/768/1440 px**. Minimalni pikselni kontrast nakon popravka iznosi **6,08:1 za naslov** i **5,14:1 za podnaslov**; mjereni su pikseli pod glifovima na stvarnom gradijentu. `document` i zaglavlje imaju 0 px horizontalnog overflowa u svih osam stanja. Sigurno otvaranje objave na 390 px je prošlo bez like/comment mutacije; mobilni i desktop blog su vizualno pregledani.

Uska regresija **2/2** uključuje tvorničke vrijednosti, oba javna prikaza, izmijenjenu paletu i prethodnu žutu varijantu. `check`, `makemigrations --check --dry-run` i puni suite **213/213** prošli su. Izvorni `db.sqlite3`, `media`, port 8000 i `main` nisu korišteni.

Ovo ne zatvara druge nalaze Phase100a: naslovi postova triju simple dizajna, like kontrast u više obitelji, male dodirne mete i preostalih 28 dizajna čekaju zasebnu aktualnu verifikaciju.
