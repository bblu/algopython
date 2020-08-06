--正常值范围表
SELECT [p1i_min],[p1i_max],[p1o_min],[p1o_max],[date]
FROM [gisdata].[dbo].[alarm_range]

--p1i_min	p1i_max	p1o_min	p1o_max ...	date
--30	50	40	60	... 2017-04-21
------------------------------------------------------------
--创建插入类型生成报警信息触发器
if (object_id('tgr_sync_alarm', 'tr') is not null)
    drop trigger tgr_sync_alarm
go
create trigger tgr_sync_alarm
on dbo.data --表名
    for insert
as
	declare @p1i_min real,@p1i_max real,@p1o_min real,@p1o_max real;
	--有范围表的话直接select赋值
	select @p1i_min = p1i_min, @p1i_max = p1i_max, @p1o_min = p1o_min,@p1o_max = p1o_max from alarm_range;
    declare @id int, @name varchar(16), @p1i real,@p1o real, @dt datetime;
    select @id = id, @name = name, @p1i = press1_in,@p1o = press1_out,@dt = dttm from inserted;

	if (@p1i < @p1i_min or @p1i >@p1i_max)
		insert into dbo.alarm values(@id,@name,'press1_in',@p1i,@p1i_min,@p1i_max,@dt);
	if (@p1o < @p1o_min or @p1o > @p1o_max)
		insert into dbo.alarm values(@id,@name,'press1_out',@p1o,@p1o_min,@p1o_max,@dt);
	
-------------------------------------------------------------
--插入数据
INSERT INTO [gisdata].[dbo].[data]
           ([No],[name],[press1_in],[press1_out],dttm)
     VALUES
           (1,'1#站',10,80,getDate())
-----------------------------------------------------------
SELECT TOP 10 [id]
      ,[name]
      ,[tpio]--警报位置
      ,[warn]--警报值
      ,[rmin]--报警下限
      ,[rmax]--报警上限
      ,[dttm]--日期时间
	  
  FROM [gisdata].[dbo].[alarm]
------------------------------------------------------------
--id	name	tpio		warn	rmin	rmax	dttm
--1	1#站	press1_out	80		3		5		2017-04-21 16:41:01.303
--1	1#站	press1_in 	10		30		50		2017-04-21 16:45:38.663
--1	1#站	press1_out	80		40		60		2017-04-21 16:45:38.663
