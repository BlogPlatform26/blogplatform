# Phase 93d — foto-neovisan kontrast Sjene ulice (`sjene_ulice`)

## Nalaz i promjena

Na početku su naslov bloga i podnaslov bili izravno nad fotografijom, a post, kalendar, arhiva i analitika imali su samo `rgba(19,16,14,.34)` podlogu. Desni profil nije imao vlastitu podlogu. Prethodni audit izračunao je na svijetloj zoni omjere 2,20:1 za naslov bloga, 1,93:1 za podnaslov, 1,13:1 za naslov posta, 1,73:1 za tijelo, 1,11:1 za autora/akcije, 1,12:1 za naslov kalendara i 1,60:1 za arhivu.

Tema sada tim karticama i desnom profilu daje neprozirnu noćnu podlogu `#241813`; naslov i podnaslov imaju usku, zaobljenu podlogu umjesto prekrivanja cijele panorame. Godina objave ima čvrstu svijetlu boju umjesto poluprozirne plave. Fotografija, narančasti naslovi i desktopni raspored ostali su vidljivi. Promjena je lokalna za ovu temu; Phase 93c zaštita komentara, likea, upute i kalendarskih strelica ostaje.

## Stvarni preglednik

Izolirana sintetička SQLite baza s dva javna posta i komentarom, zaseban server na portu 8025, učitan Bootstrap (`.row` = `flex`). Blog i post-detail provjereni prije/poslije na 320/390/768/1440 px — osam stanja. Nakon promjene computed podloge svih ciljanih kartica i profila su neprozirne `rgb(36,24,19)` na obje rute i svim širinama. Naslov bloga postiže **7,86:1**, podnaslov **12,26:1**, naslov posta **6,86:1**, tijelo **13,43:1**, autor i slabije meta oznake **6,82:1**, akcijska poveznica **8,61:1**, kalendarski i arhivski naslovi **6,93:1**, arhivska poveznica **8,98:1**, profilno ime **13,43:1**, profilni podnaslov **8,97:1**, a godina objave **11,85:1**. Zbog neprozirne podloge ti omjeri ne ovise o svijetlom ili tamnom dijelu fotografije.

`document.scrollWidth/clientWidth` iznosi 305/305, 375/375, 753/753 i 1425/1425; kalendarski grid također nema lokalni overflow. Stvarni sigurni klikovi prethodnog mjeseca, dana s objavom i arhive vode na očekivane rute. Like i komentari nisu mutirani. Mobilni i desktopni kadar vizualno su pregledani.

## Testovi i ostatak

Novi regresijski test pokriva blog/detail i izolaciju teme. Uski testovi 4/4, `manage.py check`, `makemigrations --check --dry-run`, `git diff --check` i puni Django skup **163/163** prošli su.

Ovo ne zatvara dugi neprekinuti naslov bloga koji može uzrokovati document overflow na 320/390, niti uski mobilni post/comment raspored. Mobilni kalendarski dani širine 27/31 px, pojedine desktop kalendarske mete i tablet/desktop post-akcije ostaju P2. Kraljevska sidebar foto-provjera, audit `mjesecev_ples` i `asfaltni_plamen` te završna matrica svih 37 dizajna ostaju otvoreni.
