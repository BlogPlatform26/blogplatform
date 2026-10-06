# Phase 91b — Kraljevska pozornica: like i anonimna uputa

## Promjena

`kraljevska_pozornica` lokalno dodaje neprozirnu površinu `#2b0d14` i tintu `#fff0e2` za Bootstrap like i poruku neprijavljenome. Time se mete odvajaju od svijetlih i tamnih zona fotografije, uz zadržan topli kazališni identitet.

## Kontrast i raspored

Omjer `#fff0e2` prema `#2b0d14` je **16,08:1**, pa vrijedi neovisno o cropu i prelazi 4,5:1 s velikom marginom. Promjena je ograničena na dvije kontrole i ne mijenja stupce, kalendar ni druge dizajne.

Izolirana migrirana SQLite baza s jednim javnim postom i komentarom posluživala je stvarne rute bloga i detalja na zasebnom portu 8765. Headless Chrome provjerio je **8 stanja** (obje rute na 320/390/768/1440 px): obje kontrole postoje i imaju computed `rgb(255, 240, 226)` na neprozirnom `rgb(43, 13, 20)` u svakom stanju. Like je na 320/390 visok 44 px; na 768/1440 ostaje 25 px, što pripada zasebnom P2 zahvatu za tablet/desktop akcijske mete. Stvarni nemutirajući klik na prethodni mjesec otvorio je očekivani `?year=2026&month=9` na sve četiri širine. Like i komentiranje nisu kliknuti. Vizualno su pregledani 390 i 1440 px detalji; toplu kazališnu paletu kontrola zadržava.

Naknadna provjera u Phase91e otkrila je da u prvom browser pokretanju vanjski Bootstrap CSS nije bio učitan zbog TLS provjere CDN-a. Tadašnji navodni document excess (+14/+6 px) i profilni panel izvan viewporta bili su artefakti nepotpunih stilova, **ne potvrđeni kvar dizajna**. Nakon učitavanja Bootstrap CSS-a stvarni blog/detalj imaju 0 px document overflowa i profil ostaje unutar viewporta na 320/390/768/1440. Kontrast ove faze ponovno je izmjeren s učitanim CSS-om: 16,08:1 u svih osam stanja.

## Regresijska zaštita

`blog/test_phase91b_kraljevska_guest_like_contrast.py` pokriva lokalni ugovor na javnom blogu i detail ruti. Uski test, `manage.py check`, `makemigrations --check --dry-run`, `git diff --check` i puni Django skup (**147/147**) prošli su završni gate.
