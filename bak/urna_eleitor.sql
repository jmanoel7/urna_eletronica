BEGIN TRANSACTION;
DROP TABLE IF EXISTS "urna_eleitor";
CREATE TABLE IF NOT EXISTS "urna_eleitor" (
	"id"	integer NOT NULL,
	"nome"	varchar(100) NOT NULL UNIQUE,
	"data_nascimento"	date NOT NULL,
	"titulo_eleitor"	varchar(12) NOT NULL UNIQUE,
	"zona"	varchar(4) NOT NULL,
	"secao"	varchar(4) NOT NULL,
	"municipio"	varchar(100) NOT NULL,
	"uf"	varchar(2) NOT NULL,
	"data_emissao"	date NOT NULL,
	"urna_id"	bigint NOT NULL,
	FOREIGN KEY("urna_id") REFERENCES "urna_urna"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "urna_eleitor" ("id","nome","data_nascimento","titulo_eleitor","zona","secao","municipio","uf","data_emissao","urna_id") VALUES (1,'José Maria Nogueira Rodrigues','1981-04-10','002392100934','0035','0080','Goiânia','GO','2017-10-10',1),
 (2,'João Melo da Silva Júnior','1979-02-11','201200304698','0035','0080','Goiânia','GO','2000-09-11',1),
 (3,'Kaio da Silva Sampaio','2000-12-30','001230205000','0035','0080','Goiânia','GO','2018-07-03',1),
 (4,'Leila Azevedo','1990-01-01','000135871269','0035','0080','Goiânia','GO','1999-08-11',1),
 (5,'Mariana da Silva Neto','2001-05-03','099013279708','0035','0080','Goiânia','GO','1967-09-01',1),
 (6,'Kamila Vicente de Paula','1975-08-25','450025732870','0035','0080','Goiânia','GO','1998-06-22',1),
 (7,'João Nogueira','1983-10-01','000345912375','0035','0080','Goiânia','GO','2018-10-10',1),
 (8,'Sandra Ribeiro','1975-04-29','008927348620','0035','0080','Goiânia','GO','2019-01-10',1),
 (9,'Jair Messias Bolsonaro','1955-03-21','000812340987','0035','0080','Goiânia','GO','2020-03-01',1),
 (10,'Luiz Inácio Lula da Silva','1945-10-27','000643217890','0035','0080','Goiânia','GO','2021-04-09',1);
DROP INDEX IF EXISTS "urna_eleitor_urna_id_7b433076";
CREATE INDEX IF NOT EXISTS "urna_eleitor_urna_id_7b433076" ON "urna_eleitor" (
	"urna_id"
);
COMMIT;
