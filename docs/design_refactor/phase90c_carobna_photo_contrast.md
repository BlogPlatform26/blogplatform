# Phase 90c — Čarobna ljubičasta: naslov, post i komentari na fotografiji

## Opseg i početno stanje

Phase 90a imala je samo referentne omjere prema `#542b7e`, ne dokaz nad
svijetlim kadrom fotografije. Prije promjene su naslov/podnaslov bili potpuno
prozirni, post kartica imala tek 9% tamnog sloja, a moderni komentar na
768/1440 imao je 34% bijelu podlogu pod svijetlim tekstom. Zato se dobro
čitanje nije moglo zajamčiti na svim zonama fotografije.

## Promjena

Naslov i podnaslov dobili su usku 84% tamnoljubičastu podlogu; post kartica
koristi isti 84% sloj. Moderni komentar ima 90% tamnoljubičasti sloj, s
preciznim selektorom koji pobjeđuje kasniji shared comment renderer. Fotografija
zamka/neba ostaje vidljiva oko tih površina i kroz sloj; boje, tipografija i
raspored desktopa ostali su prepoznatljivi. Phase 90b like i uputa nisu dirani.

## Mjerljiva granica kontrasta

Stvarni preglednik potvrdio je computed slojeve i boje na blogu i detalju
objave na 320/390/768/1440 px (osam stanja). Najsvjetliji mogući RGB kadar
fotografije, bijeli `#ffffff`, pod 84% slojem `rgba(33,12,56,.84)` postaje
najviše `#453358`. To je konzervativniji test od odabira pojedinog piksela
fotografije. Omjeri na toj granici su:

| Tekst | Minimalni izračunati omjer |
| --- | ---: |
| naslov/podnaslov bloga | 10,58:1 |
| naslov i tijelo posta | najmanje 9,96:1 |
| autor i akcijske poveznice posta | 7,78:1 |
| tekst komentara, preko dodatnog 90% sloja | 15,29:1 |
| autor komentara, preko dodatnog 90% sloja | 11,95:1 |

To su granice za zadane boje ovog dizajna, ne tvrdnja o proizvoljnim budućim
korisničkim overrideovima. Na svih osam stanja `document overflow` je 0 px;
naslov, kartica i komentar imaju `scrollWidth == clientWidth`. Pregled desktopa
na 1440 px potvrdio je očuvanu panoramsku fotografiju i kompoziciju. Na 390 px
sigurni klik prethodnog mjeseca otvorio je očekivani query, a dan s objavom
slugged detalj. Mutirajuće kontrole nisu kliknute.

Izolirana sintetička SQLite baza, port 8142 i privremeni browser korišteni su
samo za provjeru. Izvorni `db.sqlite3`, media i port 8000 nisu dirani.

## Testovi i otvoreno

`blog/test_phase90c_carobna_photo_contrast.py` štiti lokalni render na blogu i
detalju i odsutnost ugovora u drugom dizajnu. Ciljani test, `manage.py check`,
provjera migracija, `git diff --check` i puni Django skup (**144/144**) prošli
su završni gate.

Lokalni overflow kalendara pri 768 px (box 150/184, grid 117/168) i
tablet/desktop post-action touch mete ostaju P2. Preostalih pet dizajna i
završna matrica svih 37 još nisu dovršeni.
