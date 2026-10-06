# Phase 91c — Kraljevska pozornica: naslov i podnaslov

## Opseg

Naslov bloga i podnaslov stajali su izravno preko kazališne fotografije. Phase91a je za svijetlu granicu foto-cropa izračunala samo 1,12:1 za naslov; tekstualna sjena ne jamči kontrast. Ovaj zahvat mijenja samo lokalni naslovni par: uske, neprozirne bordo površine `#2b0d14`, svijetla tinta `#fff0d9`, bez smanjenja panoramske fotografije ili promjene drugih dizajna. Naslov se po potrebi lomi unutar vlastitog stupca.

## Browser i kontrast

Izolirana migrirana SQLite baza s javnim postom i komentarom posluživana je na portu 8766. Stvarni Chrome provjerio je blog i detalj na 320/390/768/1440 px (**8 stanja**). U svakom je naslov, njegov link i podnaslov imao computed tintu `rgb(255, 240, 217)` na neprozirnoj podlozi `rgb(43, 13, 20)`, uz opacity 1: **15,99:1**, neovisno o svijetlom ili tamnom kadru. Siguran stvarni klik na `Prethodni mjesec` na sve četiri širine otvorio je očekivani `?year=2026&month=9`; mutirajuće kontrole nisu kliknute.

Phase91e ponovila je provjeru s učitanim vanjskim Bootstrap CSS-om: raniji excess i izlazak profila bili su artefakti nepotpunog browser prikaza. S potpunim stilovima naslov ostaje unutar viewporta, document overflow je 0 px na sve četiri širine i kontrast ostaje 15,99:1; panoramski prikazi 390/1440 vizualno su ponovno pregledani. Na 768 px lokalni kalendarski overflow bio je stvaran nalaz, obrađen zasebno u Phase91e.

## Provjera

`blog/test_phase91c_kraljevska_title_contrast.py` štiti lokalni ugovor na blogu i detalju. Uski test, `manage.py check`, `makemigrations --check --dry-run`, `git diff --check` i puni Django skup (**148/148**) prošli su završni gate.
