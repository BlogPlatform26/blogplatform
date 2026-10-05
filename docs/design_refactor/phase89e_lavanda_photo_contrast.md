# Phase 89e — Polje lavande: čitljivost objave i komentara preko fotografije

## Nalaz i lokalni popravak

Phase89a je za link autora i akcije izmjerila samo 3,56:1 prema osnovnoj
lavandinoj boji, dok su objava i komentari stajali na prozirnim površinama.
Stvarni desktop crop miješao je tekst sa svijetlim nebom i tamnim cvjetovima;
omjer prema jednobojnoj osnovi zato nije bio foto-neovisan minimum. Prije
promjene su `blog-post-entry` i uputa neprijavljenome imali prozirnu pozadinu,
komentar na desktopu bijelu podlogu s alfom 0,34, a like je ostao Bootstrap
plav (`#0d6efd`).

Lokalno pravilo samo za `polje_lavande` daje objavi, komentaru, uputi i
arhivskom linku neprozirnu svijetloljubičastu podlogu `#f5e6fa`. Tekst,
autor, datum objave, post akcije uključujući like, komentar i arhiva koriste
tamnu ljubičastu `#512767`, s omjerom **9,58:1** za neprozirni tekst.
Godina datuma ostaje blago prigušena (`opacity: 0.86`), ali na toj podlozi
ima kontrastnu marginu. Mobilna i desktop tipografija, geometrija, hero
fotografija, boje kalendara i okolna lavandina površina ostaju. Popravak ne
mijenja druge dizajne.

## Stvarna provjera u pregledniku

Izolirana migrirana SQLite baza sadržavala je sintetičkog autora, objavu i
komentar. Javni blog i post detail pregledani su prije i poslije na 320, 390,
768 i 1440 px: **osam stanja** po prolazu. Na svim stanjima nakon promjene
computed podloge objave, komentara, upute i arhivskog linka bile su
`rgb(245,230,250)`; tekst, autor, comment autor, post akcije i like bili su
`rgb(81,39,103)`. Document overflow je 0 px na svakoj širini i ruti.
Podloga je neprozirna, pa isti izmjereni omjer vrijedi nad svijetlim i tamnim
zonama fotografije, neovisno o cropu.

Vizualni pregled 320 i 1440 px potvrđuje da je polje lavande i dalje vidljivo
oko kartice, a sadržaj kartice sada čitljiv. Sigurni klik `Prethodni mjesec`
na 390 px vodio je na `?year=2026&month=9`; klik na dan 5 s objavom vodio je
na slugged detail rutu. Nisu kliknute mutirajuće akcije.

## Regresija i otvoreno

`blog/test_phase89e_lavanda_photo_contrast.py` provjerava blog i detail te
izolaciju CSS ugovora od Zlatnog polja. Uski testovi 2/2, `manage.py check`,
`makemigrations --check --dry-run` i `git diff --check` prošli su. Puni
Django skup prošao je **138/138** testova.

Ovaj popravak ne proglašava hero naslov i prozirne profile/kalendar potpuno
foto-neovisnima na svim cropovima. Zasebno ostaju tablet/desktop post-action
touch mete od oko 21 px te završna matrica svih 37 dizajna. Izvorni
`db.sqlite3`, media i port 8000 nisu korišteni.
