Zadání 
============

Na vstupu máte data o letech (`input_data.csv`). Vašim úkolem je z těchto dat sestavit cesty, které obletí přesně 10 různých zemí včetně země z které vylétává první let a vrátí se do původní destinace. Maximální doba trvání cesty od výletu z první země po návrat do původní země je omezena na (1 rok (+/- 24hodin)). Cesty musí obsahovat přesně 10 letů. Vygenerovaných cest musí být minimálně 100.

Formát výstupu
===========
```
<trip_id>;<country_code>;<source>;<destination>;<local_departure_time>;<local_arrival_time>
```
- trip_id - id cesty
- country_code - kód země (ISO Alpha-2) pro letiště z kterého let vylétá
- source - iata kód letiště z kterého let vylétá
- destination - iata kód letiště na které let přilétá
- local_departure_time - lokální čas letiště z kterého let vylétá
- local_arrival_time - lokální čas letiště na které let přilétá

iata kód: https://en.wikipedia.org/wiki/International_Air_Transport_Association_code

Ukazkový výstup
============
```
1;CZ;PRG;BRU;2017-03-04T13:15;2017-03-04T15:15
1;AA;BRU;LON;2017-04-04T13:15;2017-04-04T15:15
1;BB;LON;VIE;2017-05-04T13:15;2017-05-04T15:15
1;CC;VIE;AAA;2017-06-04T13:15;2017-06-04T15:15
1;DD;AAA;HHH;2017-07-04T13:15;2017-07-04T15:15
1;EE;HHH;KKK;2017-08-04T13:15;2017-08-04T15:15
1;FF;KKK;LLL;2017-09-04T13:15;2017-09-04T15:15
1;GG;LLL;GGG;2017-10-04T13:15;2017-10-04T15:15
1;HH;GGG;UUU;2017-11-04T13:15;2017-11-04T15:15
1;II;UUU;PRG;2017-12-04T13:15;2017-12-04T15:15
2;AA;BRU;LON;2017-01-04T13:15;2017-01-04T15:15
2;CZ;LON;PRG;2017-02-04T13:15;2017-03-04T15:15
2;BB;PRG;VIE;2017-03-04T13:15;2017-03-04T15:15
2;CC;VIE;AAA;2017-04-04T13:15;2017-04-04T15:15
2;DD;AAA;HHH;2017-05-04T13:15;2017-05-04T15:15
2;EE;HHH;KKK;2017-06-04T13:15;2017-06-04T15:15
2;FF;KKK;LLL;2017-07-04T13:15;2017-07-04T15:15
2;GG;LLL;GGG;2017-08-04T13:15;2017-08-04T15:15
2;HH;GGG;UUU;2017-09-04T13:15;2017-09-04T15:15
2;II;UUU;BRU;2017-10-04T13:15;2017-10-04T15:15
```

Limitace
======
Úkol musíte řešit pomocí pythonu 2.7/3.5/3.6.
Knihovny můžete využít jakékoliv.

Odevzdání
=========

Jako `.zip` file pomocí přílohy mailu na adresu `pythonvikend@kiwi.com`.



Doporučený zdroj dat
======

**Informace o letištích**
- http://www.iata.org/publications/pages/code-search.aspx
- https://www.world-airport-codes.com/