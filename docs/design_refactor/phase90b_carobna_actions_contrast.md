# Phase 90b — Čarobna ljubičasta: uputa i like

## Opseg

Lokalno su popravljene dvije P1 mete potvrđene u Phase 90a: anonimna uputa
ispod komentara (1,38:1) i Bootstrap like gumb (2,31:1). Ostali prozirni
naslovi, sadržaj i komentari nisu ovom fazom proglašeni foto-neovisno
verificiranima.

## Promjena i mjerenje

Obje mete sada imaju neprozirnu tamnoljubičastu površinu `#211038` i
svijetloljubičasti tekst `#f6c7ff`. Izračunati efektivni kontrast je
**12,15:1**, neovisan o svijetlom ili tamnom kadru fotografije. Uski
selektori ciljaju samo ovaj dizajn; obližnji linkovi i zajednički renderer
nisu promijenjeni.

Stvarni preglednik potvrdio je computed boje na blogu i detalju objave pri
320, 390, 768 i 1440 px (osam stanja). U svih osam `document overflow` je
0 px. Na 320/390 like zadržava 44 px visine; postojeće tabletne/desktop
post-action mete od 21–25 px ostaju zaseban P2. Vizualni pregled pri 320 i
1440 px potvrdio je da mala neprozirna podloga ostavlja prepoznatljivu
fotografiju i ljubičasti desktop izgled vidljivima.

Na izoliranoj sintetičkoj bazi sigurni klik `Prethodni mjesec` na 390 px
otvorio je očekivani `?year=2026&month=9`, a klik na dan s objavom otvorio je
slugged detalj. Like, komentar i druge mutirajuće kontrole nisu kliknuti.
Izvorni `db.sqlite3`, media i port 8000 nisu korišteni.

## Granica i regresija

`blog/test_phase90b_carobna_actions_contrast.py` štiti render lokalnih
selektora na blogu i detalju te odsutnost tih selektora u drugom dizajnu.
`manage.py check`, `makemigrations --check --dry-run`, `git diff --check` i
puni Django testni skup (**142/142**) prošli su završni gate.

Sljedeće zasebno: foto-neovisan kontrast naslova/posta/komentara,
768 px lokalni kalendarski overflow, zatim preostalih pet dizajna i završna
matrica svih 37. Shared tablet post-action mete i pojedine kalendarske mete
ostaju otvorene.
