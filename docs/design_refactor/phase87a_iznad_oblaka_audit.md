# Phase 87a — `iznad_oblaka` audit

## Opseg i fixture

`iznad_oblaka` je registrirani dizajn iz
`blog/templates/blog/designs/iznad_oblaka.html`. Ovaj docs-only audit obuhvaća
javni blog i post-detail na 320, 390, 768 i 1440 px, ukupno osam stvarnih
browser stanja.

Korištena je izolirana, migrirana SQLite kopija sa svježim autorom, praznim
`UserBlogPreference.data`, jednom objavljenom objavom, drugim korisnikom i
komentarom. Originalni `db.sqlite3`, media i mutirajuće kontrole nisu korišteni.

## Metoda kontrasta

Computed boje i geometrija očitani su iz preglednika. Budući da su header,
postovi, kalendar i arhiva većinom transparentni, kontrast nije računat prema
fallback boji tijela. Za svaku metu uzorkovano je devet točaka pravokutnika na
stvarnoj fotografiji `iznad_oblaka.jpg`, uz njezin stvarni responsive crop,
deklarirani pastelno-bijeli gradijent te alpha površine kontrole ili kartice.
Poluprozirna boja teksta također je komponirana prije WCAG izračuna. Sjene
teksta nisu tretirane kao pouzdana kontrastna površina.

## Efektivni kontrast

Najniže izmjerene vrijednosti kroz osam stanja:

| Meta | Minimum | Nalaz |
| --- | ---: | --- |
| naslov bloga | **1,00:1** | fail; bijeli tekst prelazi preko gotovo bijelog neba |
| tagline | **1,00:1** | fail |
| naslov posta | **1,02:1** | fail; 768 px raspon 1,03–4,41 |
| tijelo posta | **3,88:1** | fail na 768; 4,24 na 1440 |
| autor posta | **3,84:1** | fail |
| like kontrola | **3,84:1** | fail; nasljeđuje Bootstrap plavu |
| komentar / open-post akcija | **3,84:1** | fail |
| autor komentara | **3,63:1** | fail |
| tekst komentara | 4,79:1 | pass; minimum ostaje iznad 4,5 |
| anonimna uputa | 6,46:1 | pass |
| kalendarska navigacija | **1,01:1** | fail; vrlo svijetla tinta na svijetloj alpha površini |
| kalendarski dan s postom | 5,31:1 | pass |
| arhivska poveznica | **4,45:1** | marginalni fail |

Vizualni pregled na 390, 768 i 1440 px potvrđuje da naslov/tagline, naslov
posta, naslovi komentara/arhive i kalendarske strelice blijede ili nestaju na
fotografiji. Tijelo posta je vidljivije, ali na svijetlim zonama nema potrebnu
marginu. Komentar ima dovoljno čitljiv tekst, dok njegova plavo-siva autorska
poveznica ne doseže 4,5:1.

## Geometrija i touch mete

Dokumentni overflow je `0 px` u svih osam stanja. Kalendar ipak ima lokalni
overflow:

- 320 px: grid `204/203 px` — samo subpikselno zaokruživanje;
- 390 px: grid `274/273 px` — samo subpikselno zaokruživanje;
- 768 px: kalendar `177/150 px`, grid `161/118 px` — stvarni strukturni problem;
- 1440 px: kalendar `260/260 px`, grid `229/228 px` — subpikselno zaokruživanje.

Na 320/390 px kalendarska navigacija, dan s postom, like i post akcije imaju
44 px ili više u visinu. Na 768 px like je oko 25 px, a comment/open-post akcije
oko 21 px. Na 1440 px kalendarske strelice su 30 × 30 px, dan s postom oko
28,5 × 35,4 px, arhivska poveznica oko 33 px visoka te post akcije 21–25 px.
To su P2 veličine ciljeva; shared tablet post-action problem nije lokalno
popravljan ovim auditom.

Na 320 px naslov posta dobiva samo oko 53 px širine uz datumsku značku i lomi
se u više vrlo uskih redaka. Nema izlaska iz dokumenta, ali je raspored krhak.

## Sigurne navigacije

Na 390 px potvrđeno je:

- `Prethodni mjesec` otvara očekivani `year=2026&month=9` query;
- dan s postom otvara slugged detail;
- `Otvori post` otvara isti detail.

Nije aktiviran like, komentar, spremanje, objava ni druga mutacija.

## Prioriteti

### P0

Nema potvrđenog P0. Obje javne rute se renderiraju, nema dokumentnog overflowa
i sigurne navigacije rade.

### P1

1. Naslov bloga, tagline i naslov posta trebaju diskretnu foto-neovisnu
   kontrastnu zaštitu; minima su 1,00–1,02:1.
2. Kalendarska navigacija treba stabilnu lokalnu tintu/površinu; minimum je
   1,01:1.
3. Tijelo posta, autor i post akcije trebaju pouzdanu svijetlu podlogu ili
   tamniju lokalnu tintu; minima su 3,84–4,24:1.
4. Autor komentara i arhivska poveznica trebaju malu kontrastnu korekciju;
   minima su 3,63:1 i 4,45:1.

### P2

1. Ukloniti stvarni 768 px lokalni overflow kalendara bez skrivanja sadržaja
   ili smanjivanja mobilnih touch meta.
2. Proširiti shared touch-target pravila na tabletne post akcije i, zasebno,
   lokalne desktop kalendarske/arhivske mete.
3. Stabilizirati 320 px raspodjelu širine između naslova posta i datumske
   značke.

## Sljedeća najmanja faza

Predložena Phase 87b je uski kontrastni popravak samo za naslov bloga, tagline
i naslov posta: kompaktna, foto-neovisna lokalna površina koja čuva pastelnu
fotografiju i ne mijenja raspored kalendara, akcija ili komentara. To uklanja
najgore potvrđene minimume 1,00–1,02:1 uz najmanji rizik i jasnu browser
regresijsku provjeru na svih osam stanja.
