# Phase 82b — sigurna validacija kalendarskih query parametara

Datum: 2026-09-26. Uski P0 popravak potvrđenih 500 odgovora iz Phase 82a. CSS, mobilne mete i `default_right` raspored nisu mijenjani.

## Implementacija

Dodana je zajednička funkcija `normalize_calendar_query` u `blog/services.py`, koju koriste oba javna puta:

- `prepare_blog_context` za `/blog/<username>/`;
- `author_detail` za `/blog/<username>/upoznaj-autora/`.

Pravila su deterministička:

- godina mora biti 1–9998; gornja granica ostavlja valjanu završnu granicu perioda pri konstrukciji `datetime` vrijednosti;
- mjesec mora biti 1–12;
- dan se provjerava prema stvarnom broju dana odabranog mjeseca, uključujući prijestupne godine;
- nevaljana ili nenumerička godina/mjesec uklanja filter i vraća kalendarski prikaz na današnju godinu/mjesec;
- nevaljan ili nenumerički dan uklanja samo dnevni filter i zadržava valjani mjesečni filter;
- mjesec bez godine koristi današnju godinu;
- valjani `2024-02-29` ostaje dnevni filter.

## Regresijska pokrivenost

Novi testovi šalju GET na obje rute za:

- `month=13`;
- `year=2026&month=9&day=32`;
- nemoguć datum `2026-02-31`;
- `year=0` i `year=10000`;
- nenumeričke `year/month/day` vrijednosti;
- valjani prijestupni datum `2024-02-29`.

Posebno se potvrđuje da nevaljani dan pada na cijeli valjani mjesec, dok 29. veljače na blog ruti vraća samo post toga dana. Autorova ruta zadržava valjani kalendarski kontekst i više ne ruši ekstremnu godinu.

## Provjera nad izoliranom kopijom

Na `db_phase82b_trial.sqlite3`, kopiji postojeće lokalne probne baze, svih sedam query kombinacija vratilo je HTTP 200 na obje rute (14/14). Prije popravka su `month=13`, `day=32` i `year=10000` davali 500 na blogu, a `year=10000` i na autorovoj ruti.

Kopija je nakon provjere uklonjena. Izvorni `db.sqlite3`, mediji, port 8000, `main`, merge i deployment nisu dirani.
