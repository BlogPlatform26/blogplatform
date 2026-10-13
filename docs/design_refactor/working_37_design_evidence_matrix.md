[Phase100t](phase100t_vodopad_planine_comment_dates.md) zatvara timestamp P1 Vodopad/Planine: svih32 datuma u16 stanja ima7.35:1 na neprozirnoj lokalnoj podlozi;geometrija i postojeci local overflow identicni100s. Naslovi/komentari/kalendari i druge fotozone jos otvoreni.

[Phase100s](phase100s_vodopad_planine_current_matrix.md) dodaje16 aktualnih stanja Vodopad/Planine s2komentara: timestamp P1 3.42-3.96, uski naslov/comment overflow i tablet kalendari jos otvoreni. Obuhvat15/37 nije15 prolaznih;ostalih22 posebna dizajna trebaju novu matricu. Aplikacija nepromijenjena.

[Phase100r](phase100r_podvodna_photo_bound.md) dodaje analiticku foto-procjenu prvog Podvodna desktop komentara: autor>=4.85,tijelo>=5.10 u provjerenom1440 rasporedu. Izracun koristi stvarni asset i slojeve s marginom; nije izravni rendered-pixel dokaz niti cijela tema prolaz. Aplikacija nepromijenjena.

[Phase100q](phase100q_comment_time_surface.md) zatvara P1 datuma komentara Litica/Podvodna na768/1440: lokalna neprozirna podloga daje15.92:1 i preko fotografije, geometrija svih komentara u16 stanja ista. Mobilni datumi nepromijenjeni. Ostali fotografski kontrasti jos otvoreni.

[Phase100p](phase100p_comment_time_contrast_audit.md) potvrduje novi P1 datuma komentara: Litica4.18:1 i Podvodna3.99:1 na768/1440 izvan foto-zone zbog opacity0.78. Mobiteli prolaze11.46-11.95. Prvi Podvodna desktop komentar ostaje fotografski neprovjeren; screenshot koordinatni nesklad onemogucio je pouzdan pikselni dokaz. Aplikacija nepromijenjena; sirova16-state mjerenja spremljena.

[Phase100o](phase100o_litica_podvodna_mobile_calendar.md) zatvara gusti mobilni kalendar Litica/Podvodna: lokalno vodoravno pomicanje cuva sedam dana i 44px mete, svih 32 blog/detail stanja bez dokumentnog overflowa. Tablet/desktop geometrija nepromijenjena. Fotografski kontrasti i preostala matrica ostaju otvoreni.

[Phase100n](phase100n_litica_podvodna_tablet_calendar.md) zatvara tablet kalendar Litica/Podvodna768-991: puni tjedan7x44px bez overflowa; desktop nepromijenjen. Tada potvrdeni gusti mobilni overflow sada je zatvoren u Phase100o.

[Phase100m](phase100m_podvodna_mobile_comment_author.md) zatvara mobilni autor-link P1 Podvodne:13.96:1 umjesto3.95. Tablet/desktop boja nepromijenjena.100l kalendarski overflow i fotografski kontrast ostaju otvoreni.

[Phase100l](phase100l_litica_podvodna_current_matrix.md) dodaje16 aktualnih stanja Litica/Podvodna: mobilni autor komentara Podvodne3.95:1 (P1), oba tablet kalendara+51px grid overflow. Foto-zone ostaju eksplicitno neprovjerene. Preostala24 posebna dizajna trebaju novu seriju;13 obuhvacenih nije13 prolaznih.

[Phase100k](phase100k_magazin_factory_title_surface.md) zatvara Magazin tvornicki foto-naslov:14.68:1 uz lokalnu neprozirnu podlogu. Dugi naslovi vise ne preklapaju objave; korisnicke boje sacuvane. Matrica svih37 i desktopne mete jos nisu dovrsene.

[Phase100j](phase100j_magazin_photo_title_evidence.md) potvrdjuje Magazin fotografski naslov ispod3:1: osam stanja, najnizi uzorkovani omjeri1.44-1.74. Problem sada izmjeren, popravak jos otvoren. Aplikacijski kod nepromijenjen.

[Phase100i](phase100i_editorial_phone_post_headers.md) zatvara uske mobilne naslove Studio/Magazin. Svih 16 aktualnih stanja bez dokumentnog i uzorkovanog lokalnog overflowa; geometrija na 768/1440 nepromijenjena. Fotografski kontrast i desktopne mete ostaju otvoreni.

# Radna matrica dokaza za 37 registriranih dizajna

## Novije provjere — 10. listopada 2026.

[Phase100h](phase100h_studio_action_calendar_contrast.md) zatvara dva Studio P1 nalaza iz 100g: lajk sada 5.53:1, današnji datum 5.86:1. Mobilni naslovi i preostale stavke matrice ostaju otvoreni.

[Phase100g — Studio i Magazin](phase100g_studio_magazin_current_matrix.md) dodaje 16 aktualnih blog/detail prikaza s komentarima i sistemskom fotografijom. Studio ima potvrđen P1 kontrast lajka i današnjeg dana, oba dizajna imaju uske mobilne naslove, a Magazinov naslov preko fotografije ostaje neizmjeren. Ostaje 26 posebnih dizajna bez nove serije; ova dva nisu proglašena potpuno završenima.

Raniji P1 nalazi naslova Simple objava zatvoreni su u [Phase100d](phase100d_simple_post_title_contrast.md), a kontrast gumba za lajk u [Phase100e](phase100e_like_theme_contrast.md) (72 prikaza, 5.34–7.19:1). [Phase100f](phase100f_dark_comment_status_contrast.md) popravlja statusne poruke komentara dark/dark_right na 9.84:1. Povijesni odlomak niže koji navodi otvorene like/title P1 nalaze opisuje stanje prije tih faza. Ove uske provjere ne zamjenjuju završnu matricu: drugih 28 dizajna i potpuna tvornička Default provjera još su otvoreni, kao i preostale touch mete i lokalni overflow.

Ovo je **indeks postojećih mjerenja**, ne završna potvrda da je svih 37 dizajna usklađeno. Popis dolazi iz `Profile.TEMPLATE_CHOICES` u `blog/models.py` i [Phase 75 inventara](phase75_mobile_inventory_and_test_matrix.md). Svaki red upućuje na relevantne pojedinačne ili obiteljske izvještaje; raniji audit i naknadni popravci moraju se čitati zajedno. Pri ovom osvježenju indeksa nije ponavljan browser audit niti je mijenjan aplikacijski kod ili korisnički sadržaj.

| # | Registrirani ključ | Postojeći dokaz za blog/detail ili zadnji popravak |
| ---: | --- | --- |
| 1 | `default` | [99a shared-base audit](phase99a_shared_base_current_state_audit.md), [100a aktualna serija — spremljena, ne tvornička paleta](phase100a_shared_base_final_matrix_batch.md) |
| 2 | `dark` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [99b autor](phase99b_shared_author_link_contrast.md) |
| 3 | `classic` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [99b autor](phase99b_shared_author_link_contrast.md) |
| 4 | `default_right` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [99b autor](phase99b_shared_author_link_contrast.md) |
| 5 | `dark_right` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [99b autor](phase99b_shared_author_link_contrast.md) |
| 6 | `classic_right` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [99b autor](phase99b_shared_author_link_contrast.md) |
| 7 | `simple_pattern` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [100b tvornički naslov](phase100b_simple_pattern_factory_header.md), [99g spremljeni žuti naslov](phase99g_simple_pattern_header_contrast.md) |
| 8 | `simple_image` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [99e naslov](phase99e_simple_image_header_contrast.md) |
| 9 | `simple_retro` | [100a aktualna serija](phase100a_shared_base_final_matrix_batch.md), [99h naslov](phase99h_simple_retro_header_contrast.md) |
| 10 | `soho` → `studio.html` | [83a audit](phase83a_special_designs_batch1_audit.md), [55 mobilni stupci](phase55_soho_mobile_column_fix.md) |
| 11 | `magazin` | [83k kontrast](phase83k_magazin_contrast.md) |
| 12 | `litica_noci` | [84f2 komentar](phase84f2_comment_contrast.md) |
| 13 | `podvodna_tisina` | [84f2 komentar](phase84f2_comment_contrast.md) |
| 14 | `vodopad_u_magli` | [84f3b kontrast](phase84f3b_vodopad_contrast_fix.md) |
| 15 | `planine_u_magli` | [84f4c naslov](phase84f4c_planine_hero_contrast.md) |
| 16 | `nebeski_mir` | [84f5c naslov](phase84f5c_nebeski_hero_contrast.md) |
| 17 | `svemirski_horizont` | [85d tabletni kalendar](phase85d_svemirski_tablet_calendar.md) |
| 18 | `zlatni_horizont` | [86e tabletni kalendar](phase86e_zlatni_tablet_calendar.md) |
| 19 | `iznad_oblaka` | [87e tabletni kalendar](phase87e_iznad_oblaka_calendar_tablet_fit.md) |
| 20 | `sumska_svjetlost` | [88d kontrast](phase88d_sumska_contrast.md), [88e kalendar](phase88e_forest_polar_calendar_fit.md) |
| 21 | `polarna_svjetlost` | [88c2 komentar/arhiva](phase88c2_polarna_comment_archive_contrast.md), [88e kalendar](phase88e_forest_polar_calendar_fit.md) |
| 22 | `zlatno_polje` | [89f naslov](phase89f_zlatno_hero_contrast.md) |
| 23 | `neonski_grad` | [89b uputa](phase89b_neonski_guest_hint_contrast.md) |
| 24 | `polje_lavande` | [89e fotografski kontrast](phase89e_lavanda_photo_contrast.md) |
| 25 | `carobna_ljubicasta` | [90c fotografski kontrast](phase90c_carobna_photo_contrast.md), [90d kalendar](phase90d_carobna_tablet_calendar.md) |
| 26 | `kraljevska_pozornica` | [91d post/komentar](phase91d_kraljevska_post_comment_contrast.md), [91e kalendar](phase91e_kraljevska_tablet_calendar.md), [91f sidebar](phase91f_kraljevska_sidebar_contrast.md) |
| 27 | `dimni_akordi` | [92d fotografski kontrast](phase92d_dimni_photo_contrast.md), [96a mobilni kalendar](phase96a_dimni_mobile_calendar_touch.md) |
| 28 | `nebeska_klasika` | [83i kontrast](phase83i_nebeska_klasika_contrast.md) |
| 29 | `ponocna_elegancija` | [83j kontrast](phase83j_ponocna_elegancija_contrast.md) |
| 30 | `ruzicasti_vrt` | [83d kontrast](phase83d_ruzicasti_vrt_contrast.md) |
| 31 | `stara_aleja` | [83b kontrast](phase83b_stara_aleja_contrast.md) |
| 32 | `staza_prema_vrhovima` | [83g kontrast](phase83g_staza_prema_vrhovima_contrast.md) |
| 33 | `jedro_u_suton` | [83c kontrast](phase83c_jedro_u_suton_contrast.md) |
| 34 | `misticno_jezero` | [83h kontrast](phase83h_misticno_jezero_contrast.md) |
| 35 | `sjene_ulice` | [93f mobilni post/komentar](phase93f_sjene_mobile_post_layout.md), [96b mobilni kalendar](phase96b_sjene_mobile_calendar_touch.md) |
| 36 | `mjesecev_ples` | [94c fotografski kontrast](phase94c_mjesecev_photo_contrast.md), [96c mobilni kalendar](phase96c_mjesecev_mobile_calendar_touch.md), [97a mobilni post](phase97a_mjesecev_mobile_post_layout.md) |
| 37 | `asfaltni_plamen` | [95c3 post](phase95c3_asfaltni_post_contrast.md), [95c4 komentar](phase95c4_asfaltni_comment_contrast.md), [95c5 sidebar](phase95c5_asfaltni_sidebar_contrast.md), [95c6 mobilni post](phase95c6_asfaltni_mobile_post_layout.md), [96d mobilni kalendar](phase96d_asfaltni_mobile_calendar_touch.md) |

## Aktualni status nakon Phase100y

[100y](phase100y_nebeski_svemirski_current_matrix.md) dodaje aktualnih16 stanja Nebeskog mira i Svemirskog horizonta:17/37 obuhvacenih, ne17 prolaznih. Dvadeset posebnih kljuceva jos ceka aktualnu seriju. Novi potvrdeni nalazi i preostali opseg nalaze se u izvjestaju i remaining_verification_scope.md; brojevi u starijim odlomcima su povijesni.

[100v](phase100v_vodopad_planine_comment_wrap.md) zatvara lokalni preljev pojedinacne rijeci komentara Vodopada/Planina na mobitelu. Kalendari i druge navedene provjere ostaju otvoreni.

Ovaj indeks nije postotak dovrsenosti projekta. Aktualnim serijama obuhvaceno je 15/37 kljuceva, ali nisu svi dobili zavrsni prolaz. Preostala 22 imaju ranije radove, a cekaju aktualnu verifikaciju. [Preostali opseg](remaining_verification_scope.md) odvaja otvorene nalaze od dovrsenih zahvata. [100u](phase100u_vodopad_planine_phone_titles.md) zatvara mobilne post-naslove Vodopada/Planina; 100t njihove datume komentara. Povijesni P1 navodi za Simple naslove i zajednicki like iz 100a zatvoreni su u 100d/e.

## Što indeks ne dokazuje

Završna matrica mora za **svaki** ključ zasebno zabilježiti blog i detalj na 320/390/768/1440 px, kontrast teksta i autora komentara (i na desktopnoj/fotografskoj zoni), naslov/post/autor/akcije, kalendar/arhivu, dokumentni i lokalni overflow, dodirne mete te sigurne klikove. Veza na raniji izvještaj nije zamjena za aktualno završno mjerenje; `soho` se mora testirati registriranim ključem, ne imenom datoteke.

Od izrade početnog indeksa zatvoreni su navedeni lokalni nalazi Asfaltnog plamena i Kraljevske pozornice te četiri mobilna kalendara (Phase95c3–c6 i Phase96a–d). [Phase98a](phase98a_all_design_tablet_post_actions.md) obuhvatila je zajedničke tabletne post-akcije, ali završna provjera dodirnih meta i desktopnih kalendara još nije dovršena. [Phase100a](phase100a_shared_base_final_matrix_batch.md) potvrdila je nove P1 nalaze: naslovi postova tri Simple dizajna i `like` u tamnoj, klasičnoj i Simple obitelji i dalje su ispod 4,5:1. Tvornički `default` treba ponoviti bez naslijeđenih preferencija ID-a 1. Ne smije se zaključiti da drugi redovi prolaze samo zato što u ovom indeksu nema zabilježenog P1 nalaza.

Osvježeni indeks sadrži **37 jedinstvenih redaka i 0 nepostojećih poveznica**. `manage.py check`, `makemigrations --check --dry-run` i `git diff --check` prošli su. Nije bilo promjene aplikacijskog koda; puni skup 213/213 prošao je u prethodnoj Phase100b i ovdje nije ponovno pokretan. Indeks i dalje ne potvrđuje svih 37 aktualnim mjerenjem.
