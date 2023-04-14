-- PostgreSQL code for the current schema layout of AltBot.
-- When AltBot gets deployed, this should not change much, and all updates will be appended as SQL 'ALTER' code where applicable.

CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(32) NOT NULL
);

CREATE TABLE devices (
    user_id BIGINT,
    device_name VARCHAR(15) NOT NULL,
    device_version VARCHAR(50) NOT NULL,
    device_ecid VARCHAR,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE update_channels (
    channel_id BIGINT NOT NULL
);

CREATE TABLE sources (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(200) NOT NULL
);

CREATE TABLE apps (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    source VARCHAR(100) NOT NULL,
    FOREIGN KEY(source) REFERENCES sources(id)
);

CREATE TABLE ping_roles (
    guild_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    appbundle_id VARCHAR(100) NOT NULL
);

CREATE TABLE tags (
    name VARCHAR(32) PRIMARY KEY,
    tag VARCHAR(4000) NOT NULL,
    section VARCHAR(15)
);

CREATE TABLE annoys (
    name VARCHAR(200) NOT NULL,
    content VARCHAR(4000)
);

CREATE TYPE skin_type AS ENUM ('edgeToEdge', 'standard', 'both');

CREATE TABLE skins (
    name VARCHAR(50) PRIMARY KEY,
    creator VARCHAR(32) NOT NULL,
    console VARCHAR(30) NOT NULL,
    supported skin_type NOT NULL,
    url VARCHAR(200) NOT NULL
);

CREATE TABLE role_menus (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	placeholder VARCHAR(100),
	guild BIGINT NOT NULL,
	max_choice INT NOT NULL DEFAULT 1 CHECK (max_choice >= 1 AND max_choice <= 25),
	UNIQUE (guild, name)
);

CREATE TABLE menu_messages (
	id BIGINT PRIMARY KEY,
	channel BIGINT NOT NULL,
	menu INT REFERENCES role_menus(id) ON DELETE CASCADE,
	UNIQUE (id, channel),
	UNIQUE (id, menu)
);

CREATE TABLE roles (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    guild BIGINT NOT NULL,
    menu INTEGER NULL REFERENCES role_menus(id) ON DELETE SET NULL,
    description VARCHAR(100),
    emoji VARCHAR(5),
    UNIQUE (guild, id),
    UNIQUE (menu, id),
    UNIQUE (menu, name)
);

CREATE VIEW role_menu_info AS
 SELECT rm.id AS mid,
    rm.name AS mname,
    rm.placeholder AS mplaceholder,
    rm.guild AS mguild,
    rm.max_choice AS mmchoice,
    r.id AS rid,
    r.name AS rname,
    r.description AS rdesc,
    r.emoji AS remoji
   FROM (public.role_menus rm
     JOIN public.roles r ON ((r.menu = rm.id)));
