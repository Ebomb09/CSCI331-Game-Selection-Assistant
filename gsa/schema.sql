DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS collection;

CREATE TABLE user (
	id 			INTEGER NOT NULL,
	email		TEXT UNIQUE NOT NULL,
	password 	TEXT NOT NULL,
	name 		TEXT NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE game (
	id			INTEGER UNIQUE NOT NULL,
	name 		TEXT NOT NULL,
	description TEXT,
	tags		TEXT,
	image_url,	TEXT,
	playtime	REAL,

	PRIMARY KEY (id)
);

CREATE TABLE collection (
	gameId 		INTEGER NOT NULL,
	userId 		INTEGER NOT NULL,
	dateAdded	INTEGER NOT NULL,
	rating		INTEGER,
	completed	INTEGER,

	FOREIGN KEY (userId) REFERENCES user(id),
	FOREIGN KEY (gameId) REFERENCES game(id),
	PRIMARY KEY (gameId, userId)
);
