# Phase 14 — audit navbar CSS-a u dizajnima

Izrađeno: 2026-07-03 11:02:07

## Cilj

Provjeriti diraju li pojedini blog dizajni globalni navbar. Navbar, tražilica, logo, obavijesti i globalni dropdownovi trebaju biti dio platforme, ne dio pojedinog dizajna.

## Sažetak

- Template dizajna u kodu: **42**
- Dizajni s bilo kakvim navbar hitovima: **31**
- Dizajni s rizičnim navbar hitovima: **31**

## Grupe

| Grupa | Ukupno | S navbar hitovima |
|---|---:|---:|
| `posebni` | 9 | 9 |
| `posebni_hero` | 2 | 2 |
| `right_sidebar` | 3 | 0 |
| `simple` | 4 | 0 |
| `zajednicki_layout` | 24 | 20 |

## Dizajni koji možda diraju navbar

| Dizajn | Grupa | Vidljivost | Navbar hitovi | Rizični hitovi |
|---|---|---|---:|---:|
| `asfaltni_plamen` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `carobna_ljubicasta` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `dimni_akordi` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `iznad_oblaka` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `jedro_u_suton` | `posebni` | `vjerojatno_ponuden` | 2 | 2 |
| `kraljevska_pozornica` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `magazin` | `posebni_hero` | `vjerojatno_ponuden` | 2 | 2 |
| `misticno_jezero` | `posebni` | `vjerojatno_ponuden` | 2 | 2 |
| `mjesecev_ples` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `morski_prijelaz` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `nebeska_klasika` | `posebni` | `vjerojatno_ponuden` | 2 | 2 |
| `nebeski_mir` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `nebesko_polje` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `neonski_grad` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `planine_u_magli` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `podvodna_tisina` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `polarna_svjetlost` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `polje_lavande` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `ponocna_elegancija` | `posebni` | `vjerojatno_ponuden` | 2 | 2 |
| `ruzicasti_vrt` | `posebni` | `vjerojatno_ponuden` | 2 | 2 |
| `sjene_ulice` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `stara_aleja` | `posebni` | `vjerojatno_ponuden` | 2 | 2 |
| `staza_prema_vrhovima` | `posebni` | `vjerojatno_ponuden` | 2 | 2 |
| `studio` | `posebni_hero` | `samo_template_ili_nejasno` | 2 | 2 |
| `sumska_svjetlost` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `svemirski_horizont` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `vecer_uz_jezero` | `posebni` | `samo_template_ili_nejasno` | 2 | 2 |
| `vecer_zaljubljenih` | `posebni` | `samo_template_ili_nejasno` | 2 | 2 |
| `vodopad_u_magli` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `zlatni_horizont` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |
| `zlatno_polje` | `zajednicki_layout` | `vjerojatno_ponuden` | 2 | 2 |

## Globalni navbar CSS

Ovo su globalne datoteke u kojima navbar smije postojati. Njih ne treba automatski smatrati problemom.

- `blog\templates\blog\base.html` — navbar hitovi: **11**, rizični hitovi: **4**
- `blog\templates\blog\components\blog_design_styles.html` — navbar hitovi: **6**, rizični hitovi: **6**

## Detalji rizičnih dizajnova

### `asfaltni_plamen`

- Datoteka: `blog\templates\blog\designs\asfaltni_plamen.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 53:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```

### `carobna_ljubicasta`

- Datoteka: `blog\templates\blog\designs\carobna_ljubicasta.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 84:
```txt
0081:     filter: blur(0.15px);
0082: }
0083: 
0084: nav.navbar {
0085:     position: relative;
0086:     z-index: 4000 !important;
0087: }
```
Linija 89:
```txt
0086:     z-index: 4000 !important;
0087: }
0088: 
0089: nav.navbar .dropdown-menu {
0090:     z-index: 4100 !important;
0091: }
0092: 
```

### `dimni_akordi`

- Datoteka: `blog\templates\blog\designs\dimni_akordi.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 53:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```

### `iznad_oblaka`

- Datoteka: `blog\templates\blog\designs\iznad_oblaka.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```

### `jedro_u_suton`

- Datoteka: `blog\templates\blog\designs\jedro_u_suton.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 31:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(38, 23, 17, 0.78) !important;
```
Linija 39:
```txt
0036:     border-bottom: 1px solid rgba(255, 228, 203, 0.10);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```

### `kraljevska_pozornica`

- Datoteka: `blog\templates\blog\designs\kraljevska_pozornica.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 79:
```txt
0076:     background-repeat: no-repeat;
0077: }
0078: 
0079: nav.navbar {
0080:     position: relative;
0081:     z-index: 4000 !important;
0082: }
```
Linija 84:
```txt
0081:     z-index: 4000 !important;
0082: }
0083: 
0084: nav.navbar .dropdown-menu {
0085:     z-index: 4100 !important;
0086: }
0087: 
```

### `magazin`

- Datoteka: `blog\templates\blog\designs\magazin.html`
- Grupa: `posebni_hero`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 352:
```txt
0349:     z-index: 9999;
0350: }
0351: 
0352: nav.navbar {
0353:     position: relative;
0354:     z-index: 5000 !important;
0355: }
```
Linija 357:
```txt
0354:     z-index: 5000 !important;
0355: }
0356: 
0357: nav.navbar .dropdown-menu {
0358:     z-index: 5100 !important;
0359: }
0360: 
```

### `misticno_jezero`

- Datoteka: `blog\templates\blog\designs\misticno_jezero.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 31:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(26, 10, 36, 0.76) !important;
```
Linija 39:
```txt
0036:     backdrop-filter: blur(8px);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```

### `mjesecev_ples`

- Datoteka: `blog\templates\blog\designs\mjesecev_ples.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 53:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```

### `morski_prijelaz`

- Datoteka: `blog\templates\blog\designs\morski_prijelaz.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 41:
```txt
0038:         background-size: cover, cover;
0039:     }
0040: 
0041:     nav.navbar {
0042:         position: relative;
0043:         z-index: 4000 !important;
0044:     }
```
Linija 46:
```txt
0043:         z-index: 4000 !important;
0044:     }
0045: 
0046:     nav.navbar .dropdown-menu {
0047:         z-index: 4100 !important;
0048:     }
0049: 
```

### `nebeska_klasika`

- Datoteka: `blog\templates\blog\designs\nebeska_klasika.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 29:
```txt
0026:     display: none;
0027: }
0028: 
0029: nav.navbar {
0030:     position: relative;
0031:     z-index: 4000 !important;
0032:     background: rgba(42, 45, 51, 0.84) !important;
```
Linija 37:
```txt
0034:     border-bottom: 1px solid rgba(255,255,255,0.08);
0035: }
0036: 
0037: nav.navbar .dropdown-menu {
0038:     z-index: 4100 !important;
0039: }
0040: 
```

### `nebeski_mir`

- Datoteka: `blog\templates\blog\designs\nebeski_mir.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 44:
```txt
0041:     background-size: 100% 100%, cover;
0042: }
0043: 
0044: nav.navbar {
0045:     position: relative;
0046:     z-index: 4000 !important;
0047:     background: rgba(0, 0, 0, 0.88) !important;
```
Linija 51:
```txt
0048:     backdrop-filter: blur(8px);
0049: }
0050: 
0051: nav.navbar .dropdown-menu {
0052:     z-index: 4100 !important;
0053: }
0054: 
```

### `nebesko_polje`

- Datoteka: `blog\templates\blog\designs\nebesko_polje.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 60:
```txt
0057:     background-size: cover;
0058: }
0059: 
0060: nav.navbar {
0061:     position: relative;
0062:     z-index: 5000 !important;
0063: }
```
Linija 65:
```txt
0062:     z-index: 5000 !important;
0063: }
0064: 
0065: nav.navbar .dropdown-menu {
0066:     z-index: 5100 !important;
0067: }
0068: 
```

### `neonski_grad`

- Datoteka: `blog\templates\blog\designs\neonski_grad.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 44:
```txt
0041:     background-size: 100% 100%, 100% 100%, 100% auto;
0042: }
0043: 
0044: nav.navbar {
0045:     position: relative;
0046:     z-index: 4000 !important;
0047: }
```
Linija 49:
```txt
0046:     z-index: 4000 !important;
0047: }
0048: 
0049: nav.navbar .dropdown-menu {
0050:     z-index: 4100 !important;
0051: }
0052: 
```

### `planine_u_magli`

- Datoteka: `blog\templates\blog\designs\planine_u_magli.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, cover;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046:     background: rgba(23, 28, 36, 0.88) !important;
```
Linija 50:
```txt
0047:     backdrop-filter: blur(8px);
0048: }
0049: 
0050: nav.navbar .dropdown-menu {
0051:     z-index: 4100 !important;
0052: }
0053: 
```

### `podvodna_tisina`

- Datoteka: `blog\templates\blog\designs\podvodna_tisina.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:         background-size: 100% 100%, 100% auto;
0041:     }
0042: 
0043:     nav.navbar {
0044:         position: relative;
0045:         z-index: 4000 !important;
0046:     }
```
Linija 48:
```txt
0045:         z-index: 4000 !important;
0046:     }
0047: 
0048:     nav.navbar .dropdown-menu {
0049:         z-index: 4100 !important;
0050:     }
0051: 
```

### `polarna_svjetlost`

- Datoteka: `blog\templates\blog\designs\polarna_svjetlost.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```

### `polje_lavande`

- Datoteka: `blog\templates\blog\designs\polje_lavande.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```

### `ponocna_elegancija`

- Datoteka: `blog\templates\blog\designs\ponocna_elegancija.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 31:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(9, 14, 25, 0.84) !important;
```
Linija 39:
```txt
0036:     border-bottom: 1px solid rgba(255,255,255,0.08);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```

### `ruzicasti_vrt`

- Datoteka: `blog\templates\blog\designs\ruzicasti_vrt.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 31:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(64, 42, 49, 0.24) !important;
```
Linija 39:
```txt
0036:     border-bottom: 1px solid rgba(255,255,255,0.14);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```

### `sjene_ulice`

- Datoteka: `blog\templates\blog\designs\sjene_ulice.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 53:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```

### `stara_aleja`

- Datoteka: `blog\templates\blog\designs\stara_aleja.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 31:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(44, 30, 20, 0.82) !important;
```
Linija 39:
```txt
0036:     border-bottom: 1px solid rgba(255,255,255,0.08);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```

### `staza_prema_vrhovima`

- Datoteka: `blog\templates\blog\designs\staza_prema_vrhovima.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 31:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(28, 20, 13, 0.82) !important;
```
Linija 39:
```txt
0036:     backdrop-filter: blur(6px);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```

### `studio`

- Datoteka: `blog\templates\blog\designs\studio.html`
- Grupa: `posebni_hero`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 346:
```txt
0343:     z-index: 9999;
0344: }
0345: 
0346: nav.navbar {
0347:     position: relative;
0348:     z-index: 5000 !important;
0349: }
```
Linija 351:
```txt
0348:     z-index: 5000 !important;
0349: }
0350: 
0351: nav.navbar .dropdown-menu {
0352:     z-index: 5100 !important;
0353: }
0354: 
```

### `sumska_svjetlost`

- Datoteka: `blog\templates\blog\designs\sumska_svjetlost.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```

### `svemirski_horizont`

- Datoteka: `blog\templates\blog\designs\svemirski_horizont.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```

### `vecer_uz_jezero`

- Datoteka: `blog\templates\blog\designs\vecer_uz_jezero.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 31:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(30, 13, 12, 0.82) !important;
```
Linija 38:
```txt
0035:     border-bottom: 1px solid rgba(255, 228, 204, 0.10);
0036: }
0037: 
0038: nav.navbar .dropdown-menu {
0039:     z-index: 4100 !important;
0040: }
0041: 
```

### `vecer_zaljubljenih`

- Datoteka: `blog\templates\blog\designs\vecer_zaljubljenih.html`
- Grupa: `posebni`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 42:
```txt
0039:     display: none;
0040: }
0041: 
0042: nav.navbar {
0043:     position: relative;
0044:     z-index: 4000 !important;
0045:     background: rgba(32, 7, 6, 0.42) !important;
```
Linija 50:
```txt
0047:     border-bottom: 1px solid rgba(255, 226, 206, 0.10);
0048: }
0049: 
0050: nav.navbar .dropdown-menu {
0051:     z-index: 4100 !important;
0052: }
0053: 
```

### `vodopad_u_magli`

- Datoteka: `blog\templates\blog\designs\vodopad_u_magli.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```

### `zlatni_horizont`

- Datoteka: `blog\templates\blog\designs\zlatni_horizont.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 43:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```

### `zlatno_polje`

- Datoteka: `blog\templates\blog\designs\zlatno_polje.html`
- Grupa: `zajednicki_layout`
- Navbar hitovi: **2**
- Rizični hitovi: **2**

Linija 46:
```txt
0043:     background-size: 100% 100%, 100% auto;
0044: }
0045: 
0046: nav.navbar {
0047:     position: relative;
0048:     z-index: 4000 !important;
0049: }
```
Linija 51:
```txt
0048:     z-index: 4000 !important;
0049: }
0050: 
0051: nav.navbar .dropdown-menu {
0052:     z-index: 4100 !important;
0053: }
0054: 
```

## Preporuka

1. Spremiti ovaj audit u git.
2. Ako neki dizajn direktno stilizira `.navbar`, `.navbar-brand`, tražilicu ili badge obavijesti, taj CSS treba maknuti iz dizajna ili ograničiti na blog layout.
3. Navbar treba ostati globalan i isti na svim dizajnima.
4. Ne mijenjati dizajne dok se ne potvrdi točan popis rizičnih selektora.
