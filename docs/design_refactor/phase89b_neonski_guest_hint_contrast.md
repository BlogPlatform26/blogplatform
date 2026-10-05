# Phase 89b — Neonski grad: poruka neprijavljenome

## Opseg

Ova uska faza rješava samo P1 poruku `Za komentiranje je potrebna registracija.` u `neonski_grad`. Ne mijenja shared stilove, druge dizajne, kalendar ni layout.

## Promjena

Lokalni selektor `[id^="comments-"] > .small.text-muted` sada daje poruci neprozirnu površinu `#0b081d`, tintu `#f0e4ff`, tanki lokalni obrub i mali padding. Površina je isti tamni neonski ton koji već koristi gradijentna kartica, pa poruka ostaje čitljiva i kad je pozadinska fotografija svijetla.

## Stvarni preglednik

Prije promjene je browser u blog i detail rutama pri 320, 390, 768 i 1440 px računao `rgba(33,37,41,.75)` bez vlastite podloge. Referentni omjer prema tamnoj osnovi bio je 1,15:1.

Nakon promjene svih osam stanja imaju computed `rgb(240,228,255)` na `rgb(11,8,29)`. Izmjereni omjer je **16,17:1**, znatno iznad zahtjeva 4,5:1, a ne ovisi o cropu fotografije. Document overflow je `0 px` na 320, 390 i 1440 px; na 768 px ostaje postojeći rubni `3 px` overflow, nepromijenjen ovim selektorom. Sigurni klikovi `Prethodni mjesec` i dana s objavom vode na očekivani query odnosno slugged detail bez mutacije.

## Regresijska zaštita

`blog/test_phase89b_neonski_guest_hint_contrast.py` potvrđuje da se lokalni ugovor renderira na blog i detail ruti te da se ne pojavljuje u `zlatno_polje`.
