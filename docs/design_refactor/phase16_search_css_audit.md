# Phase 16 — audit CSS-a koji može mijenjati navbar tražilicu

Izrađeno: 2026-07-03 11:48:42

## Cilj

Pronaći CSS u dizajnima koji može mijenjati globalnu tražilicu u navbaru. Tražilica, logo, obavijesti i gumbi u navbaru trebaju biti isti kao na naslovnoj stranici.

## Sažetak

- Template dizajna u kodu: **42**
- Dizajni s hitovima vezanim za search/form/navbar: **31**
- Dizajni s rizičnim hitovima: **31**
- Ukupno hitova: **331**
- Ukupno rizičnih hitova: **331**

## Što se smatra rizičnim

Rizično je ako dizajn ima selektore poput:

- `nav.navbar`
- `.navbar`
- `.form-control`
- `.input-group`
- `input`
- `button`
- `.btn`
- `badge`, `notif`, `notification`

Takvi selektori mogu slučajno promijeniti izgled tražilice, gumba ili obavijesti u navbaru.

## Pregled dizajnova s hitovima

| Dizajn | Grupa | Hitovi | Rizični hitovi |
|---|---|---:|---:|
| `asfaltni_plamen` | `zajednicki_layout` | 10 | 10 |
| `carobna_ljubicasta` | `zajednicki_layout` | 13 | 13 |
| `dimni_akordi` | `zajednicki_layout` | 10 | 10 |
| `iznad_oblaka` | `zajednicki_layout` | 13 | 13 |
| `jedro_u_suton` | `posebni` | 13 | 13 |
| `kraljevska_pozornica` | `zajednicki_layout` | 5 | 5 |
| `magazin` | `posebni_hero` | 9 | 9 |
| `misticno_jezero` | `posebni` | 12 | 12 |
| `mjesecev_ples` | `zajednicki_layout` | 10 | 10 |
| `morski_prijelaz` | `zajednicki_layout` | 7 | 7 |
| `nebeska_klasika` | `posebni` | 9 | 9 |
| `nebeski_mir` | `zajednicki_layout` | 6 | 6 |
| `nebesko_polje` | `zajednicki_layout` | 9 | 9 |
| `neonski_grad` | `zajednicki_layout` | 16 | 16 |
| `planine_u_magli` | `zajednicki_layout` | 6 | 6 |
| `podvodna_tisina` | `zajednicki_layout` | 7 | 7 |
| `polarna_svjetlost` | `zajednicki_layout` | 13 | 13 |
| `polje_lavande` | `zajednicki_layout` | 13 | 13 |
| `ponocna_elegancija` | `posebni` | 12 | 12 |
| `ruzicasti_vrt` | `posebni` | 12 | 12 |
| `sjene_ulice` | `zajednicki_layout` | 10 | 10 |
| `stara_aleja` | `posebni` | 13 | 13 |
| `staza_prema_vrhovima` | `posebni` | 12 | 12 |
| `studio` | `posebni_hero` | 9 | 9 |
| `sumska_svjetlost` | `zajednicki_layout` | 13 | 13 |
| `svemirski_horizont` | `zajednicki_layout` | 13 | 13 |
| `vecer_uz_jezero` | `posebni` | 12 | 12 |
| `vecer_zaljubljenih` | `posebni` | 12 | 12 |
| `vodopad_u_magli` | `zajednicki_layout` | 6 | 6 |
| `zlatni_horizont` | `zajednicki_layout` | 13 | 13 |
| `zlatno_polje` | `zajednicki_layout` | 13 | 13 |

## Detalji

### `asfaltni_plamen`

- Datoteka: `blog\templates\blog\designs\asfaltni_plamen.html`
- Grupa: `zajednicki_layout`
- Hitovi: **10**
- Rizični hitovi: **10**

Linija 53 — `navbar` — dira navbar:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54 — `navbar` — dira navbar:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```
Linija 249 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0246:     color: #ffe1bd;
0247: }
0248: 
0249: .btn-outline-light {
0250:     border-color: rgba(239, 199, 146, 0.38) !important;
0251:     color: #ffe1bd !important;
0252: }
```
Linija 254 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0251:     color: #ffe1bd !important;
0252: }
0253: 
0254: .btn-outline-light:hover {
0255:     background: rgba(239, 199, 146, 0.12) !important;
0256:     color: #fff6ec !important;
0257: }
```
Linija 342 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0339:     padding: 10px 44px 10px 12px;
0340: }
0341: 
0342: textarea.form-control,
0343: input.form-control,
0344: select.form-select {
0345:     background: rgba(33, 23, 18, 0.64) !important;
```
Linija 343 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0340: }
0341: 
0342: textarea.form-control,
0343: input.form-control,
0344: select.form-select {
0345:     background: rgba(33, 23, 18, 0.64) !important;
0346:     color: #f6e8da !important;
```
Linija 343 — `input_selector` — genericki input selector:
```txt
0340: }
0341: 
0342: textarea.form-control,
0343: input.form-control,
0344: select.form-select {
0345:     background: rgba(33, 23, 18, 0.64) !important;
0346:     color: #f6e8da !important;
```
Linija 350 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0347:     border-color: rgba(221, 160, 101, 0.18) !important;
0348: }
0349: 
0350: textarea.form-control::placeholder,
0351: input.form-control::placeholder {
0352:     color: rgba(246, 232, 218, 0.56) !important;
0353: }
```
Linija 351 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0348: }
0349: 
0350: textarea.form-control::placeholder,
0351: input.form-control::placeholder {
0352:     color: rgba(246, 232, 218, 0.56) !important;
0353: }
0354: 
```
Linija 351 — `input_selector` — genericki input selector:
```txt
0348: }
0349: 
0350: textarea.form-control::placeholder,
0351: input.form-control::placeholder {
0352:     color: rgba(246, 232, 218, 0.56) !important;
0353: }
0354: 
```

### `carobna_ljubicasta`

- Datoteka: `blog\templates\blog\designs\carobna_ljubicasta.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 84 — `navbar` — dira navbar:
```txt
0081:     filter: blur(0.15px);
0082: }
0083: 
0084: nav.navbar {
0085:     position: relative;
0086:     z-index: 4000 !important;
0087: }
```
Linija 89 — `navbar` — dira navbar:
```txt
0086:     z-index: 4000 !important;
0087: }
0088: 
0089: nav.navbar .dropdown-menu {
0090:     z-index: 4100 !important;
0091: }
0092: 
```
Linija 617 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0614:     color: #f4eaff;
0615: }
0616: 
0617: textarea.form-control,
0618: input.form-control,
0619: select.form-select {
0620:     background: rgba(255, 255, 255, 0.10) !important;
```
Linija 618 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0615: }
0616: 
0617: textarea.form-control,
0618: input.form-control,
0619: select.form-select {
0620:     background: rgba(255, 255, 255, 0.10) !important;
0621:     color: #fff3ff !important;
```
Linija 618 — `input_selector` — genericki input selector:
```txt
0615: }
0616: 
0617: textarea.form-control,
0618: input.form-control,
0619: select.form-select {
0620:     background: rgba(255, 255, 255, 0.10) !important;
0621:     color: #fff3ff !important;
```
Linija 626 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0623:     box-shadow: none !important;
0624: }
0625: 
0626: textarea.form-control::placeholder,
0627: input.form-control::placeholder {
0628:     color: rgba(243, 232, 255, 0.52) !important;
0629: }
```
Linija 627 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0624: }
0625: 
0626: textarea.form-control::placeholder,
0627: input.form-control::placeholder {
0628:     color: rgba(243, 232, 255, 0.52) !important;
0629: }
0630: 
```
Linija 627 — `input_selector` — genericki input selector:
```txt
0624: }
0625: 
0626: textarea.form-control::placeholder,
0627: input.form-control::placeholder {
0628:     color: rgba(243, 232, 255, 0.52) !important;
0629: }
0630: 
```
Linija 631 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0628:     color: rgba(243, 232, 255, 0.52) !important;
0629: }
0630: 
0631: textarea.form-control:focus,
0632: input.form-control:focus,
0633: select.form-select:focus {
0634:     border-color: rgba(243, 176, 255, 0.58) !important;
```
Linija 632 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0629: }
0630: 
0631: textarea.form-control:focus,
0632: input.form-control:focus,
0633: select.form-select:focus {
0634:     border-color: rgba(243, 176, 255, 0.58) !important;
0635:     box-shadow: none !important;
```
Linija 632 — `input_selector` — genericki input selector:
```txt
0629: }
0630: 
0631: textarea.form-control:focus,
0632: input.form-control:focus,
0633: select.form-select:focus {
0634:     border-color: rgba(243, 176, 255, 0.58) !important;
0635:     box-shadow: none !important;
```
Linija 639 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0636: }
0637: 
0638: .blog-action-outline,
0639: .btn-outline-light {
0640:     border-color: rgba(243, 176, 255, 0.32) !important;
0641:     color: #fff3ff !important;
0642:     background: rgba(255, 255, 255, 0.10) !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `dimni_akordi`

- Datoteka: `blog\templates\blog\designs\dimni_akordi.html`
- Grupa: `zajednicki_layout`
- Hitovi: **10**
- Rizični hitovi: **10**

Linija 53 — `navbar` — dira navbar:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54 — `navbar` — dira navbar:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```
Linija 239 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0236:     color: #ffe0be;
0237: }
0238: 
0239: .btn-outline-light {
0240:     border-color: rgba(239, 192, 143, 0.38) !important;
0241:     color: #ffe0be !important;
0242: }
```
Linija 244 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0241:     color: #ffe0be !important;
0242: }
0243: 
0244: .btn-outline-light:hover {
0245:     background: rgba(239, 192, 143, 0.12) !important;
0246:     color: #fff4e9 !important;
0247: }
```
Linija 332 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0329:     padding: 10px 44px 10px 12px;
0330: }
0331: 
0332: textarea.form-control,
0333: input.form-control,
0334: select.form-select {
0335:     background: rgba(40, 23, 17, 0.62) !important;
```
Linija 333 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0330: }
0331: 
0332: textarea.form-control,
0333: input.form-control,
0334: select.form-select {
0335:     background: rgba(40, 23, 17, 0.62) !important;
0336:     color: #f5e4d6 !important;
```
Linija 333 — `input_selector` — genericki input selector:
```txt
0330: }
0331: 
0332: textarea.form-control,
0333: input.form-control,
0334: select.form-select {
0335:     background: rgba(40, 23, 17, 0.62) !important;
0336:     color: #f5e4d6 !important;
```
Linija 340 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0337:     border-color: rgba(208, 151, 108, 0.18) !important;
0338: }
0339: 
0340: textarea.form-control::placeholder,
0341: input.form-control::placeholder {
0342:     color: rgba(245, 228, 214, 0.56) !important;
0343: }
```
Linija 341 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0338: }
0339: 
0340: textarea.form-control::placeholder,
0341: input.form-control::placeholder {
0342:     color: rgba(245, 228, 214, 0.56) !important;
0343: }
0344: 
```
Linija 341 — `input_selector` — genericki input selector:
```txt
0338: }
0339: 
0340: textarea.form-control::placeholder,
0341: input.form-control::placeholder {
0342:     color: rgba(245, 228, 214, 0.56) !important;
0343: }
0344: 
```

### `iznad_oblaka`

- Datoteka: `blog\templates\blog\designs\iznad_oblaka.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```
Linija 408 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0405:     color: #5f6670;
0406: }
0407: 
0408: textarea.form-control,
0409: input.form-control,
0410: select.form-select {
0411:     background: rgba(255, 255, 255, 0.46) !important;
```
Linija 409 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0406: }
0407: 
0408: textarea.form-control,
0409: input.form-control,
0410: select.form-select {
0411:     background: rgba(255, 255, 255, 0.46) !important;
0412:     color: #4f5863 !important;
```
Linija 409 — `input_selector` — genericki input selector:
```txt
0406: }
0407: 
0408: textarea.form-control,
0409: input.form-control,
0410: select.form-select {
0411:     background: rgba(255, 255, 255, 0.46) !important;
0412:     color: #4f5863 !important;
```
Linija 417 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0414:     box-shadow: none !important;
0415: }
0416: 
0417: textarea.form-control::placeholder,
0418: input.form-control::placeholder {
0419:     color: rgba(95, 102, 112, 0.48) !important;
0420: }
```
Linija 418 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0415: }
0416: 
0417: textarea.form-control::placeholder,
0418: input.form-control::placeholder {
0419:     color: rgba(95, 102, 112, 0.48) !important;
0420: }
0421: 
```
Linija 418 — `input_selector` — genericki input selector:
```txt
0415: }
0416: 
0417: textarea.form-control::placeholder,
0418: input.form-control::placeholder {
0419:     color: rgba(95, 102, 112, 0.48) !important;
0420: }
0421: 
```
Linija 422 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0419:     color: rgba(95, 102, 112, 0.48) !important;
0420: }
0421: 
0422: textarea.form-control:focus,
0423: input.form-control:focus,
0424: select.form-select:focus {
0425:     border-color: rgba(221, 186, 202, 0.56) !important;
```
Linija 423 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0420: }
0421: 
0422: textarea.form-control:focus,
0423: input.form-control:focus,
0424: select.form-select:focus {
0425:     border-color: rgba(221, 186, 202, 0.56) !important;
0426:     box-shadow: none !important;
```
Linija 423 — `input_selector` — genericki input selector:
```txt
0420: }
0421: 
0422: textarea.form-control:focus,
0423: input.form-control:focus,
0424: select.form-select:focus {
0425:     border-color: rgba(221, 186, 202, 0.56) !important;
0426:     box-shadow: none !important;
```
Linija 430 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0427: }
0428: 
0429: .blog-action-outline,
0430: .btn-outline-light {
0431:     border-color: rgba(221, 186, 202, 0.44) !important;
0432:     color: #5f6670 !important;
0433:     background: rgba(255, 255, 255, 0.36) !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `jedro_u_suton`

- Datoteka: `blog\templates\blog\designs\jedro_u_suton.html`
- Grupa: `posebni`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 31 — `navbar` — dira navbar:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(38, 23, 17, 0.78) !important;
```
Linija 39 — `navbar` — dira navbar:
```txt
0036:     border-bottom: 1px solid rgba(255, 228, 203, 0.10);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```
Linija 256 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0253:     box-shadow: 0 8px 18px rgba(18, 11, 8, 0.22);
0254: }
0255: 
0256: .jus-profile-wrap .btn-primary {
0257:     background: rgba(255, 210, 168, 0.18);
0258:     border-color: rgba(255, 210, 168, 0.52);
0259:     color: #fff8ef;
```
Linija 262 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0259:     color: #fff8ef;
0260: }
0261: 
0262: .jus-profile-wrap .btn-primary:hover {
0263:     background: rgba(255, 210, 168, 0.24);
0264:     border-color: rgba(255, 210, 168, 0.66);
0265:     color: #fffdf9;
```
Linija 268 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0265:     color: #fffdf9;
0266: }
0267: 
0268: .jus-profile-wrap .btn-outline-primary {
0269:     color: #ffd2a8;
0270:     border-color: rgba(255, 210, 168, 0.48);
0271: }
```
Linija 273 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0270:     border-color: rgba(255, 210, 168, 0.48);
0271: }
0272: 
0273: .jus-profile-wrap .btn-outline-primary:hover {
0274:     background: rgba(255, 210, 168, 0.16);
0275:     color: #fff8ef;
0276: }
```
Linija 397 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0394: }
0395: 
0396: .blog-action-outline,
0397: .btn-outline-light,
0398: .jus-theme .btn-outline-secondary {
0399:     border-color: rgba(255, 210, 168, 0.48) !important;
0400:     color: #ffd2a8 !important;
```
Linija 398 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0395: 
0396: .blog-action-outline,
0397: .btn-outline-light,
0398: .jus-theme .btn-outline-secondary {
0399:     border-color: rgba(255, 210, 168, 0.48) !important;
0400:     color: #ffd2a8 !important;
0401:     background: transparent !important;
```
Linija 405 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0402: }
0403: 
0404: .blog-action-outline:hover,
0405: .btn-outline-light:hover,
0406: .jus-theme .btn-outline-secondary:hover {
0407:     background: rgba(255, 210, 168, 0.14) !important;
0408:     color: #fff8ef !important;
```
Linija 406 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0403: 
0404: .blog-action-outline:hover,
0405: .btn-outline-light:hover,
0406: .jus-theme .btn-outline-secondary:hover {
0407:     background: rgba(255, 210, 168, 0.14) !important;
0408:     color: #fff8ef !important;
0409:     box-shadow: 0 0 8px rgba(255, 210, 168, 0.14);
```
Linija 420 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0417: }
0418: 
0419: .comment-row textarea,
0420: .comment-row .form-control {
0421:     flex: 1;
0422:     background: rgba(255, 245, 235, 0.06) !important;
0423:     color: #fff7ef !important;
```
Linija 431 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0428: }
0429: 
0430: .comment-row textarea:focus,
0431: .comment-row .form-control:focus {
0432:     border-color: rgba(255, 210, 168, 0.34) !important;
0433:     box-shadow: 0 0 0 0.2rem rgba(255, 210, 168, 0.08) !important;
0434: }
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `kraljevska_pozornica`

- Datoteka: `blog\templates\blog\designs\kraljevska_pozornica.html`
- Grupa: `zajednicki_layout`
- Hitovi: **5**
- Rizični hitovi: **5**

Linija 79 — `navbar` — dira navbar:
```txt
0076:     background-repeat: no-repeat;
0077: }
0078: 
0079: nav.navbar {
0080:     position: relative;
0081:     z-index: 4000 !important;
0082: }
```
Linija 84 — `navbar` — dira navbar:
```txt
0081:     z-index: 4000 !important;
0082: }
0083: 
0084: nav.navbar .dropdown-menu {
0085:     z-index: 4100 !important;
0086: }
0087: 
```
Linija 568 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0565:     box-shadow: 0 14px 28px rgba(255, 195, 124, 0.22);
0566: }
0567: 
0568: .blog-profile-panel .btn-outline-primary {
0569:     border-color: rgba(255, 201, 142, 0.30);
0570:     color: #ffe6cd;
0571:     background: rgba(255, 255, 255, 0.03);
```
Linija 574 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0571:     background: rgba(255, 255, 255, 0.03);
0572: }
0573: 
0574: .blog-profile-panel .btn-outline-primary:hover,
0575: .blog-profile-panel .btn-outline-primary:focus {
0576:     background: rgba(255, 201, 142, 0.12);
0577:     color: #ffffff;
```
Linija 575 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0572: }
0573: 
0574: .blog-profile-panel .btn-outline-primary:hover,
0575: .blog-profile-panel .btn-outline-primary:focus {
0576:     background: rgba(255, 201, 142, 0.12);
0577:     color: #ffffff;
0578:     border-color: rgba(255, 201, 142, 0.42);
```

### `magazin`

- Datoteka: `blog\templates\blog\designs\magazin.html`
- Grupa: `posebni_hero`
- Hitovi: **9**
- Rizični hitovi: **9**

Linija 24 — `button_selector` — genericki button selector:
```txt
0021:                     {% if not is_restricted %}
0022:                         <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0023:                             {% csrf_token %}
0024:                             <button type="submit" class="btn {% if is_following %}btn-outline-primary{% else %}btn-primary{% endif %} btn-sm">
0025:                                 {% if is_following %}Pratiš{% else %}Prati{% endif %}
0026:                             </button>
0027:                         </form>
```
Linija 45 — `button_selector` — genericki button selector:
```txt
0042:                                 <li>
0043:                                     <form method="post" action="{% url 'unfollow_user' blog.username %}" class="m-0">
0044:                                         {% csrf_token %}
0045:                                         <button type="submit" class="dropdown-item">Prestani pratiti</button>
0046:                                     </form>
0047:                                 </li>
0048:                             {% else %}
```
Linija 52 — `button_selector` — genericki button selector:
```txt
0049:                                 <li>
0050:                                     <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0051:                                         {% csrf_token %}
0052:                                         <button type="submit" class="dropdown-item" {% if is_restricted %}disabled{% endif %}>Prati korisnika</button>
0053:                                     </form>
0054:                                 </li>
0055:                             {% endif %}
```
Linija 60 — `button_selector` — genericki button selector:
```txt
0057:                             <li>
0058:                                 <form method="post" action="{% url 'restrict_user' blog.username %}" class="m-0">
0059:                                     {% csrf_token %}
0060:                                     <button type="submit" class="dropdown-item">Ograniči korisnika</button>
0061:                                 </form>
0062:                             </li>
0063: 
```
Linija 69 — `button_selector` — genericki button selector:
```txt
0066:                             <li>
0067:                                 <form method="post" action="{% url 'block_user' blog.username %}" class="m-0">
0068:                                     {% csrf_token %}
0069:                                     <button type="submit" class="dropdown-item text-danger">Blokiraj korisnika</button>
0070:                                 </form>
0071:                             </li>
0072:                         </ul>
```
Linija 352 — `navbar` — dira navbar:
```txt
0349:     z-index: 9999;
0350: }
0351: 
0352: nav.navbar {
0353:     position: relative;
0354:     z-index: 5000 !important;
0355: }
```
Linija 357 — `navbar` — dira navbar:
```txt
0354:     z-index: 5000 !important;
0355: }
0356: 
0357: nav.navbar .dropdown-menu {
0358:     z-index: 5100 !important;
0359: }
0360: 
```
Linija 613 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0610:     border: 1px solid var(--magazin-content-border);
0611: }
0612: 
0613: textarea.form-control {
0614:     background: #fff !important;
0615:     color: var(--magazin-text) !important;
0616:     border: 1px solid var(--magazin-content-border) !important;
```
Linija 619 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0616:     border: 1px solid var(--magazin-content-border) !important;
0617: }
0618: 
0619: textarea.form-control:focus {
0620:     box-shadow: 0 0 0 0.12rem rgba(155, 123, 90, 0.18) !important;
0621:     border-color: #b68f68 !important;
0622: }
```

### `misticno_jezero`

- Datoteka: `blog\templates\blog\designs\misticno_jezero.html`
- Grupa: `posebni`
- Hitovi: **12**
- Rizični hitovi: **12**

Linija 31 — `navbar` — dira navbar:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(26, 10, 36, 0.76) !important;
```
Linija 39 — `navbar` — dira navbar:
```txt
0036:     backdrop-filter: blur(8px);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```
Linija 222 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0219:     box-shadow: 0 8px 18px rgba(15, 5, 24, 0.28);
0220: }
0221: 
0222: .mj-profile-wrap .btn-primary {
0223:     background: #f7c88f;
0224:     border-color: #f7c88f;
0225:     color: #311a1a;
```
Linija 228 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0225:     color: #311a1a;
0226: }
0227: 
0228: .mj-profile-wrap .btn-primary:hover {
0229:     background: #ffddb0;
0230:     border-color: #ffddb0;
0231:     color: #261414;
```
Linija 234 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0231:     color: #261414;
0232: }
0233: 
0234: .mj-profile-wrap .btn-outline-primary {
0235:     color: #ffe7be;
0236:     border-color: #ffe7be;
0237: }
```
Linija 239 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0236:     border-color: #ffe7be;
0237: }
0238: 
0239: .mj-profile-wrap .btn-outline-primary:hover {
0240:     background: #ffe7be;
0241:     color: #311a1a;
0242: }
```
Linija 401 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0398: }
0399: 
0400: .blog-action-outline,
0401: .btn-outline-light {
0402:     border-color: #ffe7be !important;
0403:     color: #ffe7be !important;
0404:     background: transparent !important;
```
Linija 408 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0405: }
0406: 
0407: .blog-action-outline:hover,
0408: .btn-outline-light:hover {
0409:     background: rgba(255, 231, 190, 0.16) !important;
0410:     color: #fffaf4 !important;
0411:     box-shadow: 0 0 10px rgba(255,231,190,0.14);
```
Linija 430 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0427: }
0428: 
0429: .comment-row textarea,
0430: .comment-row .form-control {
0431:     flex: 1;
0432:     background: rgba(255,255,255,0.08) !important;
0433:     color: #f5e9ff !important;
```
Linija 441 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0438: }
0439: 
0440: .comment-row textarea:focus,
0441: .comment-row .form-control:focus {
0442:     border-color: rgba(255,231,190,0.34) !important;
0443:     box-shadow: 0 0 0 0.2rem rgba(255,231,190,0.08) !important;
0444: }
```
Linija 447 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0444: }
0445: 
0446: .comment-row textarea::placeholder,
0447: .comment-row .form-control::placeholder {
0448:     color: #ead8f6 !important;
0449: }
0450: 
```
Linija 579 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0576:         align-items: stretch;
0577:     }
0578: 
0579:     .comment-row .btn {
0580:         width: 100%;
0581:     }
0582: }
```

### `mjesecev_ples`

- Datoteka: `blog\templates\blog\designs\mjesecev_ples.html`
- Grupa: `zajednicki_layout`
- Hitovi: **10**
- Rizični hitovi: **10**

Linija 53 — `navbar` — dira navbar:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54 — `navbar` — dira navbar:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```
Linija 249 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0246:     color: #ffe4bf;
0247: }
0248: 
0249: .btn-outline-light {
0250:     border-color: rgba(239, 201, 151, 0.38) !important;
0251:     color: #ffe4bf !important;
0252: }
```
Linija 254 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0251:     color: #ffe4bf !important;
0252: }
0253: 
0254: .btn-outline-light:hover {
0255:     background: rgba(239, 201, 151, 0.12) !important;
0256:     color: #fff6ec !important;
0257: }
```
Linija 350 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0347:     color: #efe5d8 !important;
0348: }
0349: 
0350: textarea.form-control,
0351: input.form-control,
0352: select.form-select {
0353:     background: rgba(34, 26, 21, 0.62) !important;
```
Linija 351 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0348: }
0349: 
0350: textarea.form-control,
0351: input.form-control,
0352: select.form-select {
0353:     background: rgba(34, 26, 21, 0.62) !important;
0354:     color: #f5e9db !important;
```
Linija 351 — `input_selector` — genericki input selector:
```txt
0348: }
0349: 
0350: textarea.form-control,
0351: input.form-control,
0352: select.form-select {
0353:     background: rgba(34, 26, 21, 0.62) !important;
0354:     color: #f5e9db !important;
```
Linija 358 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0355:     border-color: rgba(207, 177, 132, 0.18) !important;
0356: }
0357: 
0358: textarea.form-control::placeholder,
0359: input.form-control::placeholder {
0360:     color: rgba(245, 233, 219, 0.56) !important;
0361: }
```
Linija 359 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0356: }
0357: 
0358: textarea.form-control::placeholder,
0359: input.form-control::placeholder {
0360:     color: rgba(245, 233, 219, 0.56) !important;
0361: }
0362: 
```
Linija 359 — `input_selector` — genericki input selector:
```txt
0356: }
0357: 
0358: textarea.form-control::placeholder,
0359: input.form-control::placeholder {
0360:     color: rgba(245, 233, 219, 0.56) !important;
0361: }
0362: 
```

### `morski_prijelaz`

- Datoteka: `blog\templates\blog\designs\morski_prijelaz.html`
- Grupa: `zajednicki_layout`
- Hitovi: **7**
- Rizični hitovi: **7**

Linija 41 — `navbar` — dira navbar:
```txt
0038:         background-size: cover, cover;
0039:     }
0040: 
0041:     nav.navbar {
0042:         position: relative;
0043:         z-index: 4000 !important;
0044:     }
```
Linija 46 — `navbar` — dira navbar:
```txt
0043:         z-index: 4000 !important;
0044:     }
0045: 
0046:     nav.navbar .dropdown-menu {
0047:         z-index: 4100 !important;
0048:     }
0049: 
```
Linija 329 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0326:         padding: 10px 44px 10px 12px;
0327:     }
0328: 
0329:     textarea.form-control {
0330:         background: transparent !important;
0331:         color: #ffffff !important;
0332:         border: 1px solid rgba(197, 220, 255, 0.24) !important;
```
Linija 336 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0333:         border-radius: 12px;
0334:     }
0335: 
0336:     textarea.form-control:focus {
0337:         background: transparent !important;
0338:         color: #ffffff !important;
0339:         border-color: rgba(207, 225, 255, 0.44) !important;
```
Linija 348 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0345:     }
0346: 
0347:     .blog-action-outline,
0348:     .btn-outline-light {
0349:         border-color: rgba(207, 225, 255, 0.34) !important;
0350:         color: #e7f0ff !important;
0351:     }
```
Linija 354 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0351:     }
0352: 
0353:     .blog-action-outline:hover,
0354:     .btn-outline-light:hover {
0355:         background-color: rgba(207, 225, 255, 0.12) !important;
0356:         color: #ffffff !important;
0357:     }
```
Linija 382 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0379:     .archive-link,
0380:     .calendar-day,
0381:     .comment-body,
0382:     textarea.form-control {
0383:         border-color: rgba(197, 220, 255, 0.18) !important;
0384:     }
0385: 
```

### `nebeska_klasika`

- Datoteka: `blog\templates\blog\designs\nebeska_klasika.html`
- Grupa: `posebni`
- Hitovi: **9**
- Rizični hitovi: **9**

Linija 29 — `navbar` — dira navbar:
```txt
0026:     display: none;
0027: }
0028: 
0029: nav.navbar {
0030:     position: relative;
0031:     z-index: 4000 !important;
0032:     background: rgba(42, 45, 51, 0.84) !important;
```
Linija 37 — `navbar` — dira navbar:
```txt
0034:     border-bottom: 1px solid rgba(255,255,255,0.08);
0035: }
0036: 
0037: nav.navbar .dropdown-menu {
0038:     z-index: 4100 !important;
0039: }
0040: 
```
Linija 211 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0208:     box-shadow: 0 6px 16px rgba(108, 95, 80, 0.16);
0209: }
0210: 
0211: .nk-profile-wrap .btn-primary {
0212:     background: #6d7e9f;
0213:     border-color: #6d7e9f;
0214: }
```
Linija 216 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0213:     border-color: #6d7e9f;
0214: }
0215: 
0216: .nk-profile-wrap .btn-outline-primary {
0217:     color: #6d7e9f;
0218:     border-color: #6d7e9f;
0219: }
```
Linija 371 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0368: }
0369: 
0370: .blog-action-outline,
0371: .btn-outline-light {
0372:     border-color: #6d7e9f !important;
0373:     color: #6d7e9f !important;
0374:     background: transparent !important;
```
Linija 378 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0375: }
0376: 
0377: .blog-action-outline:hover,
0378: .btn-outline-light:hover {
0379:     background: #6d7e9f !important;
0380:     color: #fff !important;
0381:     box-shadow: 0 0 8px rgba(109,126,159,0.25);
```
Linija 392 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0389: }
0390: 
0391: .comment-row textarea,
0392: .comment-row .form-control {
0393:     flex: 1;
0394:     background: rgba(255,255,255,0.70) !important;
0395:     color: #554a44 !important;
```
Linija 403 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0400: }
0401: 
0402: .comment-row textarea:focus,
0403: .comment-row .form-control:focus {
0404:     border-color: rgba(109,126,159,0.62) !important;
0405:     box-shadow: 0 0 0 0.2rem rgba(109,126,159,0.12) !important;
0406: }
```
Linija 540 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0537:         align-items: stretch;
0538:     }
0539: 
0540:     .comment-row .btn {
0541:         width: 100%;
0542:     }
0543: }
```

### `nebeski_mir`

- Datoteka: `blog\templates\blog\designs\nebeski_mir.html`
- Grupa: `zajednicki_layout`
- Hitovi: **6**
- Rizični hitovi: **6**

Linija 44 — `navbar` — dira navbar:
```txt
0041:     background-size: 100% 100%, cover;
0042: }
0043: 
0044: nav.navbar {
0045:     position: relative;
0046:     z-index: 4000 !important;
0047:     background: rgba(0, 0, 0, 0.88) !important;
```
Linija 51 — `navbar` — dira navbar:
```txt
0048:     backdrop-filter: blur(8px);
0049: }
0050: 
0051: nav.navbar .dropdown-menu {
0052:     z-index: 4100 !important;
0053: }
0054: 
```
Linija 295 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0292:     padding: 10px 44px 10px 12px;
0293: }
0294: 
0295: textarea.form-control {
0296:     background: rgba(255, 255, 255, 0.72) !important;
0297:     color: #334155 !important;
0298:     border: 1px solid rgba(71, 85, 105, 0.18) !important;
```
Linija 302 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0299:     border-radius: 12px;
0300: }
0301: 
0302: textarea.form-control:focus {
0303:     background: rgba(255, 255, 255, 0.92) !important;
0304:     color: #334155 !important;
0305:     border-color: rgba(71, 85, 105, 0.28) !important;
```
Linija 314 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0311: }
0312: 
0313: .blog-action-outline,
0314: .btn-outline-light {
0315:     border-color: rgba(79, 124, 168, 0.35) !important;
0316:     color: #315f8d !important;
0317:     background: rgba(255, 255, 255, 0.50) !important;
```
Linija 321 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0318: }
0319: 
0320: .blog-action-outline:hover,
0321: .btn-outline-light:hover {
0322:     background-color: rgba(79, 124, 168, 0.12) !important;
0323:     color: #254766 !important;
0324: }
```

### `nebesko_polje`

- Datoteka: `blog\templates\blog\designs\nebesko_polje.html`
- Grupa: `zajednicki_layout`
- Hitovi: **9**
- Rizični hitovi: **9**

Linija 60 — `navbar` — dira navbar:
```txt
0057:     background-size: cover;
0058: }
0059: 
0060: nav.navbar {
0061:     position: relative;
0062:     z-index: 5000 !important;
0063: }
```
Linija 65 — `navbar` — dira navbar:
```txt
0062:     z-index: 5000 !important;
0063: }
0064: 
0065: nav.navbar .dropdown-menu {
0066:     z-index: 5100 !important;
0067: }
0068: 
```
Linija 467 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0464:     flex: 1;
0465: }
0466: 
0467: textarea.form-control,
0468: .comment-row textarea,
0469: input.form-control,
0470: select.form-select {
```
Linija 469 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0466: 
0467: textarea.form-control,
0468: .comment-row textarea,
0469: input.form-control,
0470: select.form-select {
0471:     background-color: rgba(255, 255, 255, 0.58) !important;
0472:     color: #53606d !important;
```
Linija 469 — `input_selector` — genericki input selector:
```txt
0466: 
0467: textarea.form-control,
0468: .comment-row textarea,
0469: input.form-control,
0470: select.form-select {
0471:     background-color: rgba(255, 255, 255, 0.58) !important;
0472:     color: #53606d !important;
```
Linija 478 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0475:     box-shadow: none !important;
0476: }
0477: 
0478: textarea.form-control:focus,
0479: .comment-row textarea:focus,
0480: input.form-control:focus,
0481: select.form-select:focus {
```
Linija 480 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0477: 
0478: textarea.form-control:focus,
0479: .comment-row textarea:focus,
0480: input.form-control:focus,
0481: select.form-select:focus {
0482:     background-color: rgba(255, 255, 255, 0.76) !important;
0483:     color: #4c5763 !important;
```
Linija 480 — `input_selector` — genericki input selector:
```txt
0477: 
0478: textarea.form-control:focus,
0479: .comment-row textarea:focus,
0480: input.form-control:focus,
0481: select.form-select:focus {
0482:     background-color: rgba(255, 255, 255, 0.76) !important;
0483:     color: #4c5763 !important;
```
Linija 489 — `input_selector` — genericki input selector:
```txt
0486: }
0487: 
0488: textarea::placeholder,
0489: input::placeholder {
0490:     color: rgba(89, 100, 114, 0.54) !important;
0491: }
0492: 
```

### `neonski_grad`

- Datoteka: `blog\templates\blog\designs\neonski_grad.html`
- Grupa: `zajednicki_layout`
- Hitovi: **16**
- Rizični hitovi: **16**

Linija 44 — `navbar` — dira navbar:
```txt
0041:     background-size: 100% 100%, 100% 100%, 100% auto;
0042: }
0043: 
0044: nav.navbar {
0045:     position: relative;
0046:     z-index: 4000 !important;
0047: }
```
Linija 49 — `navbar` — dira navbar:
```txt
0046:     z-index: 4000 !important;
0047: }
0048: 
0049: nav.navbar .dropdown-menu {
0050:     z-index: 4100 !important;
0051: }
0052: 
```
Linija 412 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0409:     color: #f0e4ff;
0410: }
0411: 
0412: textarea.form-control,
0413: input.form-control,
0414: select.form-select {
0415:     background: rgba(255, 255, 255, 0.03) !important;
```
Linija 413 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0410: }
0411: 
0412: textarea.form-control,
0413: input.form-control,
0414: select.form-select {
0415:     background: rgba(255, 255, 255, 0.03) !important;
0416:     color: #f5edff !important;
```
Linija 413 — `input_selector` — genericki input selector:
```txt
0410: }
0411: 
0412: textarea.form-control,
0413: input.form-control,
0414: select.form-select {
0415:     background: rgba(255, 255, 255, 0.03) !important;
0416:     color: #f5edff !important;
```
Linija 421 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0418:     box-shadow: none !important;
0419: }
0420: 
0421: textarea.form-control::placeholder,
0422: input.form-control::placeholder {
0423:     color: rgba(240, 228, 255, 0.42) !important;
0424: }
```
Linija 422 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0419: }
0420: 
0421: textarea.form-control::placeholder,
0422: input.form-control::placeholder {
0423:     color: rgba(240, 228, 255, 0.42) !important;
0424: }
0425: 
```
Linija 422 — `input_selector` — genericki input selector:
```txt
0419: }
0420: 
0421: textarea.form-control::placeholder,
0422: input.form-control::placeholder {
0423:     color: rgba(240, 228, 255, 0.42) !important;
0424: }
0425: 
```
Linija 426 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0423:     color: rgba(240, 228, 255, 0.42) !important;
0424: }
0425: 
0426: textarea.form-control:focus,
0427: input.form-control:focus,
0428: select.form-select:focus {
0429:     border-color: rgba(224, 110, 255, 0.36) !important;
```
Linija 427 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0424: }
0425: 
0426: textarea.form-control:focus,
0427: input.form-control:focus,
0428: select.form-select:focus {
0429:     border-color: rgba(224, 110, 255, 0.36) !important;
0430:     box-shadow: 0 0 0 0.18rem rgba(224, 110, 255, 0.10) !important;
```
Linija 427 — `input_selector` — genericki input selector:
```txt
0424: }
0425: 
0426: textarea.form-control:focus,
0427: input.form-control:focus,
0428: select.form-select:focus {
0429:     border-color: rgba(224, 110, 255, 0.36) !important;
0430:     box-shadow: 0 0 0 0.18rem rgba(224, 110, 255, 0.10) !important;
```
Linija 434 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0431: }
0432: 
0433: .blog-action-outline,
0434: .btn-outline-light {
0435:     border-color: rgba(224, 110, 255, 0.34) !important;
0436:     color: #f7f0ff !important;
0437:     background: rgba(255, 255, 255, 0.03) !important;
```
_Još 4 hitova prikazano je u JSON dokumentu._

### `planine_u_magli`

- Datoteka: `blog\templates\blog\designs\planine_u_magli.html`
- Grupa: `zajednicki_layout`
- Hitovi: **6**
- Rizični hitovi: **6**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, cover;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046:     background: rgba(23, 28, 36, 0.88) !important;
```
Linija 50 — `navbar` — dira navbar:
```txt
0047:     backdrop-filter: blur(8px);
0048: }
0049: 
0050: nav.navbar .dropdown-menu {
0051:     z-index: 4100 !important;
0052: }
0053: 
```
Linija 303 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0300:     background: rgba(255,255,255,0.36) !important;
0301: }
0302: 
0303: textarea.form-control {
0304:     background: rgba(255,255,255,0.54) !important;
0305:     color: #5f6975 !important;
0306:     border: 1px solid rgba(160,175,196,0.24) !important;
```
Linija 310 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0307:     border-radius: 14px;
0308: }
0309: 
0310: textarea.form-control:focus {
0311:     background: rgba(255,255,255,0.72) !important;
0312:     color: #5f6975 !important;
0313:     border-color: rgba(142,163,187,0.42) !important;
```
Linija 322 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0319: }
0320: 
0321: .blog-action-outline,
0322: .btn-outline-light {
0323:     border-color: rgba(142,163,187,0.34) !important;
0324:     color: #617181 !important;
0325:     background: rgba(255,255,255,0.20) !important;
```
Linija 329 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0326: }
0327: 
0328: .blog-action-outline:hover,
0329: .btn-outline-light:hover {
0330:     background-color: rgba(230,237,245,0.62) !important;
0331:     color: #4b5967 !important;
0332: }
```

### `podvodna_tisina`

- Datoteka: `blog\templates\blog\designs\podvodna_tisina.html`
- Grupa: `zajednicki_layout`
- Hitovi: **7**
- Rizični hitovi: **7**

Linija 43 — `navbar` — dira navbar:
```txt
0040:         background-size: 100% 100%, 100% auto;
0041:     }
0042: 
0043:     nav.navbar {
0044:         position: relative;
0045:         z-index: 4000 !important;
0046:     }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:         z-index: 4000 !important;
0046:     }
0047: 
0048:     nav.navbar .dropdown-menu {
0049:         z-index: 4100 !important;
0050:     }
0051: 
```
Linija 280 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0277:         padding: 10px 44px 10px 12px;
0278:     }
0279: 
0280:     textarea.form-control {
0281:         background: transparent !important;
0282:         color: #ffffff !important;
0283:         border: 1px solid rgba(197, 220, 255, 0.24) !important;
```
Linija 287 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0284:         border-radius: 12px;
0285:     }
0286: 
0287:     textarea.form-control:focus {
0288:         background: transparent !important;
0289:         color: #ffffff !important;
0290:         border-color: rgba(207, 225, 255, 0.44) !important;
```
Linija 299 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0296:     }
0297: 
0298:     .blog-action-outline,
0299:     .btn-outline-light {
0300:         border-color: rgba(207, 225, 255, 0.34) !important;
0301:         color: #e7f0ff !important;
0302:     }
```
Linija 305 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0302:     }
0303: 
0304:     .blog-action-outline:hover,
0305:     .btn-outline-light:hover {
0306:         background-color: rgba(207, 225, 255, 0.12) !important;
0307:         color: #ffffff !important;
0308:     }
```
Linija 333 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0330:     .archive-link,
0331:     .calendar-day,
0332:     .comment-body,
0333:     textarea.form-control {
0334:         border-color: rgba(197, 220, 255, 0.18) !important;
0335:     }
0336: 
```

### `polarna_svjetlost`

- Datoteka: `blog\templates\blog\designs\polarna_svjetlost.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```
Linija 406 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0403:     color: #e0f3ff;
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
```
Linija 407 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
0410:     color: #eefbff !important;
```
Linija 407 — `input_selector` — genericki input selector:
```txt
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
0410:     color: #eefbff !important;
```
Linija 415 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0412:     box-shadow: none !important;
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(222, 241, 255, 0.48) !important;
0418: }
```
Linija 416 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(222, 241, 255, 0.48) !important;
0418: }
0419: 
```
Linija 416 — `input_selector` — genericki input selector:
```txt
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(222, 241, 255, 0.48) !important;
0418: }
0419: 
```
Linija 420 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0417:     color: rgba(222, 241, 255, 0.48) !important;
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(196, 244, 255, 0.46) !important;
```
Linija 421 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(196, 244, 255, 0.46) !important;
0424:     box-shadow: none !important;
```
Linija 421 — `input_selector` — genericki input selector:
```txt
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(196, 244, 255, 0.46) !important;
0424:     box-shadow: none !important;
```
Linija 428 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0425: }
0426: 
0427: .blog-action-outline,
0428: .btn-outline-light {
0429:     border-color: rgba(196, 244, 255, 0.36) !important;
0430:     color: #eefbff !important;
0431:     background: transparent !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `polje_lavande`

- Datoteka: `blog\templates\blog\designs\polje_lavande.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```
Linija 508 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0505:     color: #5a3271;
0506: }
0507: 
0508: textarea.form-control,
0509: input.form-control,
0510: select.form-select {
0511:     background: rgba(255, 255, 255, 0.24) !important;
```
Linija 509 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0506: }
0507: 
0508: textarea.form-control,
0509: input.form-control,
0510: select.form-select {
0511:     background: rgba(255, 255, 255, 0.24) !important;
0512:     color: #4f2768 !important;
```
Linija 509 — `input_selector` — genericki input selector:
```txt
0506: }
0507: 
0508: textarea.form-control,
0509: input.form-control,
0510: select.form-select {
0511:     background: rgba(255, 255, 255, 0.24) !important;
0512:     color: #4f2768 !important;
```
Linija 517 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0514:     box-shadow: none !important;
0515: }
0516: 
0517: textarea.form-control::placeholder,
0518: input.form-control::placeholder {
0519:     color: rgba(90, 50, 113, 0.48) !important;
0520: }
```
Linija 518 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0515: }
0516: 
0517: textarea.form-control::placeholder,
0518: input.form-control::placeholder {
0519:     color: rgba(90, 50, 113, 0.48) !important;
0520: }
0521: 
```
Linija 518 — `input_selector` — genericki input selector:
```txt
0515: }
0516: 
0517: textarea.form-control::placeholder,
0518: input.form-control::placeholder {
0519:     color: rgba(90, 50, 113, 0.48) !important;
0520: }
0521: 
```
Linija 522 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0519:     color: rgba(90, 50, 113, 0.48) !important;
0520: }
0521: 
0522: textarea.form-control:focus,
0523: input.form-control:focus,
0524: select.form-select:focus {
0525:     border-color: rgba(158, 111, 214, 0.56) !important;
```
Linija 523 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0520: }
0521: 
0522: textarea.form-control:focus,
0523: input.form-control:focus,
0524: select.form-select:focus {
0525:     border-color: rgba(158, 111, 214, 0.56) !important;
0526:     box-shadow: none !important;
```
Linija 523 — `input_selector` — genericki input selector:
```txt
0520: }
0521: 
0522: textarea.form-control:focus,
0523: input.form-control:focus,
0524: select.form-select:focus {
0525:     border-color: rgba(158, 111, 214, 0.56) !important;
0526:     box-shadow: none !important;
```
Linija 530 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0527: }
0528: 
0529: .blog-action-outline,
0530: .btn-outline-light {
0531:     border-color: rgba(158, 111, 214, 0.42) !important;
0532:     color: #5a3271 !important;
0533:     background: rgba(255, 255, 255, 0.18) !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `ponocna_elegancija`

- Datoteka: `blog\templates\blog\designs\ponocna_elegancija.html`
- Grupa: `posebni`
- Hitovi: **12**
- Rizični hitovi: **12**

Linija 31 — `navbar` — dira navbar:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(9, 14, 25, 0.84) !important;
```
Linija 39 — `navbar` — dira navbar:
```txt
0036:     border-bottom: 1px solid rgba(255,255,255,0.08);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```
Linija 220 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0217:     box-shadow: 0 8px 18px rgba(0, 0, 0, 0.28);
0218: }
0219: 
0220: .pe-profile-wrap .btn-primary {
0221:     background: #d7c28d;
0222:     border-color: #d7c28d;
0223:     color: #111722;
```
Linija 226 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0223:     color: #111722;
0224: }
0225: 
0226: .pe-profile-wrap .btn-primary:hover {
0227:     background: #e6d19d;
0228:     border-color: #e6d19d;
0229:     color: #0d1118;
```
Linija 232 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0229:     color: #0d1118;
0230: }
0231: 
0232: .pe-profile-wrap .btn-outline-primary {
0233:     color: #d7c28d;
0234:     border-color: #d7c28d;
0235: }
```
Linija 237 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0234:     border-color: #d7c28d;
0235: }
0236: 
0237: .pe-profile-wrap .btn-outline-primary:hover {
0238:     background: #d7c28d;
0239:     color: #111722;
0240: }
```
Linija 398 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0395: }
0396: 
0397: .blog-action-outline,
0398: .btn-outline-light {
0399:     border-color: #d7c28d !important;
0400:     color: #d7c28d !important;
0401:     background: transparent !important;
```
Linija 405 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0402: }
0403: 
0404: .blog-action-outline:hover,
0405: .btn-outline-light:hover {
0406:     background: #d7c28d !important;
0407:     color: #111722 !important;
0408:     box-shadow: 0 0 10px rgba(215,194,141,0.16);
```
Linija 419 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0416: }
0417: 
0418: .comment-row textarea,
0419: .comment-row .form-control {
0420:     flex: 1;
0421:     background: rgba(255,255,255,0.07) !important;
0422:     color: #dce1ee !important;
```
Linija 430 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0427: }
0428: 
0429: .comment-row textarea:focus,
0430: .comment-row .form-control:focus {
0431:     border-color: rgba(215,194,141,0.46) !important;
0432:     box-shadow: 0 0 0 0.2rem rgba(215,194,141,0.10) !important;
0433: }
```
Linija 436 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0433: }
0434: 
0435: .comment-row textarea::placeholder,
0436: .comment-row .form-control::placeholder {
0437:     color: #aeb8ce !important;
0438: }
0439: 
```
Linija 567 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0564:         align-items: stretch;
0565:     }
0566: 
0567:     .comment-row .btn {
0568:         width: 100%;
0569:     }
0570: }
```

### `ruzicasti_vrt`

- Datoteka: `blog\templates\blog\designs\ruzicasti_vrt.html`
- Grupa: `posebni`
- Hitovi: **12**
- Rizični hitovi: **12**

Linija 31 — `navbar` — dira navbar:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(64, 42, 49, 0.24) !important;
```
Linija 39 — `navbar` — dira navbar:
```txt
0036:     border-bottom: 1px solid rgba(255,255,255,0.14);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```
Linija 221 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0218:     box-shadow: 0 8px 18px rgba(126, 93, 96, 0.14);
0219: }
0220: 
0221: .rv-profile-wrap .btn-primary {
0222:     background: #be738c;
0223:     border-color: #be738c;
0224:     color: #fff8fa;
```
Linija 227 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0224:     color: #fff8fa;
0225: }
0226: 
0227: .rv-profile-wrap .btn-primary:hover {
0228:     background: #aa617b;
0229:     border-color: #aa617b;
0230: }
```
Linija 232 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0229:     border-color: #aa617b;
0230: }
0231: 
0232: .rv-profile-wrap .btn-outline-primary {
0233:     color: #be738c;
0234:     border-color: #be738c;
0235: }
```
Linija 237 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0234:     border-color: #be738c;
0235: }
0236: 
0237: .rv-profile-wrap .btn-outline-primary:hover {
0238:     background: #be738c;
0239:     color: #fff8fa;
0240: }
```
Linija 399 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0396: }
0397: 
0398: .blog-action-outline,
0399: .btn-outline-light {
0400:     border-color: #be738c !important;
0401:     color: #be738c !important;
0402:     background: transparent !important;
```
Linija 406 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0403: }
0404: 
0405: .blog-action-outline:hover,
0406: .btn-outline-light:hover {
0407:     background: #be738c !important;
0408:     color: #fff8fa !important;
0409:     box-shadow: 0 0 10px rgba(190,115,140,0.14);
```
Linija 420 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0417: }
0418: 
0419: .comment-row textarea,
0420: .comment-row .form-control {
0421:     flex: 1;
0422:     background: rgba(255,255,255,0.22) !important;
0423:     color: #66575a !important;
```
Linija 431 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0428: }
0429: 
0430: .comment-row textarea:focus,
0431: .comment-row .form-control:focus {
0432:     border-color: rgba(190,115,140,0.44) !important;
0433:     box-shadow: 0 0 0 0.2rem rgba(190,115,140,0.08) !important;
0434: }
```
Linija 437 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0434: }
0435: 
0436: .comment-row textarea::placeholder,
0437: .comment-row .form-control::placeholder {
0438:     color: #9f8587 !important;
0439: }
0440: 
```
Linija 569 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0566:         align-items: stretch;
0567:     }
0568: 
0569:     .comment-row .btn {
0570:         width: 100%;
0571:     }
0572: }
```

### `sjene_ulice`

- Datoteka: `blog\templates\blog\designs\sjene_ulice.html`
- Grupa: `zajednicki_layout`
- Hitovi: **10**
- Rizični hitovi: **10**

Linija 53 — `navbar` — dira navbar:
```txt
0050:     background-size: 100% 100%, 100% auto;
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
```
Linija 54 — `navbar` — dira navbar:
```txt
0051: }
0052: 
0053: nav.navbar,
0054: nav.navbar .dropdown-menu {
0055:     z-index: 4000 !important;
0056: }
0057: 
```
Linija 239 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0236:     color: #f2d1ad;
0237: }
0238: 
0239: .btn-outline-light {
0240:     border-color: rgba(216, 176, 132, 0.30) !important;
0241:     color: #f2d1ad !important;
0242: }
```
Linija 244 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0241:     color: #f2d1ad !important;
0242: }
0243: 
0244: .btn-outline-light:hover {
0245:     background: rgba(216, 176, 132, 0.10) !important;
0246:     color: #fff5ec !important;
0247: }
```
Linija 328 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0325:     padding: 10px 44px 10px 12px;
0326: }
0327: 
0328: textarea.form-control,
0329: input.form-control,
0330: select.form-select {
0331:     background: rgba(33, 27, 24, 0.66) !important;
```
Linija 329 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0326: }
0327: 
0328: textarea.form-control,
0329: input.form-control,
0330: select.form-select {
0331:     background: rgba(33, 27, 24, 0.66) !important;
0332:     color: #f4e8de !important;
```
Linija 329 — `input_selector` — genericki input selector:
```txt
0326: }
0327: 
0328: textarea.form-control,
0329: input.form-control,
0330: select.form-select {
0331:     background: rgba(33, 27, 24, 0.66) !important;
0332:     color: #f4e8de !important;
```
Linija 336 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0333:     border-color: rgba(201, 155, 111, 0.14) !important;
0334: }
0335: 
0336: textarea.form-control::placeholder,
0337: input.form-control::placeholder {
0338:     color: rgba(244, 232, 222, 0.56) !important;
0339: }
```
Linija 337 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0334: }
0335: 
0336: textarea.form-control::placeholder,
0337: input.form-control::placeholder {
0338:     color: rgba(244, 232, 222, 0.56) !important;
0339: }
0340: 
```
Linija 337 — `input_selector` — genericki input selector:
```txt
0334: }
0335: 
0336: textarea.form-control::placeholder,
0337: input.form-control::placeholder {
0338:     color: rgba(244, 232, 222, 0.56) !important;
0339: }
0340: 
```

### `stara_aleja`

- Datoteka: `blog\templates\blog\designs\stara_aleja.html`
- Grupa: `posebni`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 31 — `navbar` — dira navbar:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(44, 30, 20, 0.82) !important;
```
Linija 39 — `navbar` — dira navbar:
```txt
0036:     border-bottom: 1px solid rgba(255,255,255,0.08);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```
Linija 261 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0258:     box-shadow: 0 8px 18px rgba(43, 28, 16, 0.20);
0259: }
0260: 
0261: .sa-profile-wrap .btn-primary {
0262:     background: rgba(255, 211, 154, 0.12);
0263:     border-color: rgba(255, 211, 154, 0.48);
0264:     color: #fff1de;
```
Linija 267 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0264:     color: #fff1de;
0265: }
0266: 
0267: .sa-profile-wrap .btn-primary:hover {
0268:     background: rgba(255, 211, 154, 0.18);
0269:     border-color: rgba(255, 211, 154, 0.58);
0270:     color: #fff7ec;
```
Linija 273 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0270:     color: #fff7ec;
0271: }
0272: 
0273: .sa-profile-wrap .btn-outline-primary {
0274:     color: #ffd39a;
0275:     border-color: rgba(255, 211, 154, 0.48);
0276: }
```
Linija 278 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0275:     border-color: rgba(255, 211, 154, 0.48);
0276: }
0277: 
0278: .sa-profile-wrap .btn-outline-primary:hover {
0279:     background: rgba(255, 211, 154, 0.16);
0280:     color: #fff6ea;
0281: }
```
Linija 402 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0399: }
0400: 
0401: .blog-action-outline,
0402: .btn-outline-light,
0403: .sa-theme .btn-outline-secondary {
0404:     border-color: rgba(255, 211, 154, 0.50) !important;
0405:     color: #ffd39a !important;
```
Linija 403 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0400: 
0401: .blog-action-outline,
0402: .btn-outline-light,
0403: .sa-theme .btn-outline-secondary {
0404:     border-color: rgba(255, 211, 154, 0.50) !important;
0405:     color: #ffd39a !important;
0406:     background: transparent !important;
```
Linija 410 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0407: }
0408: 
0409: .blog-action-outline:hover,
0410: .btn-outline-light:hover,
0411: .sa-theme .btn-outline-secondary:hover {
0412:     background: rgba(255, 211, 154, 0.18) !important;
0413:     color: #fff6ea !important;
```
Linija 411 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0408: 
0409: .blog-action-outline:hover,
0410: .btn-outline-light:hover,
0411: .sa-theme .btn-outline-secondary:hover {
0412:     background: rgba(255, 211, 154, 0.18) !important;
0413:     color: #fff6ea !important;
0414:     box-shadow: 0 0 8px rgba(255, 211, 154, 0.18);
```
Linija 425 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0422: }
0423: 
0424: .comment-row textarea,
0425: .comment-row .form-control {
0426:     flex: 1;
0427:     background: rgba(255, 244, 229, 0.10) !important;
0428:     color: #fff2e2 !important;
```
Linija 436 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0433: }
0434: 
0435: .comment-row textarea:focus,
0436: .comment-row .form-control:focus {
0437:     border-color: rgba(255, 211, 154, 0.42) !important;
0438:     box-shadow: 0 0 0 0.2rem rgba(255, 211, 154, 0.10) !important;
0439: }
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `staza_prema_vrhovima`

- Datoteka: `blog\templates\blog\designs\staza_prema_vrhovima.html`
- Grupa: `posebni`
- Hitovi: **12**
- Rizični hitovi: **12**

Linija 31 — `navbar` — dira navbar:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(28, 20, 13, 0.82) !important;
```
Linija 39 — `navbar` — dira navbar:
```txt
0036:     backdrop-filter: blur(6px);
0037: }
0038: 
0039: nav.navbar .dropdown-menu {
0040:     z-index: 4100 !important;
0041: }
0042: 
```
Linija 220 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0217:     box-shadow: 0 8px 18px rgba(0, 0, 0, 0.24);
0218: }
0219: 
0220: .spv-profile-wrap .btn-primary {
0221:     background: #d9b06f;
0222:     border-color: #d9b06f;
0223:     color: #2f2419;
```
Linija 226 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0223:     color: #2f2419;
0224: }
0225: 
0226: .spv-profile-wrap .btn-primary:hover {
0227:     background: #f0c786;
0228:     border-color: #f0c786;
0229:     color: #24160d;
```
Linija 232 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0229:     color: #24160d;
0230: }
0231: 
0232: .spv-profile-wrap .btn-outline-primary {
0233:     color: #ffd89c;
0234:     border-color: #ffd89c;
0235: }
```
Linija 237 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0234:     border-color: #ffd89c;
0235: }
0236: 
0237: .spv-profile-wrap .btn-outline-primary:hover {
0238:     background: #ffd89c;
0239:     color: #2f2419;
0240: }
```
Linija 363 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0360: }
0361: 
0362: .blog-action-outline,
0363: .btn-outline-light {
0364:     border-color: #ffd89c !important;
0365:     color: #ffd89c !important;
0366:     background: transparent !important;
```
Linija 370 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0367: }
0368: 
0369: .blog-action-outline:hover,
0370: .btn-outline-light:hover {
0371:     background: rgba(255, 216, 156, 0.16) !important;
0372:     color: #fff7ea !important;
0373:     box-shadow: 0 0 10px rgba(255,216,156,0.12);
```
Linija 384 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0381: }
0382: 
0383: .comment-row textarea,
0384: .comment-row .form-control {
0385:     flex: 1;
0386:     background: rgba(255,255,255,0.05) !important;
0387:     color: #f2e3ce !important;
```
Linija 395 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0392: }
0393: 
0394: .comment-row textarea:focus,
0395: .comment-row .form-control:focus {
0396:     border-color: rgba(255,216,156,0.34) !important;
0397:     box-shadow: 0 0 0 0.2rem rgba(255,216,156,0.08) !important;
0398: }
```
Linija 401 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0398: }
0399: 
0400: .comment-row textarea::placeholder,
0401: .comment-row .form-control::placeholder {
0402:     color: #e8d2ab !important;
0403: }
0404: 
```
Linija 528 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0525:         align-items: stretch;
0526:     }
0527: 
0528:     .comment-row .btn {
0529:         width: 100%;
0530:     }
0531: }
```

### `studio`

- Datoteka: `blog\templates\blog\designs\studio.html`
- Grupa: `posebni_hero`
- Hitovi: **9**
- Rizični hitovi: **9**

Linija 29 — `button_selector` — genericki button selector:
```txt
0026:                     {% if not is_restricted %}
0027:                         <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0028:                             {% csrf_token %}
0029:                             <button type="submit" class="btn {% if is_following %}btn-outline-primary{% else %}btn-primary{% endif %} btn-sm">
0030:                                 {% if is_following %}Pratiš{% else %}Prati{% endif %}
0031:                             </button>
0032:                         </form>
```
Linija 50 — `button_selector` — genericki button selector:
```txt
0047:                                 <li>
0048:                                     <form method="post" action="{% url 'unfollow_user' blog.username %}" class="m-0">
0049:                                         {% csrf_token %}
0050:                                         <button type="submit" class="dropdown-item">Prestani pratiti</button>
0051:                                     </form>
0052:                                 </li>
0053:                             {% else %}
```
Linija 57 — `button_selector` — genericki button selector:
```txt
0054:                                 <li>
0055:                                     <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0056:                                         {% csrf_token %}
0057:                                         <button type="submit" class="dropdown-item" {% if is_restricted %}disabled{% endif %}>Prati korisnika</button>
0058:                                     </form>
0059:                                 </li>
0060:                             {% endif %}
```
Linija 65 — `button_selector` — genericki button selector:
```txt
0062:                             <li>
0063:                                 <form method="post" action="{% url 'restrict_user' blog.username %}" class="m-0">
0064:                                     {% csrf_token %}
0065:                                     <button type="submit" class="dropdown-item">Ograniči korisnika</button>
0066:                                 </form>
0067:                             </li>
0068: 
```
Linija 74 — `button_selector` — genericki button selector:
```txt
0071:                             <li>
0072:                                 <form method="post" action="{% url 'block_user' blog.username %}" class="m-0">
0073:                                     {% csrf_token %}
0074:                                     <button type="submit" class="dropdown-item text-danger">Blokiraj korisnika</button>
0075:                                 </form>
0076:                             </li>
0077:                         </ul>
```
Linija 346 — `navbar` — dira navbar:
```txt
0343:     z-index: 9999;
0344: }
0345: 
0346: nav.navbar {
0347:     position: relative;
0348:     z-index: 5000 !important;
0349: }
```
Linija 351 — `navbar` — dira navbar:
```txt
0348:     z-index: 5000 !important;
0349: }
0350: 
0351: nav.navbar .dropdown-menu {
0352:     z-index: 5100 !important;
0353: }
0354: 
```
Linija 594 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0591:     border: 1px solid var(--soho-content-border);
0592: }
0593: 
0594: textarea.form-control {
0595:     background: #fff !important;
0596:     color: var(--soho-text) !important;
0597:     border: 1px solid var(--soho-content-border) !important;
```
Linija 600 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0597:     border: 1px solid var(--soho-content-border) !important;
0598: }
0599: 
0600: textarea.form-control:focus {
0601:     box-shadow: 0 0 0 0.12rem rgba(182, 122, 45, 0.18) !important;
0602:     border-color: #c79554 !important;
0603: }
```

### `sumska_svjetlost`

- Datoteka: `blog\templates\blog\designs\sumska_svjetlost.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```
Linija 417 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0414:     color: #5d6957;
0415: }
0416: 
0417: textarea.form-control,
0418: input.form-control,
0419: select.form-select {
0420:     background: rgba(248, 252, 243, 0.62) !important;
```
Linija 418 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0415: }
0416: 
0417: textarea.form-control,
0418: input.form-control,
0419: select.form-select {
0420:     background: rgba(248, 252, 243, 0.62) !important;
0421:     color: #53614d !important;
```
Linija 418 — `input_selector` — genericki input selector:
```txt
0415: }
0416: 
0417: textarea.form-control,
0418: input.form-control,
0419: select.form-select {
0420:     background: rgba(248, 252, 243, 0.62) !important;
0421:     color: #53614d !important;
```
Linija 426 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0423:     box-shadow: none !important;
0424: }
0425: 
0426: textarea.form-control::placeholder,
0427: input.form-control::placeholder {
0428:     color: rgba(93, 105, 87, 0.48) !important;
0429: }
```
Linija 427 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0424: }
0425: 
0426: textarea.form-control::placeholder,
0427: input.form-control::placeholder {
0428:     color: rgba(93, 105, 87, 0.48) !important;
0429: }
0430: 
```
Linija 427 — `input_selector` — genericki input selector:
```txt
0424: }
0425: 
0426: textarea.form-control::placeholder,
0427: input.form-control::placeholder {
0428:     color: rgba(93, 105, 87, 0.48) !important;
0429: }
0430: 
```
Linija 431 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0428:     color: rgba(93, 105, 87, 0.48) !important;
0429: }
0430: 
0431: textarea.form-control:focus,
0432: input.form-control:focus,
0433: select.form-select:focus {
0434:     border-color: rgba(137, 171, 112, 0.56) !important;
```
Linija 432 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0429: }
0430: 
0431: textarea.form-control:focus,
0432: input.form-control:focus,
0433: select.form-select:focus {
0434:     border-color: rgba(137, 171, 112, 0.56) !important;
0435:     box-shadow: none !important;
```
Linija 432 — `input_selector` — genericki input selector:
```txt
0429: }
0430: 
0431: textarea.form-control:focus,
0432: input.form-control:focus,
0433: select.form-select:focus {
0434:     border-color: rgba(137, 171, 112, 0.56) !important;
0435:     box-shadow: none !important;
```
Linija 439 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0436: }
0437: 
0438: .blog-action-outline,
0439: .btn-outline-light {
0440:     border-color: rgba(137, 171, 112, 0.42) !important;
0441:     color: #5d6957 !important;
0442:     background: rgba(248, 252, 243, 0.42) !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `svemirski_horizont`

- Datoteka: `blog\templates\blog\designs\svemirski_horizont.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```
Linija 406 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0403:     color: #dbe7ff;
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
```
Linija 407 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
0410:     color: #eaf2ff !important;
```
Linija 407 — `input_selector` — genericki input selector:
```txt
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
0410:     color: #eaf2ff !important;
```
Linija 415 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0412:     box-shadow: none !important;
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(216, 228, 255, 0.48) !important;
0418: }
```
Linija 416 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(216, 228, 255, 0.48) !important;
0418: }
0419: 
```
Linija 416 — `input_selector` — genericki input selector:
```txt
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(216, 228, 255, 0.48) !important;
0418: }
0419: 
```
Linija 420 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0417:     color: rgba(216, 228, 255, 0.48) !important;
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(180, 210, 255, 0.42) !important;
```
Linija 421 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(180, 210, 255, 0.42) !important;
0424:     box-shadow: none !important;
```
Linija 421 — `input_selector` — genericki input selector:
```txt
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(180, 210, 255, 0.42) !important;
0424:     box-shadow: none !important;
```
Linija 428 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0425: }
0426: 
0427: .blog-action-outline,
0428: .btn-outline-light {
0429:     border-color: rgba(180, 210, 255, 0.36) !important;
0430:     color: #eef5ff !important;
0431:     background: transparent !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `vecer_uz_jezero`

- Datoteka: `blog\templates\blog\designs\vecer_uz_jezero.html`
- Grupa: `posebni`
- Hitovi: **12**
- Rizični hitovi: **12**

Linija 31 — `navbar` — dira navbar:
```txt
0028:     display: none;
0029: }
0030: 
0031: nav.navbar {
0032:     position: relative;
0033:     z-index: 4000 !important;
0034:     background: rgba(30, 13, 12, 0.82) !important;
```
Linija 38 — `navbar` — dira navbar:
```txt
0035:     border-bottom: 1px solid rgba(255, 228, 204, 0.10);
0036: }
0037: 
0038: nav.navbar .dropdown-menu {
0039:     z-index: 4100 !important;
0040: }
0041: 
```
Linija 220 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0217:     box-shadow: 0 8px 18px rgba(0, 0, 0, 0.24);
0218: }
0219: 
0220: .vj-profile-wrap .btn-primary {
0221:     background: #f3c3a0;
0222:     border-color: #f3c3a0;
0223:     color: #341c18;
```
Linija 226 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0223:     color: #341c18;
0224: }
0225: 
0226: .vj-profile-wrap .btn-primary:hover {
0227:     background: #ffd1af;
0228:     border-color: #ffd1af;
0229:     color: #291411;
```
Linija 232 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0229:     color: #291411;
0230: }
0231: 
0232: .vj-profile-wrap .btn-outline-primary {
0233:     color: #ffd6bd;
0234:     border-color: #ffd6bd;
0235: }
```
Linija 237 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0234:     border-color: #ffd6bd;
0235: }
0236: 
0237: .vj-profile-wrap .btn-outline-primary:hover {
0238:     background: #ffd6bd;
0239:     color: #341c18;
0240: }
```
Linija 399 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0396: }
0397: 
0398: .blog-action-outline,
0399: .btn-outline-light {
0400:     border-color: #ffd6bd !important;
0401:     color: #ffd6bd !important;
0402:     background: transparent !important;
```
Linija 406 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0403: }
0404: 
0405: .blog-action-outline:hover,
0406: .btn-outline-light:hover {
0407:     background: rgba(255, 214, 189, 0.16) !important;
0408:     color: #fff7f1 !important;
0409:     box-shadow: 0 0 10px rgba(255,214,189,0.12);
```
Linija 420 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0417: }
0418: 
0419: .comment-row textarea,
0420: .comment-row .form-control {
0421:     flex: 1;
0422:     background: rgba(255,255,255,0.08) !important;
0423:     color: #f8e6dc !important;
```
Linija 431 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0428: }
0429: 
0430: .comment-row textarea:focus,
0431: .comment-row .form-control:focus {
0432:     border-color: rgba(255,214,189,0.34) !important;
0433:     box-shadow: 0 0 0 0.2rem rgba(255,214,189,0.08) !important;
0434: }
```
Linija 437 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0434: }
0435: 
0436: .comment-row textarea::placeholder,
0437: .comment-row .form-control::placeholder {
0438:     color: #f1cbbb !important;
0439: }
0440: 
```
Linija 569 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0566:         align-items: stretch;
0567:     }
0568: 
0569:     .comment-row .btn {
0570:         width: 100%;
0571:     }
0572: }
```

### `vecer_zaljubljenih`

- Datoteka: `blog\templates\blog\designs\vecer_zaljubljenih.html`
- Grupa: `posebni`
- Hitovi: **12**
- Rizični hitovi: **12**

Linija 42 — `navbar` — dira navbar:
```txt
0039:     display: none;
0040: }
0041: 
0042: nav.navbar {
0043:     position: relative;
0044:     z-index: 4000 !important;
0045:     background: rgba(32, 7, 6, 0.42) !important;
```
Linija 50 — `navbar` — dira navbar:
```txt
0047:     border-bottom: 1px solid rgba(255, 226, 206, 0.10);
0048: }
0049: 
0050: nav.navbar .dropdown-menu {
0051:     z-index: 4100 !important;
0052: }
0053: 
```
Linija 234 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0231:     box-shadow: 0 8px 18px rgba(0, 0, 0, 0.24);
0232: }
0233: 
0234: .vz-profile-wrap .btn-primary {
0235:     background: #ffb68d;
0236:     border-color: #ffb68d;
0237:     color: #31110d;
```
Linija 240 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0237:     color: #31110d;
0238: }
0239: 
0240: .vz-profile-wrap .btn-primary:hover {
0241:     background: #ffc59e;
0242:     border-color: #ffc59e;
0243:     color: #26100d;
```
Linija 246 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0243:     color: #26100d;
0244: }
0245: 
0246: .vz-profile-wrap .btn-outline-primary {
0247:     color: #ffbf96;
0248:     border-color: #ffbf96;
0249: }
```
Linija 251 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0248:     border-color: #ffbf96;
0249: }
0250: 
0251: .vz-profile-wrap .btn-outline-primary:hover {
0252:     background: #ffbf96;
0253:     color: #31110d;
0254: }
```
Linija 413 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0410: }
0411: 
0412: .blog-action-outline,
0413: .btn-outline-light {
0414:     border-color: #ffbf96 !important;
0415:     color: #ffbf96 !important;
0416:     background: transparent !important;
```
Linija 420 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0417: }
0418: 
0419: .blog-action-outline:hover,
0420: .btn-outline-light:hover {
0421:     background: #ffbf96 !important;
0422:     color: #31110d !important;
0423:     box-shadow: 0 0 10px rgba(255,191,150,0.12);
```
Linija 434 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0431: }
0432: 
0433: .comment-row textarea,
0434: .comment-row .form-control {
0435:     flex: 1;
0436:     background: rgba(255,255,255,0.06) !important;
0437:     color: #f6ddd2 !important;
```
Linija 445 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0442: }
0443: 
0444: .comment-row textarea:focus,
0445: .comment-row .form-control:focus {
0446:     border-color: rgba(255, 191, 150, 0.34) !important;
0447:     box-shadow: 0 0 0 0.2rem rgba(255, 191, 150, 0.06) !important;
0448: }
```
Linija 451 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0448: }
0449: 
0450: .comment-row textarea::placeholder,
0451: .comment-row .form-control::placeholder {
0452:     color: #e0af99 !important;
0453: }
0454: 
```
Linija 583 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0580:         align-items: stretch;
0581:     }
0582: 
0583:     .comment-row .btn {
0584:         width: 100%;
0585:     }
0586: }
```

### `vodopad_u_magli`

- Datoteka: `blog\templates\blog\designs\vodopad_u_magli.html`
- Grupa: `zajednicki_layout`
- Hitovi: **6**
- Rizični hitovi: **6**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```
Linija 290 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0287:     padding: 10px 44px 10px 12px;
0288: }
0289: 
0290: textarea.form-control {
0291:     background: rgba(255,255,255,0.30) !important;
0292:     color: #465042 !important;
0293:     border: 1px solid rgba(124,137,124,0.28) !important;
```
Linija 297 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0294:     border-radius: 12px;
0295: }
0296: 
0297: textarea.form-control:focus {
0298:     background: rgba(255,255,255,0.36) !important;
0299:     color: #465042 !important;
0300:     border-color: rgba(113,130,112,0.45) !important;
```
Linija 309 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0306: }
0307: 
0308: .blog-action-outline,
0309: .btn-outline-light {
0310:     border-color: rgba(113,130,112,0.36) !important;
0311:     color: #4f5d4a !important;
0312:     background: rgba(255,255,255,0.16) !important;
```
Linija 316 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0313: }
0314: 
0315: .blog-action-outline:hover,
0316: .btn-outline-light:hover {
0317:     background-color: rgba(221,230,214,0.38) !important;
0318:     color: #364034 !important;
0319: }
```

### `zlatni_horizont`

- Datoteka: `blog\templates\blog\designs\zlatni_horizont.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 43 — `navbar` — dira navbar:
```txt
0040:     background-size: 100% 100%, 100% auto;
0041: }
0042: 
0043: nav.navbar {
0044:     position: relative;
0045:     z-index: 4000 !important;
0046: }
```
Linija 48 — `navbar` — dira navbar:
```txt
0045:     z-index: 4000 !important;
0046: }
0047: 
0048: nav.navbar .dropdown-menu {
0049:     z-index: 4100 !important;
0050: }
0051: 
```
Linija 406 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0403:     color: #f6e1cd;
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
```
Linija 407 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
0410:     color: #fff0df !important;
```
Linija 407 — `input_selector` — genericki input selector:
```txt
0404: }
0405: 
0406: textarea.form-control,
0407: input.form-control,
0408: select.form-select {
0409:     background: transparent !important;
0410:     color: #fff0df !important;
```
Linija 415 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0412:     box-shadow: none !important;
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(240, 214, 189, 0.48) !important;
0418: }
```
Linija 416 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(240, 214, 189, 0.48) !important;
0418: }
0419: 
```
Linija 416 — `input_selector` — genericki input selector:
```txt
0413: }
0414: 
0415: textarea.form-control::placeholder,
0416: input.form-control::placeholder {
0417:     color: rgba(240, 214, 189, 0.48) !important;
0418: }
0419: 
```
Linija 420 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0417:     color: rgba(240, 214, 189, 0.48) !important;
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(255, 176, 96, 0.42) !important;
```
Linija 421 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(255, 176, 96, 0.42) !important;
0424:     box-shadow: none !important;
```
Linija 421 — `input_selector` — genericki input selector:
```txt
0418: }
0419: 
0420: textarea.form-control:focus,
0421: input.form-control:focus,
0422: select.form-select:focus {
0423:     border-color: rgba(255, 176, 96, 0.42) !important;
0424:     box-shadow: none !important;
```
Linija 428 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0425: }
0426: 
0427: .blog-action-outline,
0428: .btn-outline-light {
0429:     border-color: rgba(255, 176, 96, 0.36) !important;
0430:     color: #fff1e3 !important;
0431:     background: transparent !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

### `zlatno_polje`

- Datoteka: `blog\templates\blog\designs\zlatno_polje.html`
- Grupa: `zajednicki_layout`
- Hitovi: **13**
- Rizični hitovi: **13**

Linija 46 — `navbar` — dira navbar:
```txt
0043:     background-size: 100% 100%, 100% auto;
0044: }
0045: 
0046: nav.navbar {
0047:     position: relative;
0048:     z-index: 4000 !important;
0049: }
```
Linija 51 — `navbar` — dira navbar:
```txt
0048:     z-index: 4000 !important;
0049: }
0050: 
0051: nav.navbar .dropdown-menu {
0052:     z-index: 4100 !important;
0053: }
0054: 
```
Linija 426 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0423:     color: #5f3d10;
0424: }
0425: 
0426: textarea.form-control,
0427: input.form-control,
0428: select.form-select {
0429:     background: transparent !important;
```
Linija 427 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0424: }
0425: 
0426: textarea.form-control,
0427: input.form-control,
0428: select.form-select {
0429:     background: transparent !important;
0430:     color: #4b2d05 !important;
```
Linija 427 — `input_selector` — genericki input selector:
```txt
0424: }
0425: 
0426: textarea.form-control,
0427: input.form-control,
0428: select.form-select {
0429:     background: transparent !important;
0430:     color: #4b2d05 !important;
```
Linija 435 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0432:     box-shadow: none !important;
0433: }
0434: 
0435: textarea.form-control::placeholder,
0436: input.form-control::placeholder {
0437:     color: rgba(109, 71, 16, 0.46) !important;
0438: }
```
Linija 436 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0433: }
0434: 
0435: textarea.form-control::placeholder,
0436: input.form-control::placeholder {
0437:     color: rgba(109, 71, 16, 0.46) !important;
0438: }
0439: 
```
Linija 436 — `input_selector` — genericki input selector:
```txt
0433: }
0434: 
0435: textarea.form-control::placeholder,
0436: input.form-control::placeholder {
0437:     color: rgba(109, 71, 16, 0.46) !important;
0438: }
0439: 
```
Linija 440 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0437:     color: rgba(109, 71, 16, 0.46) !important;
0438: }
0439: 
0440: textarea.form-control:focus,
0441: input.form-control:focus,
0442: select.form-select:focus {
0443:     border-color: rgba(146, 92, 17, 0.42) !important;
```
Linija 441 — `form_control` — moze dirati Bootstrap input, ukljucujuci trazilicu:
```txt
0438: }
0439: 
0440: textarea.form-control:focus,
0441: input.form-control:focus,
0442: select.form-select:focus {
0443:     border-color: rgba(146, 92, 17, 0.42) !important;
0444:     box-shadow: none !important;
```
Linija 441 — `input_selector` — genericki input selector:
```txt
0438: }
0439: 
0440: textarea.form-control:focus,
0441: input.form-control:focus,
0442: select.form-select:focus {
0443:     border-color: rgba(146, 92, 17, 0.42) !important;
0444:     box-shadow: none !important;
```
Linija 448 — `btn_selector` — moze dirati gumbe u navbaru:
```txt
0445: }
0446: 
0447: .blog-action-outline,
0448: .btn-outline-light {
0449:     border-color: rgba(146, 92, 17, 0.34) !important;
0450:     color: #4b2d05 !important;
0451:     background: transparent !important;
```
_Još 1 hitova prikazano je u JSON dokumentu._

## Preporuka

1. Ne popravljati tražilicu po dizajnu.
2. U dizajnima ukloniti ili ograničiti generičke selektore koji pogađaju navbar: `.form-control`, `.input-group`, `input`, `button`, `.btn`, `.navbar`.
3. Globalna tražilica treba biti definirana u `blog/base.html` ili glavnom globalnom CSS-u.
4. Ako dizajn treba stilizirati forme unutar bloga, selektori moraju biti ograničeni na blog layout, npr. `.blog-main-layout-row textarea.form-control`, a ne globalno `.form-control`.