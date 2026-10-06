# Phase 91d — Kraljevska pozornica: objava i komentari

## Promjena

Phase91a je pokazala da prozirna kartica objave i prozirni komentar ne jamče čitljivost na svijetlom dijelu fotografije (granice oko 1,95:1 za tijelo i 1,25–1,37:1 za komentar). Lokalno je kartica objave sada neprozirna bordo `#2b0d14`, a komentar zasebna topla tamna površina `#3a1c23`. Svijetla tinta naslova, tijela, autora, akcija i komentara zadržava kazališni karakter. Specifično pravilo za komentar nadjačava kasnije zajedničko mobilno pravilo za prozirnu podlogu, bez izmjena ostalih dizajna.

## Izolirani browser dokaz

Migrirana sintetička SQLite baza s postom i komentarom posluživana je na portu 8767. Stvarni Chrome provjerio je blog i detalj na 320/390/768/1440 px (**8 stanja**). U svih osam computed podloge bile su neprozirne (`rgb(43, 13, 20)` i `rgb(58, 28, 35)`), pa svijetli/tamni foto-kadar ne mijenja omjer. Izmjereni omjeri: naslov objave **16,03:1**, tijelo **13,76:1**, autor i akcijski link **12,54:1**, tekst komentara **11,76:1**, autor komentara **10,71:1**. Vizualno su pregledani detalji na 390 i 1440 px; fotografija ostaje vidljiva iznad kartica. Na svakoj širini stvarni nemutirajući klik `Prethodni mjesec` otvorio je očekivani `?year=2026&month=9`; like i komentiranje nisu kliknuti.

Phase91e je ponovila browser mjerenje uz potpuno učitan Bootstrap CSS: raniji +14/+6 px document excess i izlazak profila bili su artefakti nepotpunog stila; stvarni document overflow je 0 px na sve četiri širine. Kontrast objave/komentara ponovno je izmjeren i ostao je jednak. Na 768 px lokalni calendar overflow bio je stvaran nalaz, obrađen zasebno u Phase91e. Bočni kalendarski/arhivski kontrast i tablet/desktop touch mete ostaju zasebni nalazi; ova faza ne tvrdi da je cijeli dizajn dovršen.

## Regresijski gate

`blog/test_phase91d_kraljevska_post_comment_contrast.py` štiti lokalni ugovor na obje rute. Uski test, `manage.py check`, `makemigrations --check --dry-run`, `git diff --check` i puni Django skup (**149/149**) prošli su završni gate.
