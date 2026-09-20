# Phase 79b — redoslijed ruta akcija posta

Audit Phase 79a otkrio je da je generička ruta `post/<int:post_id>/<slug:post_slug>/` presretala `edit/`, `delete/` i `comment/` nastavke. Vlasnik je za `/post/1/edit/` dobivao 404 iz prikaza javnog posta, prije dolaska do prikaza za uređivanje.

Specifične akcije `like/`, `edit/`, `delete/` i `comment/` sada su prije slug-rute. Kanonski javni URL i njegovo ime nisu promijenjeni. Nema migracije ni promjene modela, predložaka ili CSS-a.

Regresijski testovi provjeravaju rezoluciju svih akcijskih ruta i javne slug-rute, vlasnički GET obrasca (200 i pravi predložak) te odbijanje GET-a drugog korisnika (404). U izoliranoj kopiji baze mobilni preglednik na 320 px otvorio je `/post/1/edit/` s naslovom sintetičkog drafta, obrascem i oba akcijska gumba; ništa nije poslano.

Provjere: `manage.py check` bez problema; ciljani testovi 3/3; puni Django suite 43/43. Izvorna baza i mediji nisu dirani. Preostali nalazi iz Phase 79a (nedostajuća kontrola razmaka redaka i premale dodirne mete) nisu dio ovog popravka.
