# Phase 93c — akcije, komentari i kalendar Sjene ulice (`sjene_ulice`)

## Opseg

Na stvarnoj fotografiji prije promjene mali kontrolni tekst nije imao stabilnu pozadinu. Na tamnoj referentnoj zoni Bootstrap like bio je 4,16:1, autor desktop komentara 3,01:1, kalendarska navigacija 3,25:1; na svijetloj zoni izračunati omjeri padali su približno na 2,03:1, 1,22:1 i 1,41:1. Anonimna uputa bila je oko 7,16:1 na tamnoj, ali 1,47:1 na svijetloj zoni. Prozirno tijelo komentara također nije jamčilo čitljivost pri promjeni kadra.

Lokalni CSS teme sada daje likeu, anonimnoj uputi i kalendarskim strelicama neprozirnu dimno-smeđu podlogu `#241813` i toplo svijetli tekst `#f5d4ac` (**12,26:1**). Tijelo komentara dobiva istu neprozirnu podlogu; postojeći autor `#d8b084` na njoj postiže **8,61:1**, a bijeli tekst komentara **17,28:1**. Fotografija i desktopni raspored ostaju vidljivi oko tih ograničenih površina. Globalni stil i druge teme nisu mijenjani.

## Provjera u pregledniku

Izolirana sintetička baza s dva javna posta i komentarom, zaseban server na portu 8024 te učitan Bootstrap (`.row` = `flex`). Blog i post-detail provjereni prije/poslije na 320/390/768/1440 px (**osam stanja**). Computed foreground/background poslije su jednaki na obje rute i sve četiri širine. Kalendar je ostao 363/363/281/321 px visok po širinama, bez lokalnog overflowa. `document.scrollWidth/clientWidth` ostao je 305/320, 375/390, 753/768 i 1425/1440 px. Like ima 44 px visine na mobitelu, ali tablet/desktop ostaje 25 px.

Stvarni sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane rute. Like i komentari nisu mutirani.

## Testovi i otvoreno

Regresijski test provjerava blog/detail i izolaciju teme. Uski testovi 4/4, `manage.py check`, `makemigrations --check --dry-run` i puni Django skup 161/161 prošli su.

Ovo **ne zatvara** foto-neovisan kontrast naslova bloga, post naslova/tijela/autora/ostalih akcija i sidebara; prozirne površine ostaju zaseban P1. Dugi neprekinuti naslov bloga na 320/390 također ostaje P1. Mobilni kalendarski dani su samo 27/31 px široki, desktop dani/strelice i tablet/desktop post-akcije ostaju P2. Preostala dva neauditirana dizajna i završna matrica 37 dizajna nisu završeni.
