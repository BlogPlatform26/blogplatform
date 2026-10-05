# Phase 89c — shared desni profil: lom dugog korisničkog imena

## Opseg

Phase 89a je u `polje_lavande` potvrdila tabletni document overflow desnog
profilnog panela kad korisničko ime nema razmake. Uzrok je zajednički za desne
sidebare: `.blog-profile-panel__identity` se smije suziti, ali samo ime nije
smjelo lomiti neprekinuti niz. Ova faza ne mijenja širine stupaca, kalendar,
kontrast ni pojedini dizajn.

## Promjena

Zajednička `.blog-profile-panel__name` klasa sada ima
`overflow-wrap: anywhere`. To zadržava svaku znamenku imena vidljivom unutar
postojećeg panela, bez `overflow: hidden`, elipse ili horizontalnog širenja.
Uobičajena imena i desktop razmještaj ne mijenjaju se; samo neprekinuta duga
imena dobivaju dodatne retke.

## Stvarni preglednik

Izolirani autor s imenom `phase89c_lavender_profile_name_without_spaces`
prije popravka imao je `scrollWidth 416 px` unutar imena širokog 81 px na
768 px, a document overflow je bio 276 px. Isti je problem postojao u blog i
detail rutama, na 320/390/768/1440 px (`199/129/276/100 px`).

Nakon promjene svih osam stanja Lavande imaju document overflow `0 px`;
ime, identitet, panel i glavni red imaju jednak client/scroll width. Na 768 px
ime se čitljivo prelomi unutar 81 px (`112 px` visine), bez odsijecanja. Kao
reprezentativni drugi desni sidebar provjeren je `neonski_grad`: blog i detail
na 768 px također imaju overflow `0 px`, uz isti `overflow-wrap:anywhere`
ugovor. Sigurni klikovi kalendara i dana s objavom vode na očekivani query i
slugged detail bez mutacije.

## Regresijska zaštita

`blog/test_phase89c_profile_name_wrap.py` renderira blog i detail za
`polje_lavande` i `neonski_grad` s dugim imenom bez razmaka te potvrđuje
zajednički ugovor. 
