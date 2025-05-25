PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('0ddc960cfaf1');
CREATE TABLE authors (
	id INTEGER NOT NULL, 
	name VARCHAR(32) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO authors VALUES(1,'Mark');
INSERT INTO authors VALUES(2,'Petr');
CREATE TABLE quotes (
	id INTEGER NOT NULL, 
	author_id INTEGER NOT NULL, 
	text VARCHAR(255) NOT NULL, rating INTEGER DEFAULT '1' NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES authors (id)
);
INSERT INTO quotes VALUES(1,1,'Нет дыма без огня',2);
INSERT INTO quotes VALUES(2,1,'Mark''s quote',1);
INSERT INTO quotes VALUES(3,2,'Mark''s quote',1);
CREATE UNIQUE INDEX ix_authors_name ON authors (name);
COMMIT;
