# Phase 79e — mobilni korisnički izbornik u zajedničkom zaglavlju

Problem je u zajedničkom `base.html` navbaru, pa potencijalno zahvaća sve prijavljene rute, ne samo `/new/` i `/post/<id>/edit/`. Na 320 px tekst `Pozdrav, phase76_owner` trebao je 180 px, a okvir je imao samo 108 px; `strong` je završavao na x=327 i ime je bilo odsječeno. Na 390 px okvir od 165 px također je bio manji od sadržaja. Dokument nije imao horizontalni scroll, jer je tekst bio odrezan unutar `overflow:hidden`.

Na mobilnom viewportu do 575,98 px sada se skriva samo riječ `Pozdrav,`, a ostaju avatar, korisničko ime i strelica izbornika. Manji razmak unutar korisničkog gumba i između stavki navigacije oslobađa dovoljno mjesta za ispitano ime. Za dulja imena postojeći `text-overflow:ellipsis` ostaje sigurnosna granica. Na 768 i 1440 px pozdrav i postojeći razmaci nisu promijenjeni.

| Ruta | Širina | Prije: okvir/sadržaj | Poslije: okvir/sadržaj | Dokument |
| --- | ---: | ---: | ---: | ---: |
| novi i uredi | 320 | 108/180 px | 116/116 px | 305 px |
| novi i uredi | 390 | 165/180 px | 116/116 px | 375 px |
| novi i uredi | 768 | 180/180 px | 180/180 px | 753 px |
| novi i uredi | 1440 | 180/180 px | 180/180 px | 1425 px |

U izoliranom pregledniku na 320 px profilni izbornik otvorio je stavku „Moj blog”, a tipka pretrage promijenila je `aria-expanded` na `true`; ništa nije poslano ni objavljeno. Regresijski test dodatno potvrđuje prijavne veze za gosta te profilni izbornik na oba obrasca. `manage.py check` i puni Django suite 46/46 prolaze. Izvorna baza i mediji nisu dirani.
