# Phase 89d — Zlatno polje: kontrast sadržaja preko fotografije

## Nalaz i promjena

Phase89a izmjerila je autora, akcije i arhivu na 3,17–4,30:1 prema osnovnoj
zlatnoj boji, uz prozirnu karticu preko promjenjive fotografije pšenice. Lokalni
CSS sada postavlja neprozirnu pergamentnu podlogu `#fff8e4` za karticu objave,
arhivske poveznice i uputu neprijavljenome te tintu `#4b2d05` za autora,
meta-podatke, akcije i komentare. Desktop kartica komentara dobiva istu
neprozirnu podlogu; na 320/390 px ostaje prethodno provjerena mobilna podloga
`#fff6df`. Fotografija, položaj hero sekcije, tipografija i zlatna paleta nisu
mijenjani. Pravila su lokalna za `zlatno_polje`.

## Provjera u pregledniku

Izolirana migrirana SQLite baza s jednim objavljenim postom i komentarom;
izvorni `db.sqlite3`, media i port 8000 nisu korišteni. Javni blog i post
detail pregledani su na 320, 390, 768 i 1440 px: **osam stanja**. Na svima su
post kartica i arhivski linkovi computed `rgb(255,248,228)`, document overflow
je 0 px, a detalj i blog zadržavaju raspored. Na 768/1440 px komentar ima istu
neprozirnu podlogu; na 320/390 px ostaje `rgb(255,246,223)`.

Kontrast je računat prema stvarnoj computed neprozirnoj podlozi, ne prema
jednom foto-cropu. Budući da je podloga neprozirna, omjer ostaje isti i nad
svijetlim i nad tamnim dijelom fotografije:

| Element | Omjer nakon popravka |
| --- | ---: |
| tijelo objave `#5f3d10` / `#fff8e4` | 9,16:1 |
| autor, akcije, arhiva, uputa i desktop komentar `#4b2d05` / `#fff8e4` | 11,81:1 |
| mobilni autor komentara / `#fff6df` | 9,67:1 |
| mobilni tekst komentara / `#fff6df` | 10,95:1 |

Na 390 px stvarni sigurni klik `Prethodni mjesec` vodio je na očekivani
`?year=2026&month=9`, a klik na dan s objavom na slugged detail rutu. Nisu
kliknuti like niti druga mutirajuća kontrola. Preglednik može automatski
zabilježiti posjet isključivo u izoliranoj bazi.

## Regresijska provjera i otvoreno

`blog/test_phase89d_zlatno_photo_contrast.py`: 2/2. `manage.py check`,
`makemigrations --check --dry-run`, `git diff --check` i puni Django skup
136/136 su zeleni. Test potvrđuje blog/detail render lokalnog ugovora te da
ga `neonski_grad` ne preuzima.

Naslov bloga iznad kartice i dalje stoji preko fotografije; ovaj patch ne
proglašava njegov foto-neovisan kontrast riješenim. Tablet/desktop post-action
touch mete i pojedine kalendarske mete ostaju zaseban P2.
