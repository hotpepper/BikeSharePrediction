drop table station_distance;

create table station_distance
(Station1 smallint, 
lat1 double precision,
long1 double precision,
Station2 smallint,
lat2 double precision,
long2 double precision,
distance double precision);

select *
from station_distance;
