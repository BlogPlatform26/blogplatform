# Phase 94c — foto-neovisan kontrast Mjesečeva plesa (`mjesecev_ples`)

## Opseg

Phase94a potvrdio je prozirne površine preko mjesečeve fotografije: naslov i podnaslov bez podloge, kartice na samo 22% tamnog sloja te desktop komentar na 34% bijelom sloju. Bootstrap like imao je 4,16:1, a autor desktop komentara 3,88:1 već na tamnoj referentnoj osnovi. Phase94b sedmodnevni kalendar nije mijenjan.

Lokalni CSS Mjesečeva plesa sada sidri naslov/podnaslov, objavu, komentar, kalendar, arhivu, bočne kartice i profil na neprozirnu tamnu `#241b18` podlogu. Like i kalendarska navigacija koriste toplu zlatnu boju umjesto Bootstrap plave; anonimna uputa ima vlastitu tamnu podlogu. Današnji dan ima neprozirnu tamnokaramelnu boju, a blijeda godina objave čitljiviju boju. Fotografija, noćna paleta i desktopni trostupčani identitet ostali su vidljivi oko sadržaja.

## Mjerljiv kontrast

Vrijednosti prije dolaze iz Phase94a i njegove computed alfa-kompozicije na `#15110f` odnosno krajnje svijetloj mogućoj podlozi `#ffffff`. Svijetla granica prije **nije** tvrdnja da konkretni foto-piksel ima tu boju. Poslije su preglednikom potvrđene neprozirne podloge i computed boje, pa omjer više ne ovisi o svijetloj/tamnoj foto-zoni. Sjena teksta nije uračunana.

| Element | Prije: tamna / svijetla granica | Poslije: obje zone |
| --- | ---: | ---: |
| naslov/podnaslov bloga | 15,20 / 1,23:1 | 13,66:1 |
| naslov objave | 15,88 / 1,37:1 | 14,31:1 |
| tijelo objave i tekst komentara | 15,04 / 1,30:1 za tijelo; desktop komentar 4,86 / 1,09:1 | 13,55:1 |
| autor objave, akcijske veze i autor komentara | autor/akcije 12,01 / 1,04:1; desktop komentar 3,88 / 1,14:1 | 10,82:1 |
| like | 4,16 / 2,78:1 | 10,82:1 |
| anonimna uputa | 7,68 / 1,16:1 | 12,69:1 |
| kalendarska navigacija | 5,64 / 1,01:1 | 10,82:1 |
| današnji dan s objavom | 4,54 / 2,64:1 | 9,27:1 |
| arhivska veza | 11,61 / 1,37:1 | 10,53:1 |

Ovi omjeri vrijede za navedene tekstove i provjerena stanja Mjesečeva plesa; nisu dokaz da je kontrast svih 37 dizajna riješen.

## Stvarni preglednik i regresije

Izolirana migrirana sintetička SQLite baza s objavom i komentarom bila je na portu 8029. Blog i detalj pregledani su na 320/390/768/1440 px (**osam stanja**) s učitanim Bootstrapom (`.row` = `flex`). U svih osam computed pozadine naslova, objave, komentara, upute, kalendara, arhive i profila bile su neprozirne `rgb(36,27,24)`; like i kalendarske strelice imali su zlatnu boju. Nema dokumentnog ni lokalnog overflowa u reprezentativnom sadržaju:

| Širina | Dokument client/scroll | Kalendar client/scroll | Komentar client/scroll |
| ---: | ---: | ---: | ---: |
| 320 | 305/305 | 231/231 | 104/104 |
| 390 | 375/375 | 259/259 | 174/174 |
| 768 | 753/753 | 375/375 | 536/536 |
| 1440 | 1425/1425 | 259/259 | 504/504 |

Vizualno su uspoređene svjetlije i tamnije zone postojeće fotografije; panoramski kadar i desktop karakter ostali su očuvani. Na 390 px sigurni klikovi prethodnog mjeseca, dana s objavom i arhive otvorili su očekivane URL-ove. Like i komentar nisu mutirani.

Regresijski testovi `blog/test_phase94c_mjesecev_photo_contrast.py` provjeravaju blog, detalj i izolaciju od default dizajna. Uski testovi (2/2), `manage.py check`, `makemigrations --check --dry-run` i puni Django skup (171/171) prošli su bez pogreške.

## Ostatak cilja

Uski 320px naslov i tekst komentara te mobilni kalendarski dani široki 27/31 px ostaju geometrijski/touch P2, kao i zajedničke tablet/desktop post-akcije i pojedine desktop kalendarske mete. `asfaltni_plamen` još nije auditiran; Kraljevska pozornica sidebar foto-kontrast i završna matrica svih 37 s komentarima/fotografskim zonama ostaju otvoreni. Izvorni `db.sqlite3`, media i port 8000 nisu dirani.
