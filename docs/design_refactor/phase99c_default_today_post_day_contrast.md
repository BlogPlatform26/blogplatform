# Phase 99c — osnovni kalendar, današnji dan s objavom

Phase 99a je označila omjer osnovnog gradijenta dana s objavom kao neodređen. Stvarni Chrome pikselni uzorci pokazali su P1: kad se u `default` ili `default_right` današnji dan poklopi s danom s objavom, kasniji `.calendar-day-has-post` gradijent prekriva ljubičastu podlogu `.calendar-day-today`. Bijeli broj dana na svijetloj ispuni `#fbf6ef` imao je samo **1,08:1**; computed `background-color` i dalje je prijavljivao ljubičastu, pa samo čitanje te CSS vrijednosti ne bi otkrilo kvar.

Lokalno pravilo za presjek dviju klasa sada uklanja svijetli gradijent i vraća neprozirnu ljubičastu ispunu uz bijeli broj. Ostali dani s objavom, bočni raspored i desktop identitet nisu mijenjani. Chrome/Playwright s učitanim Bootstrapom i izoliranom sintetičkom bazom provjerio je blog i detalj oba dizajna na 320/390/768/1440 px (**16 stanja prije i 16 poslije**). Pikseli pozadine uzeti su s četiri unutarnja kuta kontrola, dalje od glifa, i uspoređeni s computed bijelim tekstom. Minimum je sada **5,78:1**. Vizualne snimke osnovnog bloga na 320 px prije/poslije potvrđuju da je broj ponovno čitljiv.

U svih 16 poslije-stanja document i lokalni kalendarski overflow ostali su 0. Sigurni klik dana s objavom provjeren je na blogu obaju dizajna pri 390 px, bez mutacije. Desktopni najmanji dan od 34×30 px ostaje zaseban P2 nalaz; ova faza rješava kontrast, ne veličinu kontrole. Izvorni DB, media, port 8000 i `main` nisu korišteni.

Uski Django test 2/2, `manage.py check`, `makemigrations --check --dry-run` i puni suite **203/203** su zeleni.
