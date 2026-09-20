# Phase 80d — mobilne dodirne mete podtabova dizajna

Popravak je ograničen na tri podtaba `blog/settings/?tab=dizajn`: Predlošci, Uređivanje i Ugođaj. Zajednička `.design-settings-scope` klasa ograničava mobilna pravila na njihove tabove i primarne kontrole. Do 575,98 px tabovi, „Spremi dizajn”, „Otvori live uređivač”, selecti, tekstualna pretraga te gumbi za reset/odabir/spremanje ugođaja imaju najmanje 44 px visine. CSS URL dobio je novu verziju kako postojeći klijenti ne bi zadržali stari cache. Nisu mijenjane boje, tipografija, dizajnerske kartice ni logika spremanja.

## Izolirani browser: prije → poslije

| Kontrola | 320/390 prije | 320/390 poslije | 768/1440 poslije |
| --- | ---: | ---: | ---: |
| Tri dizajnerska podtaba | 41 px | 44 px | 41 px |
| Spremi dizajn | 37 px | 44 px | 37 px |
| Otvori live uređivač | 37 px | 44 px | 37 px |
| Ugođaj: reset/odabir glazbe | 30 px | 44 px | 30 px |
| Ugođaj: primarno spremanje | 37 px | 44 px | 37 px |
| Ugođaj: selecti | 30–37 px | 44 px | 30–37 px |
| Ugođaj: tekstualna pretraga | 31 px | 44 px | 31 px |

Na viewportima 320/390/768/1440 nema pozitivnog dokumentnog ili unutarnjeg preljeva podtabova. Stvarni klikovi „Uređivanje” i „Ugođaj” otvorili su odgovarajuće podtabove; klik/fokus selecta kursora uspio je bez promjene njegove vrijednosti. Nijedna save/reset akcija nije pritisnuta. Izvorna baza, mediji i port 8000 nisu dirani; sintetička probna baza uklonjena je nakon pregleda.

Uski render/CSS contract test je dodan, a stari Phase 77 test ažuriran je samo za novu verziju CSS URL-a. `manage.py check` bez problema; puni Django suite 50/50. Preostaju nepokriveni zasebni oblici poput prekidača glazbe i samih dizajnerskih kartica, za koje ova faza ne tvrdi potpunu mobilnu reviziju.
