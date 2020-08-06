--no scale_denominator column
select * from information_schema.columns where column_name LIKE '*scale*';

select z(!scale_denominator!);

select count(*)  
---------------------------------------------------------------- 
CREATE OR REPLACE VIEW public.landuse_layer AS 
SELECT osm_ids2mbid(MAX(osm_id), true) AS osm_id, 
ST_CollectionExtract(ST_Collect(geometry), 3) AS geometry, 
landuse_class(type) AS class, type
FROM (
            SELECT osm_id, geometry, type
            FROM landuse_z5toz6
            --WHERE z(!scale_denominator!) BETWEEN 5 AND 6
            UNION ALL
            SELECT osm_id, geometry, type
            FROM landuse_z7toz8
            --WHERE z(!scale_denominator!) BETWEEN 7 AND 8
          ) 
          AS landuse_z5toz8
          --WHERE geometry && !bbox!
          GROUP BY type
          UNION ALL
          SELECT
            osm_ids2mbid(osm_id, true) AS osm_id, geometry,
            landuse_class(type) AS class, type
            FROM (
              SELECT osm_id, geometry, type
              FROM landuse_z9
              --WHERE z(!scale_denominator!) = 9
              UNION ALL
              SELECT osm_id, geometry, type
              FROM landuse_z10
              --WHERE z(!scale_denominator!) = 10
              UNION ALL
              SELECT osm_id, geometry, type
              FROM landuse_z11
              --WHERE z(!scale_denominator!) = 11
              UNION ALL
              SELECT osm_id, geometry, type
              FROM landuse_z12
              --WHERE z(!scale_denominator!) = 12
              UNION ALL
              SELECT osm_id, geometry, type
              FROM landuse_z13toz14
              --WHERE z(!scale_denominator!) BETWEEN 13 AND 14
            ) AS landuse_z9toz14
 ------------------------------------------------------
 CREATE OR REPLACE VIEW public.waterway_layer AS
 SELECT osm_ids2mbid(osm_id, false) AS osm_id, geometry, type, type AS class
          FROM (
            SELECT *
            FROM waterway_z7toz9
            UNION ALL
            SELECT *
            FROM waterway_z10toz12
            UNION ALL
            SELECT *
            FROM waterway_z13
            UNION ALL
            SELECT *
            FROM waterway_z14
          ) AS tbname
--Query returned successfully with no result in 132 msec.--
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.water_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id,geometry
          FROM (
            SELECT osm_id, geometry
            FROM water_z0
            --WHERE z(!scale_denominator!) = 0
            UNION ALL
            SELECT osm_id, geometry
            FROM water_z1
            --WHERE z(!scale_denominator!) = 1
            UNION ALL
            SELECT osm_id, geometry
            FROM water_z2toz3
            --WHERE z(!scale_denominator!) BETWEEN 2 AND 3
            UNION ALL
            SELECT osm_id, geometry
            FROM water_z4
            --WHERE z(!scale_denominator!) = 4
            UNION ALL
            SELECT osm_id, geometry
            FROM water_z5toz7
            --WHERE z(!scale_denominator!) BETWEEN 5 AND 7
            UNION ALL
            SELECT osm_id, geometry
            FROM water_z8toz10
            --WHERE z(!scale_denominator!) BETWEEN 8 AND 10
            UNION ALL
            SELECT osm_id, geometry
            FROM water_z11toz12
            --WHERE z(!scale_denominator!) BETWEEN 11 AND 12
            UNION ALL
            SELECT osm_id, geometry
            FROM water_z13toz14
            --WHERE z(!scale_denominator!) BETWEEN 13 AND 14
          ) AS water
---Query returned successfully with no result in 1.1 secs.
-----------------------------------------------------------------
 CREATE OR REPLACE VIEW public.aeroway_layer AS
SELECT osm_ids2mbid(osm_id, is_polygon(geometry)) AS osm_id, geometry, type
          FROM (
            SELECT *
            FROM aeroway_z9
            --WHERE z(!scale_denominator!) = 9
            UNION ALL
            SELECT *
            FROM aeroway_z10toz14
            --WHERE z(!scale_denominator!) BETWEEN 10 AND 14
          ) AS aeroway
--Query returned successfully with no result in 98 msec.
 -----------------------------------------------------------------
 CREATE OR REPLACE VIEW public.barrier_line_layer AS
SELECT osm_ids2mbid(osm_id, is_polygon(geometry)) AS osm_id, geometry, barrier_line_class(type) AS class
          FROM barrier_line_z14
--Query returned successfully with no result in 32 msec.
 -----------------------------------------------------------------
CREATE OR REPLACE VIEW public.building_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, geometry, building_is_underground(underground) AS underground
          FROM (
            SELECT osm_id, geometry, underground
            FROM building_z13
            --WHERE z(!scale_denominator!) = 13
            UNION ALL
            SELECT osm_id, geometry, underground
            FROM building_z14
            --WHERE z(!scale_denominator!) = 14
          ) AS building
          --WHERE geometry && !bbox!
          ORDER BY ST_YMin(ST_Envelope(geometry)) DESC
limit 3
--Query returned successfully with no result in 82 msec.
 -----------------------------------------------------------------
CREATE OR REPLACE VIEW public.landuse_overlay_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id,
            --CASE WHEN ST_Area(geometry) > 10000000
            --    THEN ST_Intersection(ST_MakeValid(geometry), !bbox!)
            --     ELSE geometry
            --END AS 
            geometry,
            landuse_overlay_class(type) AS class, type
          FROM (
            SELECT osm_id, geometry, type FROM landuse_overlay_z5
            --WHERE z(!scale_denominator!) = 5
            UNION ALL
            SELECT osm_id, geometry, type FROM landuse_overlay_z6
            --WHERE z(!scale_denominator!) = 6
            UNION ALL
            SELECT osm_id, geometry, type FROM landuse_overlay_z7
            --WHERE z(!scale_denominator!) = 7
            UNION ALL
            SELECT osm_id, geometry, type FROM landuse_overlay_z8
            --WHERE z(!scale_denominator!) = 8
            UNION ALL
            SELECT osm_id, geometry, type FROM landuse_overlay_z9
            --WHERE z(!scale_denominator!) = 9
            UNION ALL
            SELECT osm_id, geometry, type FROM landuse_overlay_z10
            --WHERE z(!scale_denominator!) = 10
            UNION ALL
            SELECT osm_id, geometry, type FROM landuse_overlay_z11toz12
            --WHERE z(!scale_denominator!) BETWEEN 11 AND 12
            UNION ALL
            SELECT osm_id, geometry, type FROM landuse_overlay_z13toz14
            --WHERE z(!scale_denominator!) BETWEEN 13 AND 14
          ) AS landuse_overlay
limit 3
--Query returned successfully with no result in 153 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.road_layer AS
SELECT osm_id, geometry, type, class, oneway, structure FROM (
              SELECT osm_ids2mbid(MAX(osm_id), false) AS osm_id, ST_CollectionExtract(ST_Collect(geometry), 2) AS geometry,
              road_type(road_class(type, NULL, NULL), type, NULL, NULL, NULL) AS type,
              road_class(type, NULL, NULL) AS class, road_oneway(0) AS oneway, 'none' AS structure, NULL AS z_order
              FROM (
                SELECT * FROM road_z5
                --WHERE z(!scale_denominator!) = 5
                UNION ALL
                SELECT * FROM road_z6toz7
                --WHERE z(!scale_denominator!) BETWEEN 6 AND 7
                UNION ALL
                SELECT * FROM road_z8toz9
                --WHERE z(!scale_denominator!) BETWEEN 8 AND 9
                UNION ALL
                SELECT * FROM road_z10
                --WHERE z(!scale_denominator!) = 10
              ) AS road_grouped_zoom_levels
              --WHERE geometry && !bbox!
              GROUP BY type
              UNION ALL
              SELECT osm_ids2mbid(osm_id, is_polygon(geometry)) AS osm_id, geometry,
              road_type(road_class(type, service, access), type, construction, tracktype, service) AS type,
              road_class(type, service, access) AS class, road_oneway(oneway) AS oneway, structure, z_order
               FROM (
                SELECT * FROM road_z11
                --WHERE z(!scale_denominator!) = 11
                UNION ALL
                SELECT * FROM road_z12
                --WHERE z(!scale_denominator!) = 12
                UNION ALL
                SELECT * FROM road_z13
                --WHERE z(!scale_denominator!) = 13
                UNION ALL
                SELECT * FROM road_z14
                --WHERE z(!scale_denominator!) = 14
               ) AS t2
              --WHERE geometry && !bbox!
              ORDER BY z_order ASC
           ) AS ordered_roads
limit 3
--Query returned successfully with no result in 1.3 secs.
 -----------------------------------------------------------------
CREATE OR REPLACE VIEW public.admin_layer AS
SELECT osm_ids2mbid(osm_id, false) AS osm_id, geometry, admin_level, disputed, maritime
          FROM (
            SELECT osm_id, geometry, admin_level, disputed, maritime
            FROM admin_z0
            --WHERE z(!scale_denominator!) = 0
            UNION ALL
            SELECT osm_id, geometry, admin_level, disputed, maritime
            FROM admin_z1toz2
            --WHERE z(!scale_denominator!) BETWEEN 1 AND 2
            UNION ALL
            SELECT osm_id, geometry, admin_level, disputed, maritime
            FROM admin_z3
            --WHERE z(!scale_denominator!) = 3
            UNION ALL
            SELECT osm_id, geometry, admin_level, disputed, maritime
            FROM admin_z4toz5
            --WHERE z(!scale_denominator!) BETWEEN 4 AND 5
            UNION ALL
            SELECT osm_id, geometry, admin_level, disputed, maritime
            FROM admin_z6
            --WHERE z(!scale_denominator!) = 6
            UNION ALL
            SELECT osm_id, geometry, admin_level, disputed, maritime
            FROM admin_z7toz14
            --WHERE z(!scale_denominator!) BETWEEN 7 AND 14
          ) AS admin
limit 3
--Query returned successfully with no result in 202 msec.
 -----------------------------------------------------------------
CREATE OR REPLACE VIEW public.country_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, wkb_geometry,
          iso3166_1_alpha_2 AS code,
          name,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh,
          rank AS scalerank
          FROM custom_countries
          WHERE (
            (
              rank <= 2
              --AND z(!scale_denominator!) = 1 AND wkb_geometry && !bbox!
            )
            OR
            (
              rank <= 3
              --AND z(!scale_denominator!) >= 2 AND wkb_geometry && !bbox!
            )
            OR
            (
              rank <= 4
              --AND z(!scale_denominator!) >= 3 AND wkb_geometry && !bbox!
            )
            OR
            (
              rank <= 5
              --AND z(!scale_denominator!) >= 4 AND wkb_geometry && !bbox!
            )
            OR
            (
              rank <= 6
              --AND z(!scale_denominator!) >= 5 AND wkb_geometry && !bbox!
            )
            OR
            (
              rank >= 7
              --AND z(!scale_denominator!) >= 6 AND wkb_geometry && !bbox!
            )
          )
limit 3
--Query returned successfully with no result in 997 msec.
 -----------------------------------------------------------------
CREATE OR REPLACE VIEW public.marine_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, wkb_geometry,
          name,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh, 
          case when ST_GeometryType(wkb_geometry) = 'ST_LineString' then 'line'
               else 'point' end AS placement,
          rank AS labelrank
          FROM custom_seas
          WHERE 
          --wkb_geometry && !bbox! AND 
          (
            (
              rank = 1 --AND z(!scale_denominator!) >= 1
            )
            OR (
              rank = 2 --AND z(!scale_denominator!) >= 2
            )
            OR (
              rank = 3 --AND z(!scale_denominator!) >= 3
            )
            OR (
              rank = 4 --AND z(!scale_denominator!) >= 4
            )
            OR (
              rank = 5 --AND z(!scale_denominator!) >= 5
            )
            OR (
              rank = 6 --AND z(!scale_denominator!) >= 6
            )
          )
limit 3
--Query returned successfully with no result in 53 msec.
 -----------------------------------------------------------------
 CREATE OR REPLACE VIEW public.state_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, wkb_geometry, abbr,
          area_sqkm AS area,
          name,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh
          FROM custom_states
          WHERE --wkb_geometry && !bbox! AND 
          (
            (
              area_sqkm > 90000 --AND z(!scale_denominator!) >= 4
            )
            --OR (z(!scale_denominator!) >= 5)
          )
limit 3
--Query returned successfully with no result in 212 msec.
 -----------------------------------------------------------------
CREATE OR REPLACE VIEW public.place_label_layer AS
--SELECT * FROM (
            SELECT osm_ids2mbid(osm_id, true) as osm_id, topoint(geometry) AS geometry,
            name,
            coalesce(NULLIF(name_en, ''), name) AS name_en,
            coalesce(NULLIF(name_es, ''), name) AS name_es,
            coalesce(NULLIF(name_fr, ''), name) AS name_fr,
            coalesce(NULLIF(name_de, ''), name) AS name_de,
            coalesce(NULLIF(name_ru, ''), name) AS name_ru,
            coalesce(NULLIF(name_zh, ''), name) AS name_zh,
            type,
            CASE WHEN is_capital THEN 2 ELSE capital END AS capital,
            NULL AS ldir,
            normalize_scalerank(scalerank) AS scalerank,


            row_number() OVER (--PARTITION BY LabelGrid(geometry, 85 * !pixel_width!)
                         ORDER BY scalerank ASC NULLS LAST,
                                  population DESC NULLS LAST
            ) AS localrank
            FROM (
                SELECT * FROM place_label_z3
                --WHERE z(!scale_denominator!) = 3
                UNION ALL
                SELECT * FROM place_label_z4
                --WHERE z(!scale_denominator!) = 4
                UNION ALL
                SELECT * FROM place_label_z5
                --WHERE z(!scale_denominator!) = 5
                UNION ALL
                SELECT * FROM place_label_z6toz7
                --WHERE z(!scale_denominator!) BETWEEN 6 AND 7
                UNION ALL
                SELECT * FROM place_label_z8
                --WHERE z(!scale_denominator!) = 8
                UNION ALL
                SELECT * FROM place_label_z9
                --WHERE z(!scale_denominator!) = 9
                UNION ALL
                SELECT * FROM place_label_z10
                --WHERE z(!scale_denominator!) = 10
                UNION ALL
                SELECT * FROM place_label_z11toz12
                --WHERE z(!scale_denominator!) BETWEEN 11 AND 12
                UNION ALL
                SELECT * FROM place_label_z13
                --WHERE z(!scale_denominator!) = 13
                UNION ALL
                SELECT * FROM place_label_z14
                --WHERE z(!scale_denominator!) = 14
              ) AS place_label
            -- WHERE geometry && !bbox!
            ORDER BY population DESC NULLS LAST
        ) 
        --AS t WHERE z(!scale_denominator!) >= 11
                  --OR (z(!scale_denominator!) = 10 AND localrank < 6)
                  --OR (z(!scale_denominator!) = 9 AND localrank < 8)
                  --OR (z(!scale_denominator!) = 8 AND localrank < 12)
                  --OR (z(!scale_denominator!) = 7 AND localrank < 12)
                  --OR (z(!scale_denominator!) = 6 AND localrank < 8)
                  --OR z(!scale_denominator!) <= 5
                  
limit 3
--Query returned successfully with no result in 112 msec.
 -----------------------------------------------------------------
 CREATE OR REPLACE VIEW public.water_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, geometry AS geometry,
          name,
          area,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh
          FROM (
            SELECT * FROM water_label_z10
            --WHERE z(!scale_denominator!) = 10
            UNION ALL
            SELECT * FROM water_label_z11
            --WHERE z(!scale_denominator!) = 11
            UNION ALL
            SELECT * FROM water_label_z12
            --WHERE z(!scale_denominator!) = 12
            UNION ALL
            SELECT * FROM water_label_z13
            --WHERE z(!scale_denominator!) = 13
            UNION ALL
            SELECT * FROM water_label_z14
            --WHERE z(!scale_denominator!) = 14
          ) AS water_label
          -- WHERE geometry && !bbox!
limit 3
--Query returned successfully with no result in 122 msec.
 -----------------------------------------------------------------
CREATE OR REPLACE VIEW public.poi_label_layer AS
 SELECT osm_ids2mbid(osm_id, true) AS osm_id, topoint(geometry) AS geometry, ref, name,
              coalesce(NULLIF(name_en, ''), name) AS name_en,
              coalesce(NULLIF(name_es, ''), name) AS name_es,
              coalesce(NULLIF(name_fr, ''), name) AS name_fr,
              coalesce(NULLIF(name_de, ''), name) AS name_de,
              coalesce(NULLIF(name_ru, ''), name) AS name_ru,
              coalesce(NULLIF(name_zh, ''), name) AS name_zh,
              format_type(type) AS type,
              CASE WHEN name = '' THEN NULL
                   ELSE poi_label_scalerank(type, area)
              END AS scalerank,
              coalesce(NULLIF(maki_label_class(type), ''), 'marker') AS maki,
              rank() OVER (--PARTITION BY LabelGrid(geometry, 128 * !pixel_width!)
                           ORDER BY poi_label_localrank(type, name) ASC) AS localrank
            FROM poi_label_z14
            --WHERE z(!scale_denominator!) = 14
             -- AND geometry && !bbox!
limit 3
--Query returned successfully with no result in 72 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.road_label_layer AS
SELECT * FROM
          (
          SELECT osm_ids2mbid(osm_id, false) AS osm_id,
            --CASE WHEN z(!scale_denominator!) < 11
             --    THEN st_startpoint(geometry)
             --    ELSE geometry
            --END AS
            geometry,
            name,
            coalesce(NULLIF(name_en, ''), name) AS name_en,
            coalesce(NULLIF(name_es, ''), name) AS name_es,
            coalesce(NULLIF(name_fr, ''), name) AS name_fr,
            coalesce(NULLIF(name_de, ''), name) AS name_de,
            coalesce(NULLIF(name_ru, ''), name) AS name_ru,
            coalesce(NULLIF(name_zh, ''), name) AS name_zh,
            nullif(ref, '') AS ref,
            nullif(char_length(ref), 0) AS reflen,
            round(MercLength(geometry)) AS len,
            road_class(type, service, access) AS class,
            'default' AS shield,
            rank() OVER (
                --PARTITION BY LabelGrid(geometry, (CASE WHEN z(!scale_denominator!) >= 11
                --                                       THEN 300
                --                                       ELSE 200 
                --                                   END) * !pixel_width!)
                ORDER BY road_localrank(type) ASC, round(MercLength(geometry)) DESC
            ) AS localrank
            FROM (
              SELECT * FROM road_label_z8toz10
              --WHERE z(!scale_denominator!) BETWEEN 8 AND 10
              UNION ALL
              SELECT * FROM road_label_z11
              --WHERE z(!scale_denominator!) = 11
              UNION ALL
              SELECT * FROM road_label_z12toz13
              --WHERE z(!scale_denominator!) BETWEEN 12 AND 13
              UNION ALL
              SELECT * FROM road_label_z14
              --WHERE z(!scale_denominator!) = 14
            ) AS road_label
            -- WHERE geometry && !bbox!
            WHERE ST_GeometryType(geometry) = 'ST_LineString' --change by bblu
              --AND ST_GeometryType(geometry) = 'ST_LineString'
          --) AS t1
          --WHERE (z(!scale_denominator!) BETWEEN 8 AND 10 AND localrank < 2)
          --   OR (z(!scale_denominator!) BETWEEN 11 AND 12 AND localrank < 5)
           --  OR (z(!scale_denominator!) BETWEEN 13 AND 14)
             
limit 3
--WARNING:  column "shield" has type "unknown"
--DETAIL:  Proceeding with relation creation anyway.
--Query returned successfully with no result in 213 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.motorway_junction_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id,
          geometry,
          name,
          NULLIF(ref, '') AS ref,
          NULLIF(char_length(ref), 0) AS reflen,
          junction_type(type) AS type,
          road_type_class(junction_type(type)) AS class
          FROM (
            SELECT * FROM motorway_junction_z12toz14
            --WHERE z(!scale_denominator!) BETWEEN 12 AND 14
          ) AS t
limit 3
--Query returned successfully with no result in 152 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.waterway_label_layer AS
SELECT osm_ids2mbid(osm_id, false) AS osm_id, geometry, name,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh,
          type, type AS class
          FROM (
            SELECT * FROM waterway_label_z13
            --WHERE z(!scale_denominator!) = 13
            UNION ALL
            SELECT * FROM waterway_label_z14
            --WHERE z(!scale_denominator!) = 14
          ) AS waterway_label
          -- WHERE geometry && !bbox!
          --WHERE linelabel(z(!scale_denominator!), name, geometry)
limit 3
--Query returned successfully with no result in 71 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.airport_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, topoint(geometry) AS geometry,
          name,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh,
          coalesce(NULLIF(iata, ''), NULLIF(ref, ''), NULLIF(icao, ''), faa) AS ref,
          airport_label_class(kind, type) AS maki,
          airport_label_scalerank(airport_label_class(kind, type), area, aerodrome) AS scalerank
          FROM airport_label_z9toz14
          -- WHERE geometry && !bbox!
          --AND z(!scale_denominator!) BETWEEN 9 AND 14
limit 3
--Query returned successfully with no result in 102 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.rail_station_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, geometry,
          name,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh,
          rail_station_class(type) AS maki,
          rail_station_class(type) AS network
          FROM (
            SELECT * FROM rail_station_label_z13
            --WHERE z(!scale_denominator!) = 13
            UNION ALL
            SELECT * FROM rail_station_label_z14
            --WHERE z(!scale_denominator!) = 14
          ) AS t
limit 3
--Query returned successfully with no result in 132 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.mountain_peak_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, geometry,
          meter_to_feet(elevation_m) AS elevation_ft,
          elevation_m,
          mountain_peak_type(type) AS maki,
          name,
          coalesce(NULLIF(name_en, ''), name) AS name_en,
          coalesce(NULLIF(name_es, ''), name) AS name_es,
          coalesce(NULLIF(name_fr, ''), name) AS name_fr,
          coalesce(NULLIF(name_de, ''), name) AS name_de,
          coalesce(NULLIF(name_ru, ''), name) AS name_ru,
          coalesce(NULLIF(name_zh, ''), name) AS name_zh
          FROM mountain_peak_label_z12toz14
          -- WHERE geometry && !bbox!
           -- AND z(!scale_denominator!) BETWEEN 12 AND 14
limit 3
--Query returned successfully with no result in 82 msec.
-----------------------------------------------------------------
CREATE OR REPLACE VIEW public.housenum_label_layer AS
SELECT osm_ids2mbid(osm_id, true) AS osm_id, topoint(geometry) AS geometry, house_num
          FROM housenum_label_z14
          -- WHERE geometry && !bbox!
           -- AND z(!scale_denominator!) = 14
limit 3
--Query returned successfully with no result in 61 msec.
-----------------------------------------------------------------
 
