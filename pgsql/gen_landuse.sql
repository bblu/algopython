select distinct class, type from landuse_layer order by class
 class    |          type
-------------+-------------------------
 park        | park|31
 park        | golf_course|32
 park        | sports_centre|34
 grass       | grass|33
 railway     | railway|51,52,53|
--新版本样式直接用typeid配置不用class或typename了。。。
update green set
class = 
case WHEN type=33 THEN 'grass'
	 WHEN type in(31,32,34) THEN 'park'
     WHEN type in(51,52,53) THEN 'railway'
END
,typename = 
case WHEN type=33 THEN 'grass'
	 WHEN type=31 THEN 'park'
	 WHEN type=32 THEN 'golf_course'
	 WHEN type=34 THEN 'sports_centre'
     WHEN type in(51,52,53) THEN 'railway'
END

alter table green rename to shanxi_green;
alter table poi rename to shanxi_poi;
alter table water rename to shanxi_water;

create table water_area as SELECT bkuid,sum(area) as allarea FROM public.water group by bkuid
--更新面积为总面积
update green set allarea = r.allarea from (SELECT bkuid,sum(area) as allarea FROM public.green group by bkuid) as r where r.bkuid = green.bkuid
update water set allarea = r.allarea from (SELECT bkuid,sum(area) as allarea FROM public.water group by bkuid) as r where r.bkuid = water.bkuid

