
begin;
update rawcitibike
set hh =  (cast (left(right("time", 11),2) as int))
where right("time", 2)= 'AM';


update rawcitibike
set hh =  (cast (left(right("time", 11),2) as int))+12
where right("time", 2)= 'PM';


update rawcitibike
set hh =  0
where hh = 12 and  right("time", 2)= 'AM';


update rawcitibike
set hh =  12
where hh = 24 and  right("time", 2)= 'PM';
commit;

update rawcitibike
set mm = (cast(right(left("time",16),2) as int))
where mm is null;

update rawcitibike
set "Fifteen" = 
case 
	when mm between 0 and 7 then 0
	when mm between 8 and 23 then 15
	when mm between 24 and 37 then 30
	when mm between 38 and 53 then 45
	else 0
end 
where "Fifteen" is null;

update rawcitibike
set dow = 
case
	when EXTRACT(DOW FROM  cast ("time" as timestamp) ) = 0 then 'SUN'
	when EXTRACT(DOW FROM  cast ("time" as timestamp) ) = 1 then 'MON'
	when EXTRACT(DOW FROM  cast ("time" as timestamp) ) = 2 then 'TUE'
	when EXTRACT(DOW FROM  cast ("time" as timestamp) ) = 3 then 'WED'
	when EXTRACT(DOW FROM  cast ("time" as timestamp) ) = 4 then 'THU'
	when EXTRACT(DOW FROM  cast ("time" as timestamp) ) = 5 then 'FRI'
	when EXTRACT(DOW FROM  cast ("time" as timestamp) ) = 6 then 'SAT'
end
where dow is null;
--------------------------------------------------------
select time, hh, mm, "Fifteen", dow, ID
from rawcitibike
order by hh;