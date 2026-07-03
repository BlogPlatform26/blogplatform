# Phase 18 — audit globalnog navbar lock sloja

Izrađeno: 2026-07-03 19:57:28

## Cilj

Pregledati `blog/templates/blog/base.html` i pronaći gdje se nalaze globalni navbar, tražilica, obavijesti i postojeći CSS koji ih može zaključati. Ovo je read-only audit i ne mijenja aplikaciju.

## Zašto ovo radimo

Masovno mijenjanje dizajna se pokazalo rizično. Bolji smjer je prvo zaštititi globalni navbar tako da dizajni bloga ne mogu promijeniti tražilicu, badge obavijesti, dropdown ili gumbe u navbaru.

## Sažetak

- File: `C:\Users\mario\blogplatform\blog\templates\blog\base.html`
- Broj linija u base.html: **3534**
- Ukupno hitova vezanih za navbar/search/dropdown/badge/form: **48**
- CSS hitova unutar `<style>` blokova: **23**

## Važni HTML dijelovi

### `navbarSearchInput` oko linije 1266

```txt
1258:         </button>
1259: 
1260:         <!-- ✅ Pretraga unutar navbara (inline) -->
1261:         <div class="collapse ms-2" id="navbarSearchInline">
1262:             <form class="d-flex align-items-center"
1263:                   method="GET"
1264:                   action="{% url 'search' %}">
1265:                 <div class="input-group input-group-sm" style="width: 320px;">
1266:                     <input id="navbarSearchInput"
1267:                            class="form-control"
1268:                            type="search"
1269:                            name="q"
1270:                            placeholder="Pretraži..."
1271:                            value="{{ request.GET.q|default:'' }}">
1272: 
1273:                     <button class="btn btn-outline-light" type="submit" title="Pretraži">
1274:                         <i class="bi bi-search"></i>
```

### `navbarSearchInline` oko linije 1253

```txt
1245:                  style="height:44px;">
1246:         </a>
1247: 
1248:         <!-- ✅ Ikona za pretragu -->
1249:         <button id="searchToggleBtn"
1250:                 class="btn btn-outline-light btn-sm ms-2"
1251:                 type="button"
1252:                 data-bs-toggle="collapse"
1253:                 data-bs-target="#navbarSearchInline"
1254:                 aria-expanded="false"
1255:                 aria-controls="navbarSearchInline"
1256:                 title="Pretraga">
1257:             <i class="bi bi-search"></i>
1258:         </button>
1259: 
1260:         <!-- ✅ Pretraga unutar navbara (inline) -->
1261:         <div class="collapse ms-2" id="navbarSearchInline">
```

### `searchToggleBtn` oko linije 1249

```txt
1241: 
1242:         <a class="navbar-brand" href="{% url 'home' %}">
1243:             <img src="{% static 'images/logo.svg' %}"
1244:                  alt="Logo"
1245:                  style="height:44px;">
1246:         </a>
1247: 
1248:         <!-- ✅ Ikona za pretragu -->
1249:         <button id="searchToggleBtn"
1250:                 class="btn btn-outline-light btn-sm ms-2"
1251:                 type="button"
1252:                 data-bs-toggle="collapse"
1253:                 data-bs-target="#navbarSearchInline"
1254:                 aria-expanded="false"
1255:                 aria-controls="navbarSearchInline"
1256:                 title="Pretraga">
1257:             <i class="bi bi-search"></i>
```

### `notif-badge` oko linije 67

```txt
0059:     }
0060:     .nav-avatar{
0061:         width: 28px;
0062:         height: 28px;
0063:         border-radius: 50%;
0064:         object-fit: cover;
0065:     }
0066:     .nav-user-text{ line-height: 1; }
0067:     .notif-badge{ font-size: 11px; padding: 3px 6px; }
0068:     .notif-actions-bar{
0069:         position: sticky;
0070:         top: 0;
0071:         z-index: 5;
0072:         background: #fff;
0073:     }
0074:     .notif-actions-bar .btn-link:disabled{
0075:         color: rgba(0,0,0,0.35) !important;
```

### `navbar-brand` oko linije 1242

```txt
1234:         </button>
1235:     </form>
1236: </div>
1237: {% endif %}
1238: 
1239: <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
1240:     <div class="container-fluid position-relative">
1241: 
1242:         <a class="navbar-brand" href="{% url 'home' %}">
1243:             <img src="{% static 'images/logo.svg' %}"
1244:                  alt="Logo"
1245:                  style="height:44px;">
1246:         </a>
1247: 
1248:         <!-- ✅ Ikona za pretragu -->
1249:         <button id="searchToggleBtn"
1250:                 class="btn btn-outline-light btn-sm ms-2"
```

### `<nav` oko linije 1239

```txt
1231:         <button type="submit"
1232:                 style="background:none; border:0; padding:0; color:#d9480f; font-weight:600; text-decoration:underline; cursor:pointer;">
1233:             ponovno pošaljite mail.
1234:         </button>
1235:     </form>
1236: </div>
1237: {% endif %}
1238: 
1239: <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
1240:     <div class="container-fluid position-relative">
1241: 
1242:         <a class="navbar-brand" href="{% url 'home' %}">
1243:             <img src="{% static 'images/logo.svg' %}"
1244:                  alt="Logo"
1245:                  style="height:44px;">
1246:         </a>
1247: 
```

## CSS hitovi u base.html

- Linija 67 — `notif-badge`
```txt
0064:         object-fit: cover;
0065:     }
0066:     .nav-user-text{ line-height: 1; }
0067:     .notif-badge{ font-size: 11px; padding: 3px 6px; }
0068:     .notif-actions-bar{
0069:         position: sticky;
0070:         top: 0;
```
- Linija 74 — `\.btn`
```txt
0071:         z-index: 5;
0072:         background: #fff;
0073:     }
0074:     .notif-actions-bar .btn-link:disabled{
0075:         color: rgba(0,0,0,0.35) !important;
0076:         pointer-events: none;
0077:     }
```
- Linija 242 — `nav\.navbar`
```txt
0239:         display:block;
0240:         background:transparent !important;
0241:     }
0242:     nav.navbar{
0243:         position:relative;
0244:         z-index:5000 !important;
0245:     }
```
- Linija 246 — `nav\.navbar`
```txt
0243:         position:relative;
0244:         z-index:5000 !important;
0245:     }
0246:     nav.navbar .dropdown-menu{
0247:         z-index:5100 !important;
0248:     }
0249: 
```
- Linija 304 — `input\[type=.?search`
```txt
0301:     .blog-cursor-theme:not(.blog-cursor-external-style) input[type="text"],
0302:     .blog-cursor-theme:not(.blog-cursor-external-style) input[type="email"],
0303:     .blog-cursor-theme:not(.blog-cursor-external-style) input[type="password"],
0304:     .blog-cursor-theme:not(.blog-cursor-external-style) input[type="search"],
0305:     .blog-cursor-theme:not(.blog-cursor-external-style) input[type="number"],
0306:     .blog-cursor-theme:not(.blog-cursor-external-style) textarea,
0307:     .blog-cursor-theme:not(.blog-cursor-external-style) [contenteditable="true"]{
```
- Linija 316 — `\.btn`
```txt
0313:     }
0314:     .blog-cursor-sparkle a,
0315:     .blog-cursor-sparkle button,
0316:     .blog-cursor-sparkle .btn,
0317:     .blog-cursor-sparkle [role="button"],
0318:     .blog-cursor-sparkle summary,
0319:     .blog-cursor-sparkle label[for],
```
- Linija 333 — `\.btn`
```txt
0330:     }
0331:     .blog-cursor-heart a,
0332:     .blog-cursor-heart button,
0333:     .blog-cursor-heart .btn,
0334:     .blog-cursor-heart [role="button"],
0335:     .blog-cursor-heart summary,
0336:     .blog-cursor-heart label[for],
```
- Linija 350 — `\.btn`
```txt
0347:     }
0348:     .blog-cursor-moon a,
0349:     .blog-cursor-moon button,
0350:     .blog-cursor-moon .btn,
0351:     .blog-cursor-moon [role="button"],
0352:     .blog-cursor-moon summary,
0353:     .blog-cursor-moon label[for],
```
- Linija 367 — `\.btn`
```txt
0364:     }
0365:     .blog-cursor-diamond a,
0366:     .blog-cursor-diamond button,
0367:     .blog-cursor-diamond .btn,
0368:     .blog-cursor-diamond [role="button"],
0369:     .blog-cursor-diamond summary,
0370:     .blog-cursor-diamond label[for],
```
- Linija 384 — `\.btn`
```txt
0381:     }
0382:     .blog-cursor-neon a,
0383:     .blog-cursor-neon button,
0384:     .blog-cursor-neon .btn,
0385:     .blog-cursor-neon [role="button"],
0386:     .blog-cursor-neon summary,
0387:     .blog-cursor-neon label[for],
```
- Linija 402 — `\.btn`
```txt
0399:     }
0400:     .blog-cursor-rose a,
0401:     .blog-cursor-rose button,
0402:     .blog-cursor-rose .btn,
0403:     .blog-cursor-rose [role="button"],
0404:     .blog-cursor-rose summary,
0405:     .blog-cursor-rose label[for],
```
- Linija 419 — `\.btn`
```txt
0416:     }
0417:     .blog-cursor-butterfly a,
0418:     .blog-cursor-butterfly button,
0419:     .blog-cursor-butterfly .btn,
0420:     .blog-cursor-butterfly [role="button"],
0421:     .blog-cursor-butterfly summary,
0422:     .blog-cursor-butterfly label[for],
```
- Linija 436 — `\.btn`
```txt
0433:     }
0434:     .blog-cursor-leaf a,
0435:     .blog-cursor-leaf button,
0436:     .blog-cursor-leaf .btn,
0437:     .blog-cursor-leaf [role="button"],
0438:     .blog-cursor-leaf summary,
0439:     .blog-cursor-leaf label[for],
```
- Linija 453 — `\.btn`
```txt
0450:     }
0451:     .blog-cursor-sun a,
0452:     .blog-cursor-sun button,
0453:     .blog-cursor-sun .btn,
0454:     .blog-cursor-sun [role="button"],
0455:     .blog-cursor-sun summary,
0456:     .blog-cursor-sun label[for],
```
- Linija 471 — `\.btn`
```txt
0468:     }
0469:     .blog-cursor-flame a,
0470:     .blog-cursor-flame button,
0471:     .blog-cursor-flame .btn,
0472:     .blog-cursor-flame [role="button"],
0473:     .blog-cursor-flame summary,
0474:     .blog-cursor-flame label[for],
```
- Linija 489 — `\.btn`
```txt
0486:     }
0487:     .blog-cursor-crown a,
0488:     .blog-cursor-crown button,
0489:     .blog-cursor-crown .btn,
0490:     .blog-cursor-crown [role="button"],
0491:     .blog-cursor-crown summary,
0492:     .blog-cursor-crown label[for],
```
- Linija 507 — `\.btn`
```txt
0504:     }
0505:     .blog-cursor-crystal a,
0506:     .blog-cursor-crystal button,
0507:     .blog-cursor-crystal .btn,
0508:     .blog-cursor-crystal [role="button"],
0509:     .blog-cursor-crystal summary,
0510:     .blog-cursor-crystal label[for],
```
- Linija 525 — `\.btn`
```txt
0522:     }
0523:     .blog-cursor-paw a,
0524:     .blog-cursor-paw button,
0525:     .blog-cursor-paw .btn,
0526:     .blog-cursor-paw [role="button"],
0527:     .blog-cursor-paw summary,
0528:     .blog-cursor-paw label[for],
```
- Linija 543 — `\.btn`
```txt
0540:     }
0541:     .blog-cursor-droplet a,
0542:     .blog-cursor-droplet button,
0543:     .blog-cursor-droplet .btn,
0544:     .blog-cursor-droplet [role="button"],
0545:     .blog-cursor-droplet summary,
0546:     .blog-cursor-droplet label[for],
```
- Linija 560 — `\.btn`
```txt
0557:     }
0558:     .blog-cursor-sword a,
0559:     .blog-cursor-sword button,
0560:     .blog-cursor-sword .btn,
0561:     .blog-cursor-sword [role="button"],
0562:     .blog-cursor-sword summary,
0563:     .blog-cursor-sword label[for],
```
- Linija 577 — `\.btn`
```txt
0574:     }
0575:     .blog-cursor-skeleton_hand a,
0576:     .blog-cursor-skeleton_hand button,
0577:     .blog-cursor-skeleton_hand .btn,
0578:     .blog-cursor-skeleton_hand [role="button"],
0579:     .blog-cursor-skeleton_hand summary,
0580:     .blog-cursor-skeleton_hand label[for],
```
- Linija 899 — `\.btn`
```txt
0896:     }
0897:     .blog-cursor-theme:not(.blog-cursor-external-style) a,
0898:     .blog-cursor-theme:not(.blog-cursor-external-style) button,
0899:     .blog-cursor-theme:not(.blog-cursor-external-style) .btn,
0900:     .blog-cursor-theme:not(.blog-cursor-external-style) [role="button"],
0901:     .blog-cursor-theme:not(.blog-cursor-external-style) summary,
0902:     .blog-cursor-theme:not(.blog-cursor-external-style) label[for],
```
- Linija 1018 — `\.form-control`
```txt
1015:     
1016: 
1017:     /* PRIKAŽI / SAKRIJ LOZINKU */
1018:     .password-toggle-group .form-control{
1019:         border-top-right-radius: 0;
1020:         border-bottom-right-radius: 0;
1021:     }
```

## Preporuka za sljedeći korak

1. Ne dirati dizajne masovno.
2. Dodati ili pojačati globalni CSS samo za navbar, ali vezan uz konkretne navbar selektore/ID-eve.
3. Zaključati izgled `#navbarSearchInput`, `#searchToggleBtn`, `.notif-badge`, navbar dropdownova i osnovnih navbar gumba.
4. Ne koristiti općenito `.form-control` ili `.btn` bez parent selektora navbara.
5. Nakon toga testirati naslovnu, `default`, `nebeski_mir`, `zlatno_polje`, `jedro_u_suton`, `magazin`.

## Napomena

Ovaj audit samo traži postojeće stanje. Ne radi izmjene u kodu.