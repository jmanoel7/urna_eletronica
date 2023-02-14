BEGIN TRANSACTION;
DROP TABLE IF EXISTS "urna_politico";
CREATE TABLE IF NOT EXISTS "urna_politico" (
	"id"	integer NOT NULL,
	"politico"	varchar(100) NOT NULL UNIQUE,
	"foto"	varchar(100) NOT NULL UNIQUE,
	"partido"	varchar(10) NOT NULL,
	"num_partido"	varchar(2) NOT NULL,
	"cargo"	varchar(50) NOT NULL,
	"urna_id"	bigint NOT NULL,
	FOREIGN KEY("urna_id") REFERENCES "urna_urna"("id") DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT "cargo_unico" UNIQUE("partido","num_partido","cargo"),
	PRIMARY KEY("id" AUTOINCREMENT),
	CONSTRAINT "politico_unico" UNIQUE("politico","partido","num_partido","cargo")
);
INSERT INTO "urna_politico" ("id","politico","foto","partido","num_partido","cargo","urna_id") VALUES (1,'Branco','branco.png','BRANCO','00','Presidente da República',1),
 (2,'Nulo','nulo.png','NULO','99','Presidente da República',1),
 (3,'Lula','Lula.png','PT','13','Presidente da República',1),
 (4,'Bolsonaro','Bolsonaro.png','PL','22','Presidente da República',1);
DROP INDEX IF EXISTS "urna_politico_urna_id_3c4ef0c2";
CREATE INDEX IF NOT EXISTS "urna_politico_urna_id_3c4ef0c2" ON "urna_politico" (
	"urna_id"
);
COMMIT;
