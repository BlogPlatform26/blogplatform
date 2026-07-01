# Mapa dizajnova za refaktor

Izrađeno: 2026-07-01 09:00:59

## Sažetak

- Ukupno dizajnova: **42**
- Koriste zajednički layout `blog/layouts/blog_design_base.html`: **31**
- Imaju posebnu strukturu preko `blog/base.html` ili drugo: **11**
- Imaju vlastitu petlju za postove: **11**

## Layout grupe

- `magazine`: 1
- `right_boxes`: 3
- `simple`: 4
- `single_right_sidebar`: 9
- `standard`: 24
- `studio`: 1

## Rizik refaktora

- nizak: 11
- srednji: 20
- visok: 11

## Tablica dizajnova

| Dizajn | Extends | Layout | Boxevi | Zajednički postovi | Vlastita petlja | Rizik |
|---|---|---|---|---:|---:|---|
| asfaltni_plamen | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| carobna_ljubicasta | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| classic | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | NE | NE | nizak |
| classic_right | `blog/layouts/blog_design_base.html` | `right_boxes` | svi boxevi desno / wide prikaz | NE | NE | nizak |
| dark | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | NE | NE | nizak |
| dark_right | `blog/layouts/blog_design_base.html` | `right_boxes` | svi boxevi desno / wide prikaz | NE | NE | nizak |
| default | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | NE | NE | nizak |
| default_right | `blog/layouts/blog_design_base.html` | `right_boxes` | svi boxevi desno / wide prikaz | NE | NE | nizak |
| dimni_akordi | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| iznad_oblaka | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| jedro_u_suton | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| kraljevska_pozornica | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| litica_noci | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | NE | NE | nizak |
| magazin | `blog/base.html` | `magazine` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| misticno_jezero | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| mjesecev_ples | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| morski_prijelaz | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| nebeska_klasika | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| nebeski_mir | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| nebesko_polje | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| neonski_grad | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| planine_u_magli | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| podvodna_tisina | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| polarna_svjetlost | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| polje_lavande | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| ponocna_elegancija | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| ruzicasti_vrt | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| simple | `blog/layouts/blog_design_base.html` | `simple` | jednostavni raspored, ovisi o simple varijanti | NE | NE | nizak |
| simple_image | `blog/layouts/blog_design_base.html` | `simple` | jednostavni raspored, ovisi o simple varijanti | NE | NE | nizak |
| simple_pattern | `blog/layouts/blog_design_base.html` | `simple` | jednostavni raspored, ovisi o simple varijanti | NE | NE | nizak |
| simple_retro | `blog/layouts/blog_design_base.html` | `simple` | jednostavni raspored, ovisi o simple varijanti | NE | NE | nizak |
| sjene_ulice | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| stara_aleja | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| staza_prema_vrhovima | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| studio | `blog/base.html` | `studio` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| sumska_svjetlost | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| svemirski_horizont | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| vecer_uz_jezero | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| vecer_zaljubljenih | `blog/base.html` | `single_right_sidebar` | lijevi i desni boxevi spojeni u jedan poseban sidebar | NE | DA | visok |
| vodopad_u_magli | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| zlatni_horizont | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |
| zlatno_polje | `blog/layouts/blog_design_base.html` | `standard` | zajednički layout: lijevi sidebar + sadržaj + desni sidebar | DA | NE | srednji |

## Dizajni koje treba prvo dirati oprezno

- `jedro_u_suton` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `magazin` — layout `magazine`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `misticno_jezero` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `nebeska_klasika` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `ponocna_elegancija` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `ruzicasti_vrt` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `stara_aleja` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `staza_prema_vrhovima` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `studio` — layout `studio`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `vecer_uz_jezero` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar
- `vecer_zaljubljenih` — layout `single_right_sidebar`, lijevi i desni boxevi spojeni u jedan poseban sidebar

## Preporučeni redoslijed

1. Prvo srediti zajedničke komponente: header, postovi, boxevi, sidebar.
2. Ne dirati posebne dizajne dok obični i right layout ne rade stabilno.
3. Posebne dizajne prebacivati jedan po jedan, uz usporedbu izgleda prije/poslije.
4. Tek nakon toga dodati rubove/bordere i dodatne opcije dizajna.
