create table museos(
  MuseoId int AUTO_INCREMENT,
  Nombre varchar(50),
  latitud double,
  longitud double,
  PRIMARY KEY(MuseoId)
);
 
insert into museos (Nombre,latitud,longitud) values ("Universum",19.311509,-99.180575);
insert into museos (Nombre,latitud,longitud) values ("Templo Mayor",19.434988,-99.131838);
insert into museos (Nombre,latitud,longitud) values ("Antiguo Colegio de San Idelfonso",19.436577,-99.130851);
insert into museos (Nombre,latitud,longitud) values ("Palacio Nacional",19.432641, -99.131194);
insert into museos (Nombre,latitud,longitud) values ("Museo Nacional del Arte",19.436395, -99.139445);
insert into museos (Nombre,latitud,longitud) values ("Museo del Estanquillo",19.433380, -99.136183);
insert into museos (Nombre,latitud,longitud) values ("Antiguo Palacio de Iturbide",19.433825, -99.139048);
insert into museos (Nombre,latitud,longitud) values ("Museo Franz Mayer",19.437224, -99.143329);
insert into museos (Nombre,latitud,longitud) values ("Museo de Memoria y Tolerancia",19.434412, -99.144595);
insert into museos (Nombre,latitud,longitud) values ("Museo Soumaya",19.440885, -99.204753);
insert into museos (Nombre,latitud,longitud) values ("Museo Casa del Risco",19.345031, -99.191909);
insert into museos (Nombre,latitud,longitud) values ("Museo de El Carmen",19.344890, -99.189860);
insert into museos (Nombre,latitud,longitud) values ("Museo de Arte Carrillo Gil",19.349698, -99.190310);
insert into museos (Nombre,latitud,longitud) values ("Museo Casa de León Trotsky",19.357978, -99.159347);
insert into museos (Nombre,latitud,longitud) values ("Museo de Historia Natural",19.410363, -99.201404);
insert into museos (Nombre,latitud,longitud) values ("Museo de Arte Moderno",19.423355, -99.179774);

CREATE TABLE conexiones (
       id_m1      INTEGER,
       id_m2      INTEGER,
       distancia       DOUBLE,
       PRIMARY KEY    (id_m1, id_m2),
       FOREIGN KEY    (id_m1) REFERENCES museos(MuseoId),
       FOREIGN KEY    (id_m2) REFERENCES museos(MuseoId)
);

Insert into conexiones (id_m1, id_m2,distancia) values (15, 16,2690.160928528786); 
Insert into conexiones (id_m1, id_m2,distancia) values (1, 11,3913.8229741328414); 
Insert into conexiones (id_m1, id_m2,distancia) values (1, 12,3838.7318668866915); 
Insert into conexiones (id_m1, id_m2,distancia) values (1, 13,4368.919908318641); 
Insert into conexiones (id_m1, id_m2,distancia) values (14, 13,3377.385621869986); 
Insert into conexiones (id_m1, id_m2,distancia) values (12, 13,536.874253590714); 
Insert into conexiones (id_m1, id_m2,distancia) values (11, 12,215.61358094745924); 
Insert into conexiones (id_m1, id_m2,distancia) values (11, 13,545.5601156258631); 
Insert into conexiones (id_m1, id_m2,distancia) values (14, 11,3708.2901916394535); 
Insert into conexiones (id_m1, id_m2,distancia) values (14, 15,7309.190604326924); 
Insert into conexiones (id_m1, id_m2,distancia) values (14, 16,7581.127123499147); 
Insert into conexiones (id_m1, id_m2,distancia) values (15, 10,3413.084649035193); 
Insert into conexiones (id_m1, id_m2,distancia) values (16, 10,3266.0513431504646); 
Insert into conexiones (id_m1, id_m2,distancia) values (9, 10,6350.928429946689); 
Insert into conexiones (id_m1, id_m2,distancia) values (9, 16,3889.6845859673317); 
Insert into conexiones (id_m1, id_m2,distancia) values (2, 3,204.83291430972847); 
Insert into conexiones (id_m1, id_m2,distancia) values (3, 4,439.2764543562214); 
Insert into conexiones (id_m1, id_m2,distancia) values (2, 4,269.65454849267496); 
Insert into conexiones (id_m1, id_m2,distancia) values (5, 6,479.0999988235459); 
Insert into conexiones (id_m1, id_m2,distancia) values (5, 7,288.877802237474); 
Insert into conexiones (id_m1, id_m2,distancia) values (5, 8,417.70061597250026); 
Insert into conexiones (id_m1, id_m2,distancia) values (3, 6,662.760080679652); 
Insert into conexiones (id_m1, id_m2,distancia) values (7, 8,587.0048840350177); 
Insert into conexiones (id_m1, id_m2,distancia) values (7, 6,304.5668955973115); 
Insert into conexiones (id_m1, id_m2,distancia) values (7, 9,585.4905395987138); 
Insert into conexiones (id_m1, id_m2,distancia) values (8, 9,339.80009501668843); 
Insert into conexiones (id_m1, id_m2,distancia) values (2, 7,767.2571909365163); 
