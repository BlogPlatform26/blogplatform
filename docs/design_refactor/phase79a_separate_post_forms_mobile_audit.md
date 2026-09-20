# Phase 79a — zasebni obrasci za post: mobilni pregled

Datum: 2026-09-20. Pregled je izveden u izoliranoj kopiji SQLite baze, s prijavljenim sintetičkim vlasnikom i sintetičkim draftom. Nije poslan nijedan obrazac niti je mijenjana izvorna baza.

## Nalazi i prioritet

1. **Kritično — uređivanje posta je nedostupno.** `GET /post/1/edit/` vraća 404 (`post_detail`: “No Post matches the given query”). U `blogplatform/urls.py` ruta `post/<int:post_id>/<slug:post_slug>/` na retku 42 prethodi ruti `post/<int:post_id>/edit/` na retku 58, pa `edit` biva protumačen kao slug. Zbog toga se UI obrasca za uređivanje nije mogao mjeriti ni interaktivno isprobati. Najmanji sljedeći popravak: staviti specifične `edit/` i `delete/` rute prije generičke slug-rute te dodati regresijski test rezolucije i vlasničkog GET-a.
2. **Važno — kontrola razmaka redaka ne stiže u HTML.** U `create_post.html` i `edit_post.html` elementi `blogplatformDirectSpacingStyle` i `blogplatformDirectSpacingScript` nalaze se iza `{% endblock %}`. Na stvarno renderiranom `/new/` oba su odsutna u DOM-u; nema ni kontrole u alatnoj traci. Za edit je potvrđena ista struktura izvornog predloška, ali renderiranje blokira prethodni nalaz.
3. **Važno — premale mete za dodir.** Na `/new/` naslov, kategorija, slika, video, tagovi, datum i oba gumba imaju visinu 37 px na svim širinama. Gumbi CKEditora imaju 30 px; neke su ikone široke samo 16 px. Potrebno je povećati dodirne mete bez loma rasporeda.
4. **Kozmetičko — na 320 px jedan element zaglavlja prelazi desni rub.** `strong` u korisničkom pozdravu završava na x=327. Nije zabilježen horizontalni scroll dokumenta (`scrollWidth=305` uz viewport 320), ali dio teksta može biti odrezan.

## Mjerenja `/new/`

| Viewport | Širina dokumenta | Polja / akcije | CKEditor alatna traka | Prelijevanje |
| ---: | ---: | ---: | ---: | --- |
| 320 | 305 | 37 px | 255 px, bez unutarnjeg scrolla; gumbi 30 px | pozdrav x=327 |
| 390 | 375 | 37 px | 325 px, bez unutarnjeg scrolla; gumbi 30 px | nije nađeno |
| 768 | 753 | 37 px | 279 px, bez unutarnjeg scrolla; gumbi 30 px | nije nađeno |
| 1440 | 1425 | 37 px | 599 px, bez unutarnjeg scrolla; gumbi 30 px | nije nađeno |

Na 320 px naslov i kategorija te ostala standardna polja završavaju na x=281, unutar vidljivog prostora. Klik/fokus naslova i kategorije uspio je bez predaje obrasca. CKEditorov izbornik naslova otvorio se i prikazao četiri opcije. U probnoj bazi kategorija nema opcija. Kontrola slike je jedna datoteka (`multiple=false`); dijalog za odabir datoteke nije otvaran. Gumbi objave i spremanja drafta nisu kliknuti.

## Granica pregleda

`/post/1/edit/` je provjeren na 320, 390, 768 i 1440 px, ali na svakoj širini prikazuje istu Django 404 stranicu; ta mjerenja nisu mjerenja obrasca. Zato je ova faza samo audit. Nakon popravka redoslijeda ruta treba ponoviti puni mobilni pregled uređivanja i tek zatim odlučiti o zajedničkim stilskim popravcima. Nisu mijenjani aplikacijski kod, migracije ni testovi.
