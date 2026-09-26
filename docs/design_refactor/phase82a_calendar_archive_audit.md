# Phase 82a — audit kalendara i arhive

Datum: 2026-09-26. Audit je read-only prema aplikacijskom kodu. Korištena je izolirana baza `db_phase82a_trial.sqlite3`, korisnik `phase76_owner` i pet sintetičkih objavljenih postova: tri u rujnu 2026. (jedan dan s jednim i jedan dan s dva posta), jedan u kolovozu i jedan u siječnju. Izvorni `db.sqlite3`, mediji, port 8000 i `main` nisu dirani.

## Rute i ponašanje

- `/blog/<username>/` renderira aktivni dizajn te prihvaća `year`, `month` i `day`. Dan s jednim postom vodi na kanonski `/post/<id>/<slug>/`; dan s više postova filtrira blog rutu.
- Mjesečne strelice i arhivski linkovi vode na `/blog/<username>/?year=...&month=...`.
- `/blog/<username>/upoznaj-autora/` koristi `blog/author_detail.html`. View računa kalendar, arhivu i mjesečnu navigaciju, ali template namjerno prazni sidebare i ne renderira nijednu od tih komponenti. Parametri mjeseca/dana zato nemaju vidljiv učinak na toj stranici.

Stvarni sigurni klikovi prošli su bez promjene podataka: rujan → prethodni mjesec dao je samo `Kolovoz`; sljedeći je vratio tri rujanska posta; dan 12 vratio je točno dva posta; arhivski siječanj vratio je samo `Sijecanj`; dan 5 otvorio je `Rujan jedan`; „Natrag na blog” s autorove stranice vratio je korisnički blog.

## Mapa svih 37 dizajna

Devet posebnih dizajna izravno dijeli `blog/components/blog_calendar_grid.html` i `blog/components/blog_archive_entries.html`:

`soho` (`studio.html`), `magazin`, `nebeska_klasika`, `ponocna_elegancija`, `ruzicasti_vrt`, `stara_aleja`, `staza_prema_vrhovima`, `jedro_u_suton`, `misticno_jezero`.

Preostalih 28 registriranih dizajna nasljeđuje `blog/layouts/blog_design_base.html` i koristi zajednički, ali zasebno implementiran markup u `blog_left_sidebar.html` / `blog_right_sidebar.html`:

`default`, `dark`, `classic`, `default_right`, `dark_right`, `classic_right`, `simple_pattern`, `simple_image`, `simple_retro`, `litica_noci`, `podvodna_tisina`, `vodopad_u_magli`, `planine_u_magli`, `nebeski_mir`, `svemirski_horizont`, `zlatni_horizont`, `iznad_oblaka`, `sumska_svjetlost`, `polarna_svjetlost`, `zlatno_polje`, `neonski_grad`, `polje_lavande`, `carobna_ljubicasta`, `kraljevska_pozornica`, `dimni_akordi`, `sjene_ulice`, `mjesecev_ples`, `asfaltni_plamen`.

Zato jedan browser primjer ne dokazuje svih 37. Statička mapa pokriva oba stvarna render puta, postojeći `ActiveDesignRenderMatrixTests` prolazi kroz cijeli registry, a browser uzorak je uzeo `default`, `default_right`, `simple_retro`, `magazin` i `stara_aleja` — oba shared-markup sustava, lijevi/desni raspored i dvije posebne varijante.

## Mjerena browser matrica

Sve stranice izmjerene su na 320, 390, 768 i 1440 px. Ni jedan reprezentativni dizajn nije stvorio dokumentni horizontalni overflow (`scrollWidth == clientWidth`). Sažetak navodi najmanju vidljivu metu; vrijednosti su bile stabilne kroz breakpointove osim gdje širina stupca utječe na širinu ćelije.

| Dizajn / obitelj | Mjesečna strelica | Aktivni dan | Arhivski link | Font dana / arhive | Nalaz |
|---|---:|---:|---:|---:|---|
| `default` / standard-left | 30×30 | min. 27,81×29,33 | 28,93 px visine | 12 / 13 px | bez overflowa, ali sve mobilne mete su premale |
| `default_right` / standard-right | 30×30 | 24,48×29,33 na 320; 27,81×29,33 na 390 | 28,93 px | 12 / 13 px | mobilno premalo; na 768 kalendar je samo 144 px širok |
| `simple_retro` / simple-right | 30×30 | 26×36 | 25,54 px | 13 / 16 px | čitljiviji font arhive, ali sve interaktivne mete ostaju ispod 44 px |
| `magazin` / shared special | 30×30 | 33,15×28 na 320; 43,15×28 na 390 | 24 px | 12,8 / 16 px | bez overflowa, vertikalne mete izrazito niske |
| `stara_aleja` / shared special | 30×30 | 30,19×34 na 320; 40,19×34 na 390 | 36,83 px | 12 / 13 px | najbolji posebni uzorak, ali još ispod 44 px |

Na `default_right` pri 768 px dvostupčani desni sidebar daje kalendaru 144 px, a gridu 114,67 px. Obje 30 px strelice slažu se vertikalno uz naslov `RUJAN, 2026`, koji se lomi u više redaka; aktivni dan je širok samo 16,01 px. Vizualni pregled potvrđuje da sadržaj nije odrezan, ali je zbijen i navigacija više nema očekivani simetrični raspored. Na 1440 px kalendar ponovno ima normalan prostor.

`upoznaj-autora` nema kalendar ni arhivu na sva četiri viewporta i nema overflow. Njegov „Natrag na blog” visok je 30,33 px na 320/390, što je zaseban niži prioritet izvan kalendarskog opsega.

## Potvrđeni kvarovi i prioriteti

### Kritično / P0 — nevalidirani numerički query parametri ruše javnu stranicu

U izoliranom Django runtimeu s `Client(raise_request_exception=False, HTTP_HOST='localhost')` potvrđeno je:

- blog: `month=13` → 500 (`ValueError: month must be in 1..12`);
- blog: `month=9&day=32` → 500 (`ValueError: day is out of range for month`);
- blog: `year=10000&month=1` → 500 (`ValueError: year 10000 is out of range`);
- tekstualni `month=x` i `day=x` padaju na postojeći fallback i vraćaju 200;
- autor: `month=13`, `month=x` i `day=32` vraćaju 200; nevaljani mjesec pada na tekući mjesec, a `day` se ne koristi;
- autor: `year=10000&month=1` → 500 u `build_calendar_for_user`.

Uzrok je da `prepare_blog_context` provjerava samo može li se vrijednost pretvoriti u `int`, ali ne validira stvarni kalendarski raspon prije `timezone.datetime`; `author_detail` ograničava mjesec, ali ne godinu i nepotrebno gradi kalendar koji template ne prikazuje.

### Važno / P1 — mobilne dodirne mete

U oba render sustava strelice, aktivni dani i arhivski linkovi ostaju ispod približno 44 px na 320/390. Budući da problem postoji u zajedničkim komponentama/sidebareima, rješenje treba primijeniti na oba sustava, a ne pojedinačno na jedan od 37 dizajna.

### Važno / P1 — `default_right` tabletna gustoća

Pri 768 px dvostupčani sidebar prerano ostaje aktivan. Kalendar i arhiva rade, ali su zbijeni; naslov i navigacija gube očekivani horizontalni raspored. Treba zasebno odlučiti hoće li se na tom breakpointu koristiti jedan stupac ili širi kalendarski blok.

### Kozmetičko / P2 — čitljivost

Standardni i dio posebnih dizajna koristi 12 px za dane i 13 px za arhivu. Tekst je vidljiv, ali sitan na mobilnom. `magazin` pokazuje da 16 px arhiva može ostati uredna bez overflowa.

## Predloženi najmanji Phase 82b

Prvo popraviti samo P0: uvesti jednu zajedničku funkciju za normalizaciju `year/month/day` prije stvaranja datuma ili kalendara. Pri nevaljanom rasponu sigurno pasti na tekuću godinu/mjesec i ukloniti nevaljani dan; koristiti je u `prepare_blog_context` i `author_detail`. Dodati regresijske GET testove za `month=13`, `day=32`, nemoguć datum poput 31. veljače i ekstremnu godinu na obje rute. Ne dirati CSS u istoj fazi.

Mobilne 44 px mete i `default_right` raspored trebaju ostati dvije zasebne kasnije faze kako bi regresijski rizik bio ograničen.
