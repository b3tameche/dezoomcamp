-- 1
-- select *
-- from green_taxi_data
-- where lpep_pickup_datetime::date = date '2019-09-18' and 
-- 	  lpep_dropoff_datetime::date = date '2019-09-18';

-- 2
-- select lpep_pickup_datetime
-- from green_taxi_data
-- where trip_distance = (select max(trip_distance) from green_taxi_data);

-- 3
-- select tz."Borough"
-- from green_taxi_data td
-- left join taxi_zones tz on tz."LocationID" = td."PULocationID" 
-- where td.lpep_pickup_datetime::date = date '2019-09-18'
-- group by tz."Borough"
-- having sum(td.total_amount) > 50000;

-- 4
-- select taxi_zones."Zone"
-- from taxi_zones
-- where taxi_zones."LocationID" = (select td."DOLocationID"
-- 								 from green_taxi_data td
-- 								 left join taxi_zones tz on tz."LocationID" = td."PULocationID" 
-- 								 where td.lpep_pickup_datetime::date >= date '2019-09-01' and
-- 								 	td.lpep_pickup_datetime::date <= date '2019-09-30' and
-- 								 	tz."Zone" = 'Astoria'
-- 								 order by td.tip_amount desc
-- 								 limit 1);
