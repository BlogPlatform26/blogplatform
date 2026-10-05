# Phase 88a — audit: Šumska i Polarna svjetlost

## Opseg i metoda

Audit obuhvaća `sumska_svjetlost` i `polarna_svjetlost`, javni blog i detail
pojedine objave na 320, 390, 768 i 1440 px: ukupno 16 stvarnih browser stanja.
Korištena je izolirana, migrirana SQLite kopija sa svježim autorima, objavama,
komentarima i arhivom. Originalni `db.sqlite3`, media i mutirajuće kontrole
nisu korišteni.

Za mete s prozirnom podlogom izračunan je referentni omjer prema deklariranoj
boji tijela. Budući da fotografija ostaje vidljiva ispod tih meta, stvarni
minimum kroz svjetlije i tamnije cropove može biti samo niži; sjene teksta nisu
tretirane kao pouzdana kontrastna površina. Computed stilovi potvrđuju da su
naslovi, sadržaj, autor, akcije, komentari i arhiva uglavnom prozirni.

## Zajednički nalazi

- Javne blog i detail rute rade, sigurni klikovi `Prethodni mjesec` i dana s
  objavom vode na očekivani query odnosno slugged detail bez mutacije.
- Fizički document overflow je `0 px` u svih 16 stanja.
- Oba dizajna imaju stvarni lokalni overflow kalendara na 768 px: Šumska
  svjetlost `176/150 px` (grid `160/117 px`), Polarna svjetlost `184/150 px`
  (grid `168/117 px`). To je isti strukturni sukob 44 px mobilne mete i uskog
  `col-md-3` sidebara koji je Phase87e riješila samo lokalno za Iznad oblaka.
- Na 320/390 px kalendarske strelice, dan s objavom, like i akcije imaju 44 px
  visine. Na 768/1440 px post-action mete ponovno padaju na približno 21–25 px;
  desktop strelice su 30 px.

## Šumska svjetlost

Tamno-zeleni naslov posta ima referentnih 4,96:1 prema `#d4e3c4`, a naslov
bloga 4,85:1. Međutim sadržaj i tekst komentara imaju samo 4,30:1, autor 3,54:1
i Bootstrap like 3,34:1 prema istoj osnovi. Sve te mete ostaju prozirne iznad
fotografije pa nisu foto-neovisne; vizualni pregled na svijetlom mobilnom cropu
potvrdio je potrebu za konzervativnim P1 tretmanom autora, sadržaja i akcija.

## Polarna svjetlost

Ovo je hitniji dizajn. Referentni omjeri prema `#4e7fbe` su: naslov bloga
3,79:1, naslov posta 3,82:1, sadržaj/komentar 3,55:1 i autor 3,57:1. Like
zadržava Bootstrap plavu `#0d6efd` bez lokalne površine: samo **1,09:1** prema
osnovi. Svijetli tekst i prozirne kontrole prelaze preko vrlo svijetlih i vrlo
tamnih zona aurora fotografije; vizualni pregled na 390 px pokazuje da se
čitljivost značajno oslanja na slučajnu zonu slike.

## Prioriteti

### P0

Nema potvrđenog P0: obje rute se renderiraju, nema document overflowa i sigurne
navigacije rade.

### P1

1. `polarna_svjetlost`: foto-neovisna površina ili tinta za like, zatim naslov,
   sadržaj, autor, komentare i arhivu. Like na 1,09:1 je najgori nalaz.
2. `sumska_svjetlost`: lokalno zaštititi autora, tijelo/komentar i post akcije;
   referentni minimumi 3,34–4,30:1 nisu sigurni preko fotografije.
3. Oba dizajna: lokalni 768 px calendar/grid overflow bez širenja shared CSS-a
   dok se ne potvrdi utjecaj na sve dizajne koji nasljeđuju bazu.

### P2

- Tabletne i desktop post-action te desktop kalendarske touch mete.
- Uska 320 px raspodjela naslova objave i datumske značke.

## Najmanji sljedeći popravak

Phase88b treba biti samo `polarna_svjetlost` P1 kontrast: najprije like i
post-action skup na punoj lokalnoj površini, zatim isti ugovor za sadržaj i
autora ako stvarni browser zadrži desktop identitet. Ne treba spajati sa
shared calendar promjenom ni Šumskom svjetlošću u istoj fazi.
