# Phase 89f — Zlatno polje: naslov neovisan o fotografiji

## Nalaz i lokalni popravak

Naslov bloga i podnaslov u `zlatno_polje` bili su tamna slova s tekstualnom
sjenom, ali na potpuno prozirnoj podlozi. U stvarnom pregledniku na blogu i
detalju objave, na 320/390/768/1440 px, oba su elementa imala computed
`rgba(0,0,0,0)`; stoga omjer iz prethodnog audita prema jednoj zlatnoj boji
nije jamčio kontrast na različitim svijetlim i tamnim cropovima pšenice/neba.

Lokalno pravilo daje samo tekstnim retcima neprozirnu pergamentnu podlogu
`#fff8e4`, s malim unutarnjim razmakom. Nisu prekrivene hero sekcija ni
panoramska fotografija, a zlatna paleta i postojeća tipografija ostaju.
Naslov prikazan preglednikom jest `#5a3605`, podnaslov `#4b2d05`; izračun
prema stvarnoj computed podlozi daje **10,08:1** za naslov i **11,81:1** za
podnaslov. Budući da je podloga neprozirna, isti omjeri vrijede na svijetloj
zoni neba i tamnijem/teksturiranom mobilnom izrezu pšenice.

## Preglednik i regresija

Izolirana migrirana sintetička SQLite baza s objavom i komentarom; izvorni
`db.sqlite3`, media i port 8000 nisu korišteni. Prije/poslije pregledani su
javni blog i detalj objave na 320, 390, 768 i 1440 px (**osam stanja**).
Nakon popravka podloge su computed `rgb(255,248,228)` u svih osam stanja;
document overflow nije pozitivan, a tekst je unutar viewporta. Vizualno su
provjereni mobilni izrez i desktop panoramski kadar. Na 390 px stvarni
sigurni klik `Prethodni mjesec` otvorio je očekivani `?year=2026&month=9`,
a klik na dan s objavom otvorio je slugged detalj. Like i druge mutirajuće
kontrole nisu kliknute; automatsko bilježenje posjeta ostalo je u sintetičkoj
bazi.

`blog/test_phase89f_zlatno_hero_contrast.py` provjerava blog/detail lokalni
ugovor i izolaciju od `neonski_grad`. Uski testovi 2/2, `manage.py check`,
`makemigrations --check --dry-run`, `git diff --check` i puni Django skup
140/140 zeleni su prije commita.

Tablet/desktop post-action touch mete i pojedine kalendarske mete ostaju
zaseban P2; preostalih šest dizajna i završna matrica svih 37 još nisu
zatvoreni.
