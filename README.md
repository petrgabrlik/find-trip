Find trip
=====

find_trip is a script written in Python which finds combinations of flights. It's the entry task for python weekend organized by Kiwi.

Task
----
Find combination of 10 flights, countries must not be repeated, last flight is to the source destination, max duration is one year.

Detailed instructions in _python_wekend.md or in this repository https://gist.github.com/MichalCab/2176c0eb2d996d906eea38e9ec9835d2

Use
-----
```
python find_trip.py input_data.csv
```

Example output
------
Example output for 10 flights per trip
```
1;IT;FCO;BCN;2015-06-02T12:40;2015-06-02T14:35
1;ES;BCN;DUB;2016-03-09T10:20;2016-03-09T12:10
1;IE;DUB;ZRH;2016-03-20T16:10;2016-03-20T19:25
1;CH;ZRH;LCY;2016-03-31T07:40;2016-03-31T08:25
1;GB;LCY;BLL;2016-03-31T19:05;2016-03-31T21:55
1;DK;BLL;AMS;2016-04-10T18:30;2016-04-10T19:40
1;NL;AMS;PRG;2016-04-25T10:55;2016-04-25T12:25
1;CZ;PRG;FRA;2016-05-08T06:00;2016-05-08T07:10
1;DE;FRA;MLA;2016-05-14T13:45;2016-05-14T16:10
1;MT;MLA;FCO;2016-05-16T18:55;2016-05-16T20:20
```

Format
```
<trip_id>;<country_code>;<source>;<destination>;<local_departure_time>;<local_arrival_time>
```
