# Phase 100g — aktualna matrica Studio / Magazin

Provjera na aplikacijskom commitu `574720a`, 10. listopada 2026. Ovo je dovršena serija mjerenja s otvorenim nalazima, **ne potvrda da oba dizajna potpuno prolaze**. Aplikacijski kod nije mijenjan.

## Uzorak i metoda

Registrirani `soho` (Studio, ne ključ `studio`) i `magazin`; sintetički autori 2401/2402, objave 11/12, dva komentara po objavi (čitatelj i autor). Dulji naslov objave i dva odlomka teksta. Izolirana `.qa100e.sqlite3`, server8017. Za oba autora eksplicitno odabran postojeći sistemski `soho_sunrise_valley`; sve ostalo tvorničko. Hero fotografija u svih 16 stanja učitana s naturalWidth > 0.

Blog i detail na **320/390/768/1440 px**, ukupno **16 stanja**. Bootstrap učitan. Kontrast je izračunat iz computed foreground boje, alphe i neprozirnog pozadinskog sloja, uz kompoziciju prozirnih međuslojeva. Fotografije/gradijenti ne zamjenjuju se pretpostavljenom punom bojom. Studio podnaslov uključuje opacity 0.82. CSS `color(srgb ...)` dana kalendara zasebno je pretvoren u RGB 0–255; prvotni generički parser za taj format dao je pogrešan rezultat, koji nije korišten u tablici.

## Najniži kontrast kroz blog/detail i sve širine

| Element | Studio / soho | Magazin |
| --- | ---: | ---: |
| Naslov bloga | 12.28 | otvoreno, tekst preko fotografije |
| Podnaslov bloga | 5.09 (opacity uključen) | 14.15 (neprozirni caption) |
| Naslov objave | 14.26 | 9.45 |
| Tijelo objave | 9.39 | 7.49 |
| Autor objave / obične akcijske poveznice | 5.53 | 8.01 |
| Stvarni gumb lajk | **4.25 — P1** | 8.01 |
| Tekst komentara | 7.86 mobilno / 9.58 tablet i desktop | 7.49 |
| Autor komentara | 4.63 mobilno / 5.64 tablet i desktop | 8.01 |
| Poruka gostu | 6.57 | 6.65 |
| Današnji dan s objavom | **3.61 — P1** | 6.49 |
| Obični dan bez objave | 8.33 | najmanje 6.49 za cijelu skupinu dana |
| Arhiva | 8.08 | 8.01 |
| Navigacija mjeseca | 9.75 | 8.74 |

Komentari su provjereni i na desktopu; iza njih u ovom uzorku postoji dovoljan neprozirni/kompozitni sloj. Magazinov naslov bloga nalazi se preko fotografije i gradijenta, pa mu ovaj computed postupak **ne dokazuje** stvarni omjer. Na 320 i 1440 vizualno je pregledan, ali treba pikselna provjera položaja glifova prije zaključka. Nisu iscrpljene proizvoljne korisničke fotografije i palete.

## Raspored i mete

Document overflow je 0 u svih 16 stanja. Lokalni scrollWidth−clientWidth je 0 za main shell, sidebar, karticu objave i oba comment-body elementa. To ne znači da je raspored ugodan:

- Studio na 320 px ostavlja naslovu samo **36.90 px** širine uz datum; naslov se pretvara u visok, vrlo uzak stupac (230.72 px). Na 390 naslov je širok 106.90 px. Vizualno potvrđeno na 320. Korijen je flex red s datumom u `components/special_designs/studio_post_card.html`.
- Magazin na 320 px ostavlja naslovu 88.90 px, visina 259.13 px. Potrebna zasebna prilagodba mobilnog reda naslov/datum, uz očuvan desktop.
- Interaktivni kalendarski dan s objavom na 320/390/768: Studio oko 46.2×46.2 px (transform), Magazin 44×44. Obični neinteraktivni dani nisu touch mete.
- Na 1440: Studio interaktivni dan 30.8×29.4, Magazin 29.33×28; strelice 30×30; arhiva 24 odnosno 25.33 px visine. Preostaje odluka/provedba postojećeg cilja većih desktop touch meta.
- Lajk i post-akcije na 320/390/768 imaju 44 px visine. Na 1440: lajk 25.33, poveznice 21 px. Phase98a tablet prolaz nije regresirao.

## Sigurna navigacija

Za oba dizajna na 390 px stvarno kliknuti prethodni mjesec (rujan, bez objava), sljedeći mjesec (listopad), aktivni dan (canonical detail), arhivski listopad i „Otvori post” (detail s komentarima). Bez slanja lajkova ili komentara. Studio mobilni sadržaj i Magazin mobilni/desktop hero vizualno pregledani.

## Sljedeći mali zahvati

1. Studio lajk: Bootstrap #0d6efd ostao na gumbu; postojeće akcijske poveznice su #8b5a23 i prolaze. Lokalno uključiti gumb u boju teme, provjeriti oba prikaza/četiri širine.
2. Studio današnji dan: `designs/studio.html:344` koristi #b67a2d s bijelim tekstom. Potamniti samo aktivnu podlogu i provjeriti i today/has-post kombinaciju.
3. Odvojeno prilagoditi mobilni naslov/datum Studija i Magazina bez promjene desktop rasporeda.
4. Zatvoriti neizmjereni fotografski kontrast Magazin naslova; zatim preostale mete.

Sljedećih 26 posebnih dizajna još nema aktualnu završnu seriju. Prvih devet iz Phase100a imaju navedene naknadne popravke, ali tvornički Default još treba punu provjeru. Ovo povećava obuhvat aktualnog pregleda, ne broj dizajna koji su potpuno završeni.

Ova faza ne mijenja aplikaciju i ne ponavlja puni suite: zadnji puni suite na istom aplikacijskom kodu u Phase100f je 214/214. Izvorni repozitorij, baza, media, port8000 i main nisu dirani.
