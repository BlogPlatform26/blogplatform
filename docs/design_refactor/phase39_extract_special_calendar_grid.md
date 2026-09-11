# Phase 39 — centralize special-design calendar grid

## Cilj

Centralizirati samo funkcionalnu jezgru kalendarske mreže u devet aktivnih special/full-custom dizajna, bez promjene lokalnih wrappera ili vizualnog identiteta.

## Promjena

- Dodana je tanka komponenta `blog/components/blog_calendar_grid.html`.
- Komponenta sadrži samo `month_calendar` / week / day petlje, empty ćeliju, lookup posta, post/archive URL grane i today uvjet.
- Svaki dizajn prosljeđuje svoje postojeće klase za empty, osnovni dan, dan s postom i današnji dan.
- Zaglavlje mjeseca, navigacija, weekday oznake, grid wrapperi, sekcije i sav CSS ostaju lokalni i nepromijenjeni.
- Neaktivni `vecer_*` templatei nisu mijenjani.

## Regresijska provjera

Za svih devet dizajnerskih prefiksa provjerava se šest stanja: prazna ćelija, običan dan, običan današnji dan, dan s jednim postom, dan s više postova i današnji dan s postom. Element, klase, URL i tekst moraju ostati semantički identični baselineu.

## Rezultat provjera

- svih 54 normaliziranih prije/poslije rendera identično je baselineu
- ciljani calendar-grid regresijski test prolazi
- `manage.py check` prolazi bez problema
- cijeli postojeći Django suite prolazi
- reprezentativni desktop i mobilni smoke-test prolazi za Studio i Nebesku klasiku
