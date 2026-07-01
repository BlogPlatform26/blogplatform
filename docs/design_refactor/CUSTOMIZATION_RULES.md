cd C:\Users\mario\blogplatform

@'
# CUSTOMIZATION RULES

Zadnje ažuriranje: 2026-07-01

## Cilj

Cilj je da svi dizajni mogu imati svoj izgled, ali da korisnikove postavke uvijek imaju prednost nad zadanim stilom dizajna.

Dizajn smije dati:
- zadane boje
- zadane fontove
- zadane pozadine
- zadani raspored
- zadani izgled bannera, postova i boxeva

Korisnikova postavka mora moći pregaziti:
- boju
- font
- veličinu
- pozadinu
- prikaz bannera
- poziciju bannera
- izgled postova
- izgled boxeva

---

## Glavno pravilo

DIZAJN = zadani izgled  
KORISNIČKE POSTAVKE = konačna odluka korisnika  

Ako dizajn kaže jedno, a korisnik u postavkama odabere drugo, korisnikova postavka mora pobijediti.

---

## Postavke koje moraju raditi svugdje

### 1. Naziv bloga

Mora podržavati:

- boju naziva bloga
- font naziva bloga
- veličinu naziva bloga

Primjeri:
- `blog_title_color`
- `blog_title_font_stack`
- `blog_title_size`

---

### 2. Opis bloga / tagline

Mora podržavati:

- prikaz opisa bloga
- osnovnu boju teksta
- osnovni font ako je moguće

Opis bloga ne smije nestati samo zato što je korisnik odabrao poseban dizajn.

---

### 3. Naslov posta

Mora podržavati:

- boju naslova posta
- font naslova posta
- veličinu naslova posta

Primjeri:
- `post_title_color`
- `post_title_font_stack`
- `post_title_size`

---

### 4. Tekst posta

Mora podržavati:

- boju teksta
- font teksta
- osnovnu čitljivost

Primjeri:
- `body_text_color`
- `body_font_stack`

Dizajn ne smije napraviti da tekst bude nečitljiv ako korisnik promijeni boje.

---

### 5. Pozadina sadržaja

Mora podržavati:

- boju pozadine glavnog sadržaja
- eventualno prozirnost ako postoji
- obrub sadržaja ako postoji

Primjeri:
- `content_background_color`
- `content_border_color`

---

### 6. Boxevi

Box mora podržavati:

- boju pozadine boxa
- boju naslova boxa
- font naslova boxa
- veličinu naslova boxa
- boju obruba boxa ako postoji

Primjeri:
- `box_background_color`
- `box_title_color`
- `box_title_font_stack`
- `box_title_size`
- `box_border_color`

---

### 7. Datum posta

Mora podržavati:

- stil datuma
- efekt datuma
- boju datuma
- veličinu datuma ako postoji

Primjeri:
- `post_date_style`
- `post_date_effect`
- `post_date_color`
- `post_date_size`

---

### 8. Banner

Banner mora podržavati:

- prikaz bannera
- skrivanje bannera ako korisnik tako odabere
- veličinu bannera
- poziciju/fokus bannera
- poravnanje slike ako postoji

Primjeri:
- `blog_banner`
- `blog_banner_display`
- `blog_banner_size`
- `blog_banner_position`
- `blog_banner_focus`

Posebni dizajni ne smiju imati banner riješen potpuno drugačije ako zbog toga korisnikove postavke ne rade.

---

### 9. Pozadina bloga

Mora podržavati:

- boju pozadine
- gradijent ako postoji
- sliku pozadine ako postoji
- zadanu sliku dizajna ako korisnik nije ništa odabrao

Primjeri:
- `outer_background_color_1`
- `outer_background_asset`
- `simple_background_image`

---

### 10. Analitika, arhiva i kalendar

Mora ostati stabilno:

- gdje se prikazuje analitika
- gdje se prikazuje arhiva
- gdje se prikazuje kalendar
- razmak između sidebar elemenata

Ne izdvajati kalendar i arhivu dok nismo sigurni da se ne mijenja razmak.

---

## Posebni dizajni

Posebni dizajni imaju veći rizik jer imaju vlastiti HTML i CSS.

Posebni single-sidebar dizajni:

- jedro_u_suton
- misticno_jezero
- nebeska_klasika
- ponocna_elegancija
- ruzicasti_vrt
- stara_aleja
- staza_prema_vrhovima
- vecer_uz_jezero
- vecer_zaljubljenih

Posebni hero dizajni:

- magazin
- studio

Ove dizajne treba raditi jedan po jedan.

---

## Zajednički layout

Dizajni koji koriste zajednički layout trebaju biti prvi za sređivanje korisničkih postavki, jer ih je najviše.

Cilj:
- centralno primijeniti CSS varijable
- ne popravljati svaki dizajn ručno
- ne mijenjati izgled ako korisnik nije ništa promijenio

---

## CSS varijable

Poželjno je da korisničke postavke idu kroz CSS varijable.

Primjer:

```css
--blog-title-color
--post-title-color
--body-text-color
--content-background-color
--box-background-color
--box-title-color
--post-date-color