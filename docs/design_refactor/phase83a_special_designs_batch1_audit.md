# Phase 83a — audit prvih devet posebnih dizajna

Datum: 2026-09-27. Ovaj korak je audit-only; aplikacijski kod nije mijenjan.

## Opseg i metoda

Stvarno su renderirani javni blog i post-detail za svih devet dizajna na 320, 390, 768 i 1440 px:

`soho` → `studio.html`, `magazin`, `nebeska_klasika`, `ponocna_elegancija`, `ruzicasti_vrt`, `stara_aleja`, `staza_prema_vrhovima`, `jedro_u_suton`, `misticno_jezero`.

Korištena je izolirana kopija baze `db_phase83a_trial.sqlite3` sa sintetičkim autorom i čitateljem, četiri objave kroz siječanj, kolovoz i rujan, vrlo dugim naslovom, dugim HTML sadržajem, postojećom slikom referenciranom samo u kopiji baze te komentarom autora i drugog korisnika. Izvorni `db.sqlite3`, sadržaj direktorija `media`, port 8000 i `main` nisu dirani.

Za svaku od 72 kombinacije dizajn × ruta × viewport mjereni su `documentElement.clientWidth/scrollWidth`, lokalni component overflow, širine kartice/slike/sidebara, prijelom naslova, kalendar i interaktivne mete. Na svakom dizajnu prošli su stvarni sigurni klikovi: prethodni i sljedeći mjesec, aktivni dan, arhivski mjesec, otvaranje/odustajanje editora komentara te like/unlike povratak s 0 → 1 → 0 bez trajne promjene.

Computed kontrast je izračunat za tekst komentara, autora komentara, akcijski gumb i autora objave. Kada između teksta i fotografske podloge postoji poluprozirni sloj, statički omjer nije dokaz stvarnog kontrasta piksela; takvi nalazi su dopunjeni vizualnim pregledom 1440 px prikaza. Postojeća mobilna pojačanja za komentare ne dokazuju desktop ni svaku fotografsku poziciju.

## Sažetak prioriteta

### P0

Nije pronađen P0. Sve stranice i kontrole rade, slike se učitavaju, a ni jedna od 72 kombinacije nema dokumentni horizontalni overflow.

### P1

1. **Stara aleja — osnovna čitljivost desktop heroja i akcijskih poveznica.** Na snimci od 1440 px naziv bloga i naslov objave stapaju se s fotografijom/poluprozirnom karticom. Plavi autor objave ima statički omjer približno 1,75:1. Tekst komentara na konkretnoj snimci izgleda čitljivo, ali poluprozirna kartica nad fotografijom daje nestabilan rezultat po poziciji; sintetički statički omjeri 1,29–1,55:1 na 768/1440 nisu pouzdani bez pikselnog uzorka, ali potvrđuju da nema neovisne neprozirne podloge.
2. **Jedro u suton — tamnoplave akcijske poveznice na fotografskoj kartici.** Autor objave mjeri približno 1,95:1, a vizualno su autor, like, komentari, otvaranje posta i arhivski linkovi teško čitljivi na 1440 px. Komentar autora na 768/1440 daje statički 1,57:1 nad promjenjivom fotografijom; mobilna puna podloga je dobra.
3. **Ružičasti vrt — presvijetle ružičaste/plave poveznice.** Autor komentara je približno 3,47–3,77:1, autor objave približno 3,55:1. Vizualna snimka potvrđuje da su komentari/otvaranje posta i dio kalendara/arhive blijedi na svijetloj fotografiji.
4. **Staza prema vrhovima i Mistična laguna — zadane plave post akcije.** Autor objave mjeri približno 3,41:1 odnosno 3,83:1; na 1440 px plavi autor/like linkovi vidljivo gube čitljivost, iako su glavni tekst i identitet dobri.
5. **Nebeska klasika, Ponoćna elegancija i Magazin — granični akcijski kontrast.** Autor objave mjeri približno 4,11:1, 4,39:1 i 4,37:1, malo ispod 4,5:1 za običan tekst. Magazinov podnaslov bloga dodatno se gubi preko svijetlog dijela hero fotografije.
6. **Tablet kalendarske mete na svih devet dizajna.** Na 768 px strelice ostaju 30×30. Aktivni dan je visok 28 px (`soho`, `magazin`) ili 34 px (preostalih sedam), a arhivski link 24–36,83 px. Phase 82c jamči 44 px samo do 600 px; tablet i dalje ostaje ispod preporučene mete.
7. **Mobilne akcije objave.** Na 320/390 px edit/delete komentara jesu 44×44 i vidljivi, ali like je visok 25,33 px, a link komentara 21 px. Funkcionalni su, ali imaju premalu vertikalnu metu.

### P2

- Lokalni overflow bez dokumentnog scrolla: Soho na 320 px (`soho-sidebar-section` +7 px; comment-body do +17 px) i oko +2 px na 390/768; Magazin sidebar +5 px na 320; Stara aleja i Jedro u suton sidebar +7 px na 320 i +2 px na 390. Sadržaj nije odrezan u pregledanim snimkama, ali vrijedi ukloniti višak.
- Vrlo dugi naslov u Sohou na 320 px dobiva samo oko 56 px korisne širine uz datum i raste na oko 333 px visine; na 390 px je oko 126 px / 233 px. Nema overflowa, ali ritam kartice je izrazito loš.
- Magazin ima isti uzorak u blažem obliku: naslov je oko 108 px širok i 346 px visok na 320 px.

## Matrica po dizajnu

| Dizajn | Raspored i slika | Kontrast / identitet na 1440 | Overflow i mete | Prioritet |
| --- | --- | --- | --- | --- |
| Soho / Studio | Lijevi sidebar na desktopu; sadržaj i slika se pravilno skupljaju, slika čuva omjer 2:1. Mobilni dugi naslov pretjerano uzak uz datum. | Čist urednički identitet, čvrsta neprozirna kartica; komentar 9,4–9,6:1, autor 5,5–5,6:1. | Nema doc overflowa; mali lokalni overflow na 320/390/768. Tablet mete 30 / 28 / 24 px. | P2 naslov i lokalni overflow; P1 tablet mete. |
| Magazin | Mobilno i tabletno koristi puni sadržaj; desktop lijevi sidebar + središnja kartica. Slika uredno prati karticu. | Snažan magazinski identitet, ali podnaslov je na hero fotografiji mjestimice gotovo nevidljiv. Komentar ≥5,8:1; autor oko 4,37–4,84:1. | Nema doc overflowa; sidebar +5 px na 320. Tablet mete 30 / 28 / 24 px. | P1 podnaslov i granični autor; P2 lokalni overflow. |
| Nebeska klasika | Mobilno jedan stupac; desktop kartica + desni sidebar. Slika 243×126 na 320 i 605×307 na 1440. | Prozračan, dosljedan identitet i dobra čitljivost kartica. Komentar oko 8:1, autor komentara 4,64–4,79:1; post autor oko 4,11:1. | Nema lokalnog ni doc overflowa. Tablet mete 30 / 34 / 36,83 px. | P1 post autor i tablet mete. |
| Ponoćna elegancija | Stabilan jedan/desni stupac raspored; slika i dugi naslov ostaju unutar kartice. | Vrlo jasan noćni identitet; glavni tekst i komentari visoko kontrastni. Post autor oko 4,39:1. | Bez overflowa. Tablet mete 30 / 34 / 36,83 px. | P1 granični post autor i tablet mete. |
| Ružičasti vrt | Stabilan raspored i slika; prozirne ružičaste kartice ovise o fotografiji. | Identitet je prepoznatljiv, ali više akcijskih/link boja je isprano: komentar autor 3,47–3,77:1, post autor 3,55:1. | Bez overflowa. Tablet mete 30 / 34 / 36,83 px. | P1 kontrast i tablet mete. |
| Stara aleja | Desktop koristi široku zajedničku prozirnu ploču; slika ostaje pravilna. | Najproblematičnija varijanta: naslov bloga/posta i plavi linkovi gube se na fotografiji. Komentari su na pregledanoj fotografiji vizualno čitljivi, ali nisu zaštićeni neprozirnom podlogom. | Bez doc overflowa; sidebar +7/+2 px na 320/390. Tablet mete 30 / 34 / 36,83 px. | Najviši P1 kontrast; P2 lokalni overflow. |
| Staza prema vrhovima | Uredan dark-overlay raspored; slika i tekst ne izlaze iz kartice. | Upečatljiv planinski identitet; osnovni bijeli tekst dobar, plavi post autor oko 3,41:1. Poluprozirni desktop komentar ovisi o fotografiji. | Bez overflowa. Tablet mete 30 / 34 / 36,83 px. | P1 akcijski kontrast i tablet mete. |
| Jedro u suton | Kartica spaja sadržaj i sidebar preko fotografske pozadine; slika uredna. | Snažan identitet, ali plave akcije su vrlo slabe: post autor 1,95:1; komentar autor na desktop/tabletu statički oko 1,57:1 nad fotografijom. | Bez doc overflowa; sidebar +7/+2 px na 320/390. Tablet mete 30 / 34 / 36,53 px. | Visoki P1 kontrast; P2 lokalni overflow. |
| Mistična laguna | Stabilna ljubičasta kartica + desni sidebar; slika uredno skalira. | Dobar vizualni identitet i čitljiv osnovni tekst; plavi post autor oko 3,83:1. Komentar i autor komentara na desktopu su oko 4,83/4,68:1. | Bez overflowa. Tablet mete 30 / 34 / 36,83 px. | P1 post akcije i tablet mete. |

## Blog naspram post-detaila

Obje rute stvarno su renderirane u svakoj kombinaciji. Njihov layout, slika, kontrast i kalendar bili su jednaki ili gotovo jednaki; očekivana razlika je broj prikazanih objava i nekoliko desetaka piksela visine zbog akcije „Otvori post”. Ni post-detail nije pokazao zaseban dokumentni overflow ili slom slike.

## Preporučeni mali sljedeći koraci

Ne popravljati sve u jednom commitu. Najmanji odvojeni zadaci:

1. Stara aleja: dati naslovu bloga/posta i post akcijama stabilnu neovisnu kontrastnu podlogu/boju na desktopu, uz vizualni test svijetle i tamne zone fotografije.
2. Jedro u suton: zamijeniti tamnoplave post/comment/archive poveznice lokalnom svijetlom akcijskom bojom; zasebno provjeriti transparentni komentar.
3. Ružičasti vrt: pojačati autor i akcijske linkove bez gubitka ružičastog identiteta.
4. Zajednički tablet ugovor: 44 px kalendar/arhiva na 601–1023/1199 px, odvojeno od kontrastnih popravaka.
5. Zajednički mobilni ugovor za like i link komentara; edit/delete već zadovoljavaju 44 px.

Phase 83a nije implementirao ni jedan od tih popravaka.
