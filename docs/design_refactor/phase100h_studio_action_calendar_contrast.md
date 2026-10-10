# Phase 100h — Studio lajk i današnji datum

Phase100g je na aktualnom Studiju (`soho`) potvrdila lajk 4.25:1 i današnji datum 3.61:1. Lokalna izmjena u `designs/studio.html` uključuje `.post-actions .btn-link` u postojeću smeđu boju poveznica #8b5a23 i mijenja samo pozadinu `.soho-calendar-day--today` iz #b67a2d u #8b5a23. Bijeli tekst i prsten datuma, ostala paleta, hero fotografija i desktop raspored ostaju isti. Spremljene postavke se ne mijenjaju.

## Provjera

Izolirana `.qa100e.sqlite3`, server8017; postojeći sintetički Studio autor2401, post11, dva komentara, sistemski sunrise hero. Polazište su osam blog/detail prikaza Studija iz Phase100g. Nakon izmjene ponovno pregledani blog i detail na 320/390/768/1440 px (**8 stanja**):

- Lajk computed #8b5a23 na neprozirnoj #fbf8f3 kartici: **5.53:1**.
- Današnji dan s objavom: bijeli tekst na #8b5a23: **5.86:1**.
- Document overflow **0** u svih osam stanja.
- Dodatni prazni Studio autor2403 (`qa100h_empty_soho`) potvrđuje isti datum bez objave na 390/1440; to je neinteraktivni DIV, ne lažna poveznica.
- Stvarni sigurni klik na aktivni dan, „Otvori post” i skok na komentare prolaze na 390 px. Bez lajkanja ili slanja komentara.
- Desktop hero/kalendar i mobilni komentari vizualno pregledani. Ovo nije nova provjera svih fotografija ili korisničkih paleta.

`manage.py check`: bez problema. `makemigrations --check --dry-run`: bez promjena. Puni suite **214/214** prošao u 101.316 s. `git diff --check` prolazi.

## Otvoreni opseg

Uski mobilni naslov Studija/Magazina, preostale desktop mete, fotografski naslov Magazina te završna matrica drugih 26 posebnih dizajna i puni tvornički Default nisu ovime završeni. Izvorna baza, media, repozitorij, port8000 i main nisu dirani.
