# Phase 42 — active design render matrix

## Opseg

- Registry-driven Django integracijski test izravno čita `Profile.TEMPLATE_CHOICES` kao jedini izvor aktivnih dizajna.
- Kontrolirani testni fixture sadrži autora, objavljeni post i komentar; public-blog view prirodno gradi arhivu i kalendar.
- Za svih 37 aktivnih ključeva test potvrđuje HTTP 200, očekivani razriješeni template, naslov i tijelo posta, comments-container, kalendarski/arhivski kontekst te aktivnu `--post-title-color` customization varijablu.
- `soho` se provjerava kroz postojeći resolver alias prema `studio.html`.
- Obiteljski manifest razlikuje samo devet aktivnih special dizajna od standard/shared dizajna. Guard potvrđuje da nema preklapanja, viška, manjka ni dupliciranih registry ključeva.
- Test koristi isključivo Django testnu bazu i ne mijenja produkcijske podatke ni datoteke.

## Rezultat provjera

- ciljani registry test: prolazi
- `manage.py check`: prolazi
- `manage.py makemigrations --check --dry-run`: nema promjena
- cijeli Django suite: 11 testova, svi prolaze

## Što ostaje za browser matricu

- serijski desktop smoke na 1440×900 za svih 37 dizajna
- serijski mobile smoke na 390×844 za svih 37 dizajna
- horizontalni overflow i console/page error provjere
- vidljivost ključnih post/meta/body/actions/comments/sidebar/calendar/archive elemenata u stvarnom DOM-u
- editor save, pojedinačni reset, reset-all i live-preview po relevantnoj layout/editor obitelji
- provjera computed CSS varijabli nakon editor promjena

Browser nije pokretan u ovoj fazi.
