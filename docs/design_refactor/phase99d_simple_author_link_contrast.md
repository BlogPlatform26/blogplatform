# Phase 99d — autorska poveznica u jednostavnim dizajnima

Phase 99a je za `simple_pattern`, `simple_image` i `simple_retro` ostavila konzervativne foto-granice, ne potvrđene padove. Izolirana sintetička baza i stvarni Chrome/Playwright sada su provjerili blog i detalj na 320/390/768/1440 px (**24 stanja prije i 24 poslije**). Pozadina neposredno ispod autorskog linka uzorkovana je iz snimke njegova područja s privremeno skrivenim glifom; computed boja i neprozirnost linka uzete su iz istog stanja. Tako se izbjegava pogreška računanja vanjske fotografije preko neprozirne post-kartice. `simple_image` stvarno prikazuje fotografiju police s knjigama, ali njegova kartica je `#fffefb`; `simple_retro` ima prozirnu post-karticu preko svijetle površine `#fbfaf6`.

Potvrđeni P1 nije bila vanjska fotografija, nego stilski izbor: boja `#3d6d86` odnosno `#2f6870` bila je postavljena na `.post-author-link` omotač, dok je stvarna `<a>` poveznica zadržavala svjetliju `#5b8ea2`. Pravilo sada obuhvaća stvarnu poveznicu, bez promjene kartice, fotografije ili desktop rasporeda.

| Dizajn | Prije | Poslije |
| --- | ---: | ---: |
| `simple_pattern` | 3,57:1 | **5,58:1** |
| `simple_image` | 3,57:1 | **5,58:1** |
| `simple_retro` | 3,45:1 | **6,03:1** |

Minimumi su jednaki kroz osam stanja svakog dizajna. Document i mjerene lokalne post/comment površine nisu imale horizontalni overflow; kalendar `simple_pattern`/`simple_image` također nije prelijevao. Za `simple_retro` ova skripta nije izmjerila vidljivi kalendar jer predložak ima skrivenu duplikatnu strukturu; ne iznosi se tvrdnja o tom zasebnom pitanju. Sigurni klik otvaranja objave prošao je za sva tri bloga na 390 px, bez mutacije. Vizualno je pregledan `simple_image` na 320 px: fotografija i svijetla kartica nisu uklonjene.

Na toj istoj snimci bijeli blog naslov na zlatnoj ploči djeluje slabije čitljiv, ali ova faza nije mjerila njegov efektivni omjer. To ostaje zaseban kandidat za provjeru u završnoj matrici, ne potvrđeni broj ni riješen nalaz. Izvorni DB, media, port 8000 i `main` nisu korišteni.

Uski Django test 2/2, `manage.py check`, `makemigrations --check --dry-run` i puni suite **205/205** su zeleni.
