# Phase 100d — tvornički Simple naslovi objava

## Granica i nalaz

Phase100a je u aktualnom pregledniku potvrdila prenizak kontrast naslova objava: `simple_pattern` 3.93:1, `simple_image` 4.31:1 i `simple_retro` 3.11:1. Ova faza mijenja samo tvorničke boje naslova na tvorničkoj papirnatoj podlozi. Korisnički promijenjena boja naslova ili podloge zadržava vlastite vrijednosti. Naslov bloga, like kontrole, kalendarske mete i drugačije korisničke palete nisu proglašeni riješenima.

## Promjena i mjerenje

U `base.html` se za tvorničke Simple palete boja `--post-title-color` zamjenjuje tamnijom nijansom istog plavo-zelenog identiteta, uključujući lokalne `.blog-main-layout-row` i `.blog-posts-shell` varijable koje inače nadjačavaju `body`. Za `simple_pattern`/`simple_image` nova boja je `#2f6479` na neprozirnoj kartici `#fffefb`: izračun iz efektivnih browser boja 6.47:1. Za `simple_retro` boja je `#2f6870` na neprozirnoj zajedničkoj podlozi `#fbfaf6`: 6.03:1. To je kontrast CSS boje prema stvarnom neprozirnom sloju iza naslova, ne pretpostavka o fotografskoj podlozi.

Izolirana sintetička SQLite baza sadržavala je tri tvornička autora, tri objave i komentare; ni izvorna baza ni mediji nisu mijenjani. Chrome s učitanim Bootstrapom provjerio je prije/poslije blog i detail na 320, 390, 768 i 1440 px za sva tri dizajna — 24 stanja po prolazu. Nakon izmjene svih 24 stanja imaju odgovarajuću novu computed boju i `-webkit-text-fill-color`, bez horizontalnog document overflowa ili novog lokalnog overflowa kartice. Mobilni i desktop pregled potvrđuju da su uzorak, fotografija i retro podloga očuvani. Siguran klik „Otvori post” na 390 px provjeren je za sva tri dizajna bez lajkanja ili objavljivanja komentara.

Regresijski test provjerava blog i detalj sva tri tvornička dizajna te da se zaštita ne uključuje kod korisnički promijenjene boje naslova ili pozadine. `manage.py check`, `makemigrations --check --dry-run` i puni testni skup 214/214: zeleni. Privremena baza, preglednik, server i snimke uklonjeni nakon provjere.

## Otvoreno

- Phase100a potvrđuje prenizak kontrast like kontrole u dark/classic i Simple varijantama; odvojena uska faza.
- Tvornički `default` treba ponoviti bez legacy spremljene palete korisnika ID1.
- Završna verifikacijska matrica s komentarima i fotografskim zonama obuhvaća tek prvih 9/37 aktualno mjerenih dizajna. `working_37_design_evidence_matrix.md` je indeks, ne završni dokaz.
