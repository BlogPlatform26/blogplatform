# DESIGN REFACTOR — STATUS

Zadnje ažuriranje: 2026-07-01

## Glavni cilj

Srediti sustav dizajnova tako da:
- dizajni ne moraju svi izgledati isto
- ali svi koriste što više zajedničkih komponenti
- korisničke postavke imaju prednost nad zadanim stilom dizajna
- nova opcija ne mora se popravljati posebno u svakom dizajnu
- posebni dizajni se ne diraju napamet

Drugim riječima:

DIZAJN = zadani izgled  
LAYOUT = raspored elemenata  
KORISNIČKE POSTAVKE = ono što korisnik promijeni i što mora imati prednost  

---

## Trenutno stanje dizajnova

Ukupno dizajnova: 42

### Zajednički layout

31 dizajn koristi:

blog/layouts/blog_design_base.html

To su lakši dizajni za održavanje jer već koriste zajedničku strukturu.

### Posebni dizajni

11 dizajnova ima posebnu strukturu i vlastiti HTML:

- jedro_u_suton
- magazin
- misticno_jezero
- nebeska_klasika
- ponocna_elegancija
- ruzicasti_vrt
- stara_aleja
- staza_prema_vrhovima
- studio
- vecer_uz_jezero
- vecer_zaljubljenih

Ove dizajne treba raditi oprezno, jedan po jedan.

---

## Što je gotovo

### Faza 1 — mapa dizajnova

Gotovo.

Napravljeno:
- docs/design_refactor/design_map.md
- docs/design_refactor/design_map.json

Cilj:
- vidjeti koliko ima dizajnova
- vidjeti koji koriste zajednički layout
- vidjeti koji su posebni/rizični

---

### Faza 2 — zajednički JavaScript za interakcije

Gotovo.

Napravljeno:
- blog/templates/blog/components/blog_interaction_scripts.html

Sređeno:
- klik na komentare
- skrolanje do komentara
- osnovni JS vezan za ankete/rezultate

Commit:
- Refactor shared blog interaction scripts

---

### Faza 3 — audit prikaza postova

Gotovo.

Napravljeno:
- docs/design_refactor/phase3_posts_audit.md
- docs/design_refactor/phase3_posts_audit.json

Cilj:
- vidjeti koji dizajni koriste zajednički prikaz postova
- vidjeti koji dizajni imaju vlastitu petlju postova

---

### Faza 4 — zajednički prikaz posta i paginacije

Gotovo.

Napravljeno:
- blog/templates/blog/components/post_card.html
- blog/templates/blog/components/blog_pagination.html
- pojednostavljen blog/templates/blog/components/blog_posts.html

Sređeno:
- zajednički prikaz jednog posta za dizajnove koji koriste zajednički layout
- zajednički prikaz paginacije

Nisu dirani:
- posebni dizajni
- banneri
- boxevi
- CSS raspored

Commit:
- Refactor shared post rendering components

---

### Faza 5 — audit boxeva i sidebara

Gotovo.

Napravljeno:
- docs/design_refactor/phase5_boxes_sidebar_audit.md
- docs/design_refactor/phase5_boxes_sidebar_audit.json

Cilj:
- vidjeti gdje se prikazuju lijevi i desni boxevi
- vidjeti koji dizajni spajaju boxeve u jedan sidebar
- ne dirati posebne dizajnove napamet

---

### Faza 6 — zajednička komponenta za jedan box

Gotovo.

Napravljeno:
- blog/templates/blog/components/blog_box.html
- pojednostavljen blog_left_sidebar.html
- pojednostavljen blog_right_sidebar.html

Sređeno:
- jedan zajednički prikaz blog boxa u zajedničkom layoutu

Nisu dirani:
- posebni dizajni
- banner
- kalendar
- arhiva
- raspored boxeva

Commit:
- Refactor shared blog box component

---

## Što smo pokušali, ali nismo zadržali

### Faza 7 — kalendar i arhiva

Pokušano, ali vraćeno.

Razlog:
- arhiva se zalijepila uz kalendar
- razmak nije ostao isti kao prije
- to je promijenilo izgled, a cilj refaktora je da izgled ostane isti

Zaključak:
- kalendar i arhivu za sada ne dirati
- prvo treba bolje srediti zajednički sidebar wrapper
- tek onda izdvajati kalendar/arhivu

---

### Faza 8 — jedro_u_suton banner

Pokušano, ali nije potvrđeno kao dobro.

Problem:
- banner u dizajnu jedro_u_suton se ne prikazuje kako se očekuje

Status:
- ne commitati dok nije vizualno potvrđeno
- ako promjena izgleda loše, vratiti:
  blog/templates/blog/designs/jedro_u_suton.html

Napomena:
- jedro_u_suton je posebni dizajn
- ne treba ga popravljati kao obične dizajnove
- treba usporediti kako banner treba izgledati u tom dizajnu

---

## Glavni otvoreni problemi

### 1. Korisničke postavke ne vrijede svugdje jednako

Problem:
- neki dizajni imaju vlastiti CSS/HTML
- zbog toga mogu pregaziti ono što korisnik postavi u postavkama

Cilj:
- korisnikove postavke uvijek moraju imati prednost

Primjeri:
- boja naslova
- pozadina
- boja posta
- boja boxa
- font
- banner pozicija
- kasnije rubovi/borderi

---

### 2. Posebni dizajni imaju vlastitu strukturu

Posebni dizajni:
- jedro_u_suton
- magazin
- misticno_jezero
- nebeska_klasika
- ponocna_elegancija
- ruzicasti_vrt
- stara_aleja
- staza_prema_vrhovima
- studio
- vecer_uz_jezero
- vecer_zaljubljenih

Oni imaju:
- vlastitu petlju postova
- vlastiti sidebar
- vlastiti banner
- vlastite klase
- često spojene lijeve i desne boxeve u jedan sidebar

Zato ih treba raditi jedan po jedan.

---

### 3. Simple i magazin slike

Za kasnije.

Želja:
- omogućiti mijenjanje slike u simple dizajnima
- omogućiti mijenjanje slike u magazin dizajnu

Ne raditi prije nego se sredi osnovni sustav dizajnova.

---

### 4. Rubovi / borderi

Za kasnije.

Ne dodavati dok se ne sredi:
- zajednička struktura dizajnova
- pravilo da korisničke postavke pobjeđuju dizajn
- posebni dizajni barem djelomično

---

## Preporučeni daljnji redoslijed

### Korak 1

Ne dirati više kalendar/arhivu dok ne odlučimo kako se čuva isti razmak.

### Korak 2

Srediti pravilo korisničkih postavki.

Cilj:
- napraviti centralno mjesto gdje se primjenjuju korisničke postavke
- dizajn daje zadani stil
- korisnikova izmjena uvijek ima prednost

### Korak 3

Posebne dizajne raditi jedan po jedan.

Prvi:
- jedro_u_suton

Kod njega prvo riješiti:
- banner
- poziciju bannera
- širinu/visinu bannera
- da se ne pokvari layout

### Korak 4

Nakon jedro_u_suton, raditi sličnu grupu:

- misticno_jezero
- nebeska_klasika
- ponocna_elegancija
- ruzicasti_vrt
- stara_aleja
- staza_prema_vrhovima
- vecer_uz_jezero

### Korak 5

Magazin i studio ostaviti kasnije.

Razlog:
- imaju poseban prikaz
- imaju slike/hero dio
- veći rizik da se pokvari izgled

---

## Pravilo za daljnji rad

Ne raditi velike promjene odjednom.

Svaka faza mora:
- imati mali cilj
- ne dirati bazu ako nije potrebno
- ne mijenjati izgled ako to nije cilj
- imati test na barem 2-3 dizajna
- imati commit tek kad vizualno izgleda dobro

---

## Test nakon svake faze

Provjeriti:

- otvara se blog
- vide se postovi
- vide se boxevi
- banner nije pokvaren
- komentari rade
- klik na Komentari radi
- anketa radi ako postoji
- arhiva i kalendar nisu promijenili razmak
- korisničke postavke se i dalje primjenjuju

---

## Trenutna sigurna zadnja faza

Zadnja sigurna faza:

FAZA 6 — zajednička komponenta za jedan box

Sve nakon toga treba raditi oprezno i po mogućnosti prvo bez commita.
