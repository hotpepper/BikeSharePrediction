select station2 as Station_ID, st_name2 as Name, 
hh as Hour, "Fifteen", cast (avg_Bikes as int), 
cast(cast((avg_Bikes/"totalDocks")*100 as int) as text)||'%'as pct_full, 
left(cast(mi_dist as text),4) as miles

from 
(select station2,  st_name2,  mi_dist
from station_distance
where station1 = 337
order by distance 
limit 4) as top_3, 

(select id, hh,  "Fifteen", avg("availableBikes") as avg_Bikes, 
avg("availableDocks") as avg_Docks, count("ID") as cnt, "totalDocks"
from rawcitibike
where dow in ('WED') and hh = 18 and "Fifteen" = 30 
group by hh,  "Fifteen", id, "totalDocks") as open

where station2=id
order by avg_bikes desc, miles, pct_full desc