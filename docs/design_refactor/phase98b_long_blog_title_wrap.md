# Phase 98b — dugi neprekinuti naslov bloga

## Uzrok i promjena

Sintetički 55-znakovni neprekinuti `blog_name` prelijevao se preko zaglavlja. Standardni naslov u osnovnom dizajnu imao je na 320px `scrollWidth/clientWidth` 884/272 i dokument 908/320px; u `vodopad_u_magli` isto, a u `mjesecev_ples` 894/272 i dokument 918/320px. Tabletna širina također je mogla prelijevati. Samo `overflow: hidden` nije prihvatljiv jer bi odsjekao ime.

Zajedničko pravilo na kraju `base.html` dopušta lom neprekinutih riječi i ograničava širinu `.blog-page-title`. Radi i za predloške s poveznicom, i za posebna tekstualna zaglavlja poput Magazina i Nebeske klasike. Ne mijenja veličinu, boju ni pozadinu naslova i ne skriva tekst; obični naslovi ostaju vizualno isti.

## Preglednik i granice dokaza

Izolirana migrirana sintetička baza imala je po autora i objavu za svih 37 registriranih dizajna; svi autori imali su isto dugo ime bloga. Chrome/Playwright s učitanim Bootstrapom provjerio je blog i detalj na 320 i 390px za svih 37 dizajna, te četiri reprezentativna dizajna na 768/1440px: **164 stanja** nakon konačnog CSS pravila, bez document overflowa; gdje se prikazuje `.blog-page-title`, nije bilo ni lokalnog overflowa tog naslova. Na 320px osnovni i Vodopad sada imaju 272/272px naslov i 320/320px dokument; Mjesečev ples 272/272px i 320/320px. Posebni Magazin i Nebeska klasika provjereni su dodatno na sve četiri širine nakon proširenja selektora. Snimka Mjesečeva plesa na 320px potvrđuje da su sve riječi vidljive unutar zaštićene tamne podloge; panoramske fotografije ostaju.

Na blogovima sa standardnom poveznicom klik naslova ostao je na lokalnoj ruti, bez mutacije. Posebna zaglavlja bez te poveznice nisu označena kao neuspjeli klik. Ova faza ne tvrdi da je završna matrica kontrasta komentara i fotografskih zona svih 37 dizajna gotova.

## Testovi

Novi regresijski test prolazi blog i detalj svih 37 predložaka s dugim imenom. Uski test 1/1, `manage.py check`, `makemigrations --check --dry-run` i puni Django suite **199/199** su zeleni. Izvorni `db.sqlite3`, `media`, port 8000, `main` i produkcija nisu dirani.
