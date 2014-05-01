update station_distance
set ft_dist = d.ft
from

(select distinct ft, station_distance.station1, station_distance.station2
from ft_d2, station_distance
where station_distance.station1 = ft_d2.station1
and station_distance.station2 = ft_d2.station2
--and station_distance.station1 = 412
) as d
where station_distance.station1 = d.station1 
and station_distance.station2 = d.station2;

update station_distance
set mi_dist = ft_dist/5280;

select station1, station2, ft_dist, mi_dist
from station_distance
where station1 =412 and station2 = 217;

