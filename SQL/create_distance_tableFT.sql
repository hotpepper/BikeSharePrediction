/*update station_distance set ft_dist = ft
where 
staion_distance.station1=ft_d.station1 
and station_distance.station2=ft_d.station2
*/

create table ft_d
(station1 text,
station2 text,
ft double precision
);

insert into ft_d(
select d1.station1, d2.station2, ((d1.x-d2.x)^2 +(d1.y-d2.y)^2)^0.5 as ft

from 

(select station1, st_name1, x,y
from station_distance, stations_shpft
where station1=id
) as d1,

(select station1, station2, st_name2, x,y
from station_distance, stations_shpft
where station2=id
) as d2
where d1.station1=d2.station1)
 --as ft_d
limit 10