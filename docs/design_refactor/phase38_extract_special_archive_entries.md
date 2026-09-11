# Phase 38 — centralize special-design archive entries

## Cilj

Centralizirati samo funkcionalnu jezgru popisa arhive u devet aktivnih special/full-custom dizajna, bez promjene DOM-a ili vizualnog identiteta.

## Promjena

- Dodana je tanka komponenta `blog/components/blog_archive_entries.html`.
- Komponenta sadrži samo loop preko `archives`, `year`/`month` URL, label/count i empty-state.
- Svaki dizajn prosljeđuje postojeću link CSS klasu i empty CSS klasu.
- Vanjski wrapperi, naslovi, ID-jevi, klase sekcija i raspored ostaju lokalni i nepromijenjeni.
- Obuhvaćeni su samo aktivni special templatei: Studio (`soho`), Magazin, Nebeska klasika, Ponoćna elegancija, Ružičasti vrt, Stara aleja, Staza prema vrhovima, Jedro u suton i Mistično jezero.
- Neaktivni `vecer_*` templatei nisu mijenjani.

## Regresijska provjera

Za svih devet dizajna normalizirani render archive jezgre uspoređuje se s baselineom za:

- jedan zapis (`year`, `month`, label i count)
- praznu arhivu i pripadajući empty-state

Element, CSS klasa, URL i tekst moraju ostati identični.
