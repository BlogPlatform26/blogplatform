# Phase 93e — dugi naslov bloga Sjene ulice

## Opseg

Samo prelamanje neprekinutog naziva bloga u zaglavlju dizajna `sjene_ulice` i u zajedničkoj kartici profila. Ne mijenja se sadržaj, fotografija, desktop paleta ni podaci korisnika. Sljedeće mobilno sužavanje post/comment kartice i touch mete ostaju zasebni.

## Izolirani preglednik

Sintetička SQLite baza `db_phase93e_trial.sqlite3`, korisnik `phase93eauthor` s nazivom `SjeneUliceNeprekinutiDugiNaslovZaMobilniPrikaz2026`, objava i komentar; lokalni poslužitelj 127.0.0.1:8025. Izvorni `db.sqlite3`, media i port 8000 nisu korišteni. Bootstrap je bio učitan.

| Širina | Blog prije (scroll/client) | Detail prije | Blog poslije | Detail poslije |
| ---: | ---: | ---: | ---: | ---: |
| 320 | 1779/305 | 1779/305 | 305/305 | 305/305 |
| 390 | 1779/375 | 1779/375 | 375/375 | 375/375 |
| 768 | 1961/753 | 1961/753 | 753/753 | 753/753 |
| 1440 | 2130/1425 | 2130/1425 | 1425/1425 | 1425/1425 |

Prvi uski popravak zaglavlja uklonio je najveći izljev, ali je kartica profila s istim neprekinutim nazivom još širila dokument (443/305 na 320). Zajedničko `overflow-wrap: anywhere` na nazivu u kartici uklonilo je i taj preostali uzrok. Nakon popravka naslov i profil imaju `scrollWidth == clientWidth` na sve četiri širine. Na 320 naslov se vizualno prelama unutar tamne plohe bez odsijecanja; panoramska noćna fotografija i desktop izgled ostaju.

Sigurni klikovi na 390: prethodni mjesec i dan s objavom vode na očekivane URL-ove; like/komentar nisu mutirani. Test `blog.test_phase93e_sjene_long_title` pokriva blog/detail i izolaciju tematskog pravila; regresijski Phase93d test također prolazi. `check`, `makemigrations --check --dry-run`, `git diff --check` i puni suite 165/165 prolaze.

## Otvoreno

Post/comment kartica na 320/390 i dalje ima lokalno sužavanje iz Phase93a audita; P2 touch mete kalendara i tablet/desktop post akcija, Kraljevska sidebar foto-kontrast, te audit `mjesecev_ples` i `asfaltni_plamen` ostaju zasebni. Bez završne matrice svih 37 ne proglašava se opći kontrast riješenim.
