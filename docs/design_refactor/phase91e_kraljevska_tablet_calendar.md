# Phase 91e — Kraljevska pozornica: tabletni kalendar

## Provjera polazišta

Izolirana sintetička baza s javnom objavom i komentarom posluživana je na portu 8768. Prva browser proba u prethodnim fazama nije učitala vanjski Bootstrap CSS zbog TLS provjere CDN-a, pa je prikazala lažni document overflow i desni profil izvan ekrana. Za ovu fazu Chrome je učitao CDN stilove (`ignoreHTTPSErrors` samo u izoliranom browser kontekstu), što je potvrđeno širinom Bootstrap stupaca i prisutnošću stilova. S potpunim CSS-om blog i detalj imaju **0 px document overflowa na 320/390/768/1440** i profil ostaje unutar viewporta. Ta je korekcija zabilježena i u dokumentima Phase91b/c/d.

Stvarni preostali tabletni problem na 768 px bio je **lokalni** overflow: kalendarski okvir `clientWidth/scrollWidth` **148/188 px**, mreža dana **116/172 px**. Tri stupca ostavljala su kalendar u preuskom bočnom stupcu, s lomljenjem navigacije.

## Lokalni zahvat i browser rezultat

Samo na 768–991,98 px tri stupca Kraljevske pozornice slažu se vertikalno, a kalendar je centriran i ograničen na 376 px. Navigacija koristi dva polja od 44 px; sedam dana ima `minmax(0,1fr)` i poveznice najmanje 44×44 px. Mobilni 320/390 i desktop 1440 raspored nisu promijenjeni. Ujedno je lokalno pojačana specifičnost boje linka naslova kako je kasnije runtime pravilo prilagodbe ne bi nadjačalo.

Stvarni Chrome ponovio je blog i detalj na sve četiri širine (**8 stanja**). Na 768 px okvir je sada **374/374**, mreža **350/350 px**, dan s objavom oko **50×46 px**, strelica **44×44 px**, document overflow 0. Na 320/390 okvir i mreža ostaju 232/232 i 200/200 te 258/258 i 226/226 px; na 1440 ostaju 258/258 i 226/226 px. Vizualno je pregledan tabletni kalendar preko izvorne kazališne fotografije te puni mobilni i desktop kadar. Stvarni sigurni klik prethodnog mjeseca na 320/390/768/1440 otvorio je očekivani `?year=2026&month=9`, a klik dana s objavom na 768 otvorio je detalj; mutirajuće kontrole nisu kliknute.

## Granice i provjera

Kontrast bočnih kalendarskih/arhivskih poveznica pri najgorem foto-kadru te tablet/desktop post-akcijske mete ostaju zasebno otvoreni. Desktop kalendarski dani i strelice su također manji od 44 px. Preostala četiri dizajna nisu auditirana.

`blog/test_phase91e_kraljevska_tablet_calendar.py` pokriva lokalni CSS ugovor na blogu i detalju te izolaciju od default dizajna. Uski test, `manage.py check`, `makemigrations --check --dry-run`, `git diff --check` i puni Django skup (**151/151**) prošli su završni gate.
