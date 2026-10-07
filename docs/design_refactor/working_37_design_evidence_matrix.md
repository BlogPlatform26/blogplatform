# Radna matrica dokaza za 37 registriranih dizajna

Ovo je **indeks postojećih mjerenja**, ne završna potvrda da je svih 37 dizajna usklađeno. Popis dolazi iz `Profile.TEMPLATE_CHOICES` u `blog/models.py` i [Phase 75 inventara](phase75_mobile_inventory_and_test_matrix.md). Svaki red upućuje na najnoviji relevantni pojedinačni ili obiteljski izvještaj; raniji audit i naknadni popravci moraju se čitati zajedno. U ovoj fazi nije ponavljan browser audit, nije mijenjan kod ni korisnički sadržaj.

| # | Registrirani ključ | Postojeći dokaz za blog/detail ili zadnji popravak |
| ---: | --- | --- |
| 1 | `default` | [84a obiteljski audit](phase84a_shared_base_batch1_audit.md) |
| 2 | `dark` | [84d kontrast](phase84d_dark_family_contrast.md) |
| 3 | `classic` | [84a obiteljski audit](phase84a_shared_base_batch1_audit.md) |
| 4 | `default_right` | [84a obiteljski audit](phase84a_shared_base_batch1_audit.md) |
| 5 | `dark_right` | [84d kontrast](phase84d_dark_family_contrast.md) |
| 6 | `classic_right` | [84a obiteljski audit](phase84a_shared_base_batch1_audit.md) |
| 7 | `simple_pattern` | [84c kontrast](phase84c_simple_family_contrast.md) |
| 8 | `simple_image` | [84c kontrast](phase84c_simple_family_contrast.md) |
| 9 | `simple_retro` | [84c kontrast](phase84c_simple_family_contrast.md) |
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
| 26 | `kraljevska_pozornica` | [91d post/komentar](phase91d_kraljevska_post_comment_contrast.md), [91e kalendar](phase91e_kraljevska_tablet_calendar.md) |
| 27 | `dimni_akordi` | [92d fotografski kontrast](phase92d_dimni_photo_contrast.md) |
| 28 | `nebeska_klasika` | [83i kontrast](phase83i_nebeska_klasika_contrast.md) |
| 29 | `ponocna_elegancija` | [83j kontrast](phase83j_ponocna_elegancija_contrast.md) |
| 30 | `ruzicasti_vrt` | [83d kontrast](phase83d_ruzicasti_vrt_contrast.md) |
| 31 | `stara_aleja` | [83b kontrast](phase83b_stara_aleja_contrast.md) |
| 32 | `staza_prema_vrhovima` | [83g kontrast](phase83g_staza_prema_vrhovima_contrast.md) |
| 33 | `jedro_u_suton` | [83c kontrast](phase83c_jedro_u_suton_contrast.md) |
| 34 | `misticno_jezero` | [83h kontrast](phase83h_misticno_jezero_contrast.md) |
| 35 | `sjene_ulice` | [93f mobilni post/komentar](phase93f_sjene_mobile_post_layout.md) |
| 36 | `mjesecev_ples` | [94c fotografski kontrast](phase94c_mjesecev_photo_contrast.md) |
| 37 | `asfaltni_plamen` | [95c1 male kontrole](phase95c1_asfaltni_controls_contrast.md), [95c2 naslov](phase95c2_asfaltni_hero_contrast.md) |

## Što indeks ne dokazuje

Završna matrica mora za **svaki** ključ zasebno zabilježiti blog i detalj na 320/390/768/1440 px, kontrast teksta i autora komentara (i na desktopnoj/fotografskoj zoni), naslov/post/autor/akcije, kalendar/arhivu, dokumentni i lokalni overflow, dodirne mete te sigurne klikove. Veza na raniji izvještaj nije zamjena za aktualno završno mjerenje; `soho` se mora testirati registriranim ključem, ne imenom datoteke.

Poznati otvoreni nalazi pri izradi indeksa: `asfaltni_plamen` još nema zatvoren foto-neovisan post/comment/sidebar kontrast ni uski mobilni post/komentar; `kraljevska_pozornica` sidebar treba zasebnu foto-provjeru; neki mobilni kalendarski dani široki su 27–37 px, a zajedničke tabletne/desktopne post-akcije i pojedine kalendarske mete ostaju ispod 44 px. Ne smije se zaključiti da drugi redovi prolaze samo zato što u ovom indeksu nema zabilježenog P1 nalaza.

Provjera indeksa usporedila je sve retke izravno s `Profile.TEMPLATE_CHOICES`: **37 registriranih ključeva, 37 jedinstvenih redaka, 0 manjkova/viškova i 0 nepostojećih poveznica**. `manage.py check`, `makemigrations --check --dry-run` i `git diff --check` prošli su. Nije bilo promjene aplikacijskog koda; puni skup 177/177 prošao je u neposredno prethodnoj Phase95c2 i ovdje nije ponovno pokretan.
