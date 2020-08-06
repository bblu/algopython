select * from proj_product a,equ_te_equip_prj_rela1 b where a.item_code = b.item_id

select * from equ_te_equip_prj_rela1 b,t_tx_znyc_dz c where b.equip_type = '0300' and b.pms_equip_id = c.sbid
select * from equ_te_equip_prj_rela1 b,t_tx_znyc_pdbyq c where b.equip_type = '0302' and b.pms_equip_id = c.sbid
select * from equ_te_equip_prj_rela1 b,t_tx_zwyc_zsbyq c where b.equip_type = '0302' and b.pms_equip_id = c.sbid
select * from equ_te_equip_prj_rela1 b,t_tx_znyc_zbyq c where b.equip_type = '0301' and b.pms_equip_id = c.sbid
0303:线路  0300：变电站 0301主变 0302 配变

select * from equ_te_equip_prj_rela1 b,t_tx_zwyc_xl c where b.equip_type = '0303' and b.pms_equip_id = c.sbid

select * from t_tx_zwyc_xl a,t_tx_zwyc_dxd b where a.oid = b.ssxl
select * from t_tx_zwyc_xl a,t_tx_zwyc_dld b where a.oid = b.ssxl


select st_astext(shape) from t_tx_zwyc_dld limit 10

select * from equ where equip_type='' or pms_equip_id=''
delete from equ where equip_type='' or pms_equip_id=''

select a.oid,b.ssxl,b.sbmc,b.shape from t_tx_zwyc_xl a,t_tx_zwyc_dxd b where a.oid = b.ssxl 
limit 10

create table equ_xl as
select item_id,oid,sbmc,sbid from equ b,t_tx_zwyc_xl c 
where b.equip_type = '0303' and b.pms_equip_id = c.sbid

create table equ_xl_dev as
select item_id,b.sbid,b.oid,b.sbmc,c.shape from equ_xl b 
left join t_tx_zwyc_dld c on b.oid=c.ssxl
where c.shape is not null
order by item_id

insert into equ_xl_dev
select item_id,b.sbid,b.oid,b.sbmc,d.shape from equ_xl b 
left join t_tx_zwyc_dxd d on b.oid=d.ssxl
where d.shape is not null
order by item_id

select item_id,count(item_id) from equ_xl group by item_id order by item_id

alter table dwzy.%s alter column shape TYPE geometry USING st_setsrid(shape,3857);

update equ_xl_dev set geom=to_json(st_asgeojson(st_transform(shape,4326)))