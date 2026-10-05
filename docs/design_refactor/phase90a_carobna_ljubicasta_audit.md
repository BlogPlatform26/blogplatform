# Phase 90a — audit Čarobne ljubičaste

## Opseg i metoda

Zbog preostalog petosatnog kredita ova je faza ograničena na jedan od šest
preostalih dizajna: `carobna_ljubicasta`. Izolirana migrirana SQLite baza
sadržavala je javni post i komentar. Stvarni preglednik provjerio je blog i
detalj na 320/390/768/1440 px (**osam stanja**). Izvorni `db.sqlite3`, media,
port 8000 i mutirajuće kontrole nisu korišteni.

Omjeri u tablici računati su iz computed boje teksta prema deklariranoj
osnovnoj boji tijela `#542b7e`. To su **referentni**, a ne foto-neovisni
omjeri: naslov i kartice imaju prozirnu podlogu preko stvarne fotografije
zamka/neba, koja se različito kadrira na 320 i 1440 px. Tekstualna sjena i
`backdrop-filter` nisu računati kao zajamčena kontrastna površina. Vizualno
su pregledani mobilni i desktop kadar.

| Meta | Computed boja | Referentni omjer |
| --- | --- | ---: |
| naslov bloga i podnaslov | `#fff5ff` | 9,76:1 |
| naslov posta | `#fff7ff` | 9,88:1 |
| tijelo i tekst komentara | `#f6eeff` | 9,19:1 |
| autor, akcijski linkovi i autor komentara | `#f6c7ff` | 7,18:1 |
| arhivski link | `rgba(247,236,255,.94)` | 8,23:1 |
| Bootstrap like tekst | `#0d6efd` | **2,31:1** |
| anonimna uputa | `rgba(33,37,41,.75)` | **1,38:1** |

`like` i uputa su potvrđeni P1 na tamnoj osnovi, a prozirna kartica ne daje
stabilan minimum preko svih zona fotografije. Naslov i drugi svijetli tekst
izgledaju čitljivo na pregledanim kadrovima, ali njihov foto-neovisan
kontrast **nije potvrđen**; ne označavati ga zatvorenim bez zasebne zaštite ili
pixel-mjerenja najnepovoljnijeg kadra.

## Geometrija i interakcije

Blog i detail imaju **0 px document overflowa** na sve četiri širine i nema
P0; pri tome `body` koristi `overflow-x:hidden`, pa to samo po sebi ne
isključuje lokalno prelijevanje. Na 768 px `.calendar-box` ima
`client/scroll` približno **150/184 px**, a grid **117/168 px**: lokalni P2
koji vizualno zbija dane. Na 320/390 px strelice i dan s postom su najmanje
44×44 odnosno 46×46 px, arhivski link 44 px, a like/comment/open-post akcije
44 px. Na 768/1440 px post akcije su samo 21–25 px visoke; na 1440 px
kalendarska strelica je 30 px, dan s postom oko 28×35 px, arhiva 34 px — P2
touch mete. Naslov bloga na 320 px prelazi u dva čitljiva retka bez odsijecanja.

Na 390 px stvarni sigurni klik `Prethodni mjesec` otvorio je
`?year=2026&month=9`, a klik na dan s postom slugged detalj. Like, komentar,
mark-read i drugi mutirajući kontroleri nisu kliknuti. Automatsko bilježenje
posjeta ostalo je u sintetičkoj bazi.

`manage.py check`, `makemigrations --check --dry-run`, `git diff --check` i
puni Django skup **140/140** zeleni su; audit nije mijenjao izvršni kod.

## Redoslijed sljedećih zahvata

1. Uska lokalna faza za anonimnu uputu i Bootstrap like: tinta/podloga koja
   daje >=4,5:1 s marginom na svijetlim i tamnim zonama, bez gubitka
   ljubičaste atmosfere.
2. Zasebno izmjeriti ili zaštititi naslov, post i komentare preko promjenjive
   fotografije; referentni omjeri nisu dokaz najgoreg foto-kadra.
3. Zasebno riješiti 768 px kalendarski lokalni overflow i shared tablet
   post-action mete. Ne skrivati geometriju dodatnim `overflow:hidden`.

`kraljevska_pozornica`, `dimni_akordi`, `sjene_ulice`, `mjesecev_ples` i
`asfaltni_plamen` još nisu auditirani u ovoj seriji, a završna matrica svih
37 dizajna ostaje otvorena.
