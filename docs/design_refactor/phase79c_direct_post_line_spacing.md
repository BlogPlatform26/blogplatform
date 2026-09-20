# Phase 79c — razmak redaka u zasebnim obrascima

Na `/new/` i `/post/<id>/edit/` stil i skripta za izravnu kontrolu razmaka redaka bili su iza završetka Django `content` bloka, pa ih naslijeđeni predložak nije uključivao. Završetak bloka premješten je iza tih postojećih stilova i skripti. Nisu mijenjane njihove implementacije, CKEditor konfiguracija ni dashboard editor.

Render regresija potvrđuje da oba obrasca sadrže po jedan primjerak stila, skripte i postojeće skripte za isključivanje provjere pravopisa. U izoliranoj kopiji baze preglednik je na širinama 320 i 1440 px prikazao točno jednu kontrolu na svakoj ruti, bez horizontalnog preljeva dokumenta. Odabir vrijednosti `2` na 320 px proizveo je `line-height:2` u CKEditor sadržaju i na novom i na postojećem draftu. Nijedan obrazac nije poslan.

Provjere: `manage.py check` bez problema; ciljani render test 1/1; puni Django suite 44/44. Izvorna baza i mediji nisu dirani. Premale dodirne mete iz Phase 79a ostaju zaseban UI zadatak.
