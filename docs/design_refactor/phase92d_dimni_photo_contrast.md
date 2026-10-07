# Phase 92d — Dimni akordi, kontrast preko fotografije

## Opseg i nalaz prije izmjene

Provjera u izoliranoj sintetičkoj bazi, s objavom, komentarom i arhivskom objavom, obuhvatila je blog i detalj objave na 320, 390, 768 i 1440 px. Bootstrap CDN bio je učitan (`.row` je `display: flex`). Naslov bloga bio je izravno preko fotografije, kartice posta/kalendar/arhiva imali su samo `rgba(31,17,12,.18)`, a desktop komentar poluprozirnu bijelu pozadinu. Zbog promjene svijetlih i tamnih dijelova fotografije referentni kontrast iz Phase92a nije jamčio čitljivost; autor komentara imao je 3.51:1 na tamnoj referentnoj osnovi.

## Promjena

Samo u temi `dimni_akordi` dodana je uska zadimljena podloga naslova/podnaslova (`.84`), ista neprozirnost za post, kalendar, arhivu i bočne kartice te `.90` za tijelo komentara. Mjesečna navigacija dobila je čvrstu tamnu podlogu. Godina objave, koju zajednički date-style ugovor inače prikazuje s `opacity: .72`, lokalno je posvijetljena bez prigušenja. Fotografija ostaje panoramska i vidljiva oko kartica; desktop raspored i mobilni redoslijed nisu promijenjeni.

## Mjerenje i provjera

Kontrast je izračunat iz efektivnih computed boja, uključujući alpha i opacity, konzervativno s potpuno bijelom fotografijom ispod podloge — svjetlijom od stvarnih opaženih zona. Najniže vrijednosti: blog naslov 8.86:1, podnaslov 5.35:1, naslov posta 9.53:1, tijelo 8.85:1, autor/akcije 6.88:1, sitni autorski metapodaci 5.45:1, tekst komentara 13.67:1, autor komentara 10.63:1, vrijeme komentara 5.07:1, kalendarski naslov 7.07:1, dan s objavom 7.52:1, arhivska veza 7.26:1 i mjesečna navigacija 13.35:1. Godina objave sada ima neprozirnu svijetlu boju na tamnoj kartici. Sve navedene tekstualne mete imaju najmanje 4.5:1 i na krajnje svijetloj podlozi.

U stvarnom pregledniku potvrđeno je svih osam prikaza: 320, 390, 768 i 1440 px × blog/detalj. `document.scrollWidth` bio je redom 305, 375, 753 i 1425 px naspram širine prikaza 320, 390, 768 i 1440 px. Kartice i komentari nisu imali lokalni overflow. Vizualno je potvrđen očuvan dimni fotografski i trostupčani desktop identitet. Kliknute su isključivo sigurne navigacije: prethodni/sljedeći mjesec, dan s objavom i arhiva; nije kliknut like niti poslan komentar.

Uski regresijski testovi: 4/4. `manage.py check` i `makemigrations --check --dry-run`: čisti. Puni skup testova: 157/157.

## Ostaje otvoreno

P2 touch mete kalendarskih dana na mobitelu (27/31 px), pojedine desktop kalendarske mete i zajedničke tablet/desktop post-action mete (oko 21–25 px). Nisu ovime auditirana preostala tri dizajna (`sjene_ulice`, `mjesecev_ples`, `asfaltni_plamen`) niti zatvorena završna matrica svih 37.
