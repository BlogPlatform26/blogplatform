# Phase 80a — mobilni audit postavki dizajna i live editora

Datum: 2026-09-20. Samo audit; bez promjene aplikacijskog koda. Korištena je izolirana kopija sintetičke SQLite baze s prijavljenim vlasnikom. Za osnovni prolaz aktiviran je Magazin, a za dostupnost panela pozadina Simple Uzorak. Nisu pritisnute akcije spremanja, vraćanja ni objave. Izvorna baza, mediji i port 8000 nisu dirani.

## Stvarne rute i prethodno pokriće

- `/blog/settings/?tab=dizajn&design_tab=predlosci` — izbor dizajna.
- `/blog/settings/?tab=dizajn&design_tab=uredivanje` — ulaz u live uređivač.
- `/blog/settings/?tab=dizajn&design_tab=ugodaj` — kursor, efekti i glazba.
- `/blog/settings/live-editor/naslovi/?section=naslovi` — live naslovi/datumi.
- Ista live-editor ruta sa `section=pozadine` — pozadine samo za podržane simple dizajne; na Magazinu je tab namjerno onemogućen.

Phase 77 je već provjerio šest glavnih settings tabova na 320/390/768/1440 i popravio avatar polje te usku sidebar navigaciju. Nije detaljno pregledao tri podtaba dizajna, obrasce ni live editor; ovaj audit pokriva upravo taj jaz. Rezultati Magazina nisu dokaz za svih 37 dizajna.

## Mjerenja

Na sve tri settings podstranice širina dokumenta bila je 305/375/753/1425 px za viewport 320/390/768/1440: nema horizontalnog dokumentnog preljeva. Sva tri dizajnerska podtaba bila su visoka 41 px; šest glavnih sidebar linkova na 320 px bilo je 40–41 px. Kartice dizajna ostale su u uskom stupcu (primjer 210 px širine). „Spremi dizajn” i akcija za spremanje ugođaja mjerili su 37 px, link „Otvori live uređivač” 37 px, select za ugođaj 37 px, a mali reset i odabir glazbe 30 px.

Live editor prelazi na jedan stupac ispod 992 px. Na 320/390/768/1440 px širina dokumenta opet je 305/375/753/1425 px, ali okvir previewa ima **unutarnji** višak širine približno 65/16/16/16 px; `overflow-x:hidden` ga odsijeca umjesto da stvori dokumentni scroll. Na 320 px jedna izmjerena granica preview iframea završava na x≈345, izvan viewporta, dok je njegov vanjski okvir do x≈291. Potrebna je zasebna provjera skaliranja iframea prije promjene CSS-a.

U live editoru tabovi „Naslovi/Pozadine” mjere 30 px visine, kartični „Vrati” gumbi 27 px, save/restore akcije 30 px, boje i brojevna polja 36 px te range slideri približno 21 px. Isti mali ciljevi prisutni su i u podržanom panelu pozadina Simple Uzorka (select i boje 36 px; akcije 30 px). Na Magazinu je „Pozadine” disabled, što je očekivano. Na 320 px akcije „Spremi promjene” i „Vrati sve naslove” bile su ispod početnog viewporta, oko y=1473; preview počinje još niže, oko y=1519. Akcije su dostupne vertikalnim pomicanjem, ali nije moguće istodobno gledati kontrolu i live preview u početnom mobilnom prikazu.

Stvarni klik na „Uređivanje” otvorio je odgovarajući podtab, a „Otvori live uređivač” stvarnu rutu. Na Simple Uzorku klikovi „Naslovi” i „Pozadine” prebacili su vidljivi panel bez spremanja. Boje i akcije za spremanje/vraćanje nisu aktivirane. Nije ustanovljen očit P0 kvar za siguran izolirani popravak u istoj fazi.

## Prioritet sljedećih faza

1. **Važno (Phase 80b):** mobilne dodirne mete live editora — tabovi, Vrati, save/restore, select/boje/brojčana polja i slideri. Minimalno 44 px gdje je primjenjivo; posebno provjeriti da povećanje ne uzrokuje preljev uske bočne ploče.
2. **Važno (Phase 80c):** mobilni preview — utvrditi uzrok unutarnjeg preljeva i omogućiti korisno vizualno uspoređivanje s kontrolama. Ne uklanjati samo `overflow:hidden` bez provjere iframe skaliranja.
3. **Važno (Phase 80d):** settings dizajnerski/ugođaj tabovi i akcije visine 30–41 px; uz to provjeriti kontrast/čitljivost kartica i odabira u stvarnom sadržaju.
4. **Kozmetičko / širi QA:** ponoviti reprezentativna mjerenja na drugim obiteljima dizajna, posebno onima s pozadinama i drukčijim naslovnim/date komponentama.

Ovaj dokument je kontrolna točka; migracije, modeli, predlošci i CSS nisu mijenjani.
