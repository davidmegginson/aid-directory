DROP VIEW IF EXISTS ActivityView;
DROP VIEW IF EXISTS SectorView;
DROP VIEW IF EXISTS OrgInstanceView;
DROP VIEW IF EXISTS OrgActivityView;

DROP TABLE IF EXISTS OrgActivities;
DROP TABLE IF EXISTS OrgInstances;
DROP TABLE IF EXISTS Orgs;
DROP TABLE IF EXISTS OrgTypes;
DROP TABLE IF EXISTS OrgRoles;
DROP TABLE IF EXISTS Countries;
DROP TABLE IF EXISTS Sectors;
DROP TABLE IF EXISTS SectorVocabularies;
DROP TABLE IF EXISTS Activities;
DROP TABLE IF EXISTS Sources;


CREATE TABLE Sources (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code VARCHAR(16) UNIQUE NOT NULL,
  name VARCHAR(128) NOT NULL
);

CREATE TABLE Activities (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  source_ref INT NOT NULL,
  code VARCHAR(512) UNIQUE NOT NULL,
  name TEXT NOT NULL,
  is_humanitarian BOOL DEFAULT FALSE,
  UNIQUE(source_ref, code),
  FOREIGN KEY (source_ref) REFERENCES Sources(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE SectorVocabularies (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code VARCHAR(32) UNIQUE NOT NULL,
  name VARCHAR(512) NOT NULL
);

CREATE TABLE Sectors (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code VARCHAR(256) NOT NULL,
  vocabulary_ref INT NOT NULL,
  name TEXT NOT NULL,
  UNIQUE(code, vocabulary_ref),
  FOREIGN KEY (vocabulary_ref) REFERENCES SectorVocabularies(id)
);

CREATE TABLE Countries (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code CHAR(2) UNIQUE NOT NULL,
  name VARCHAR(256) NOT NULL
);

CREATE TABLE OrgRoles (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code VARCHAR(16) UNIQUE NOT NULL,
  name VARCHAR(128) NOT NULL
);

-- Extra roles (not in IATI codelist)
INSERT INTO OrgRoles (code, name)
VALUES
('990', 'Reporting'),
('991', 'Provider'),
('992', 'Receiver'),
('999', '(Unspecified)');

CREATE TABLE OrgTypes (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code VARCHAR(8) UNIQUE NOT NULL,
  name VARCHAR(128) NOT NULL
);

CREATE TABLE Orgs (
  id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code VARCHAR(512) UNIQUE NOT NULL,
  type INT NOT NULL,
  name VARCHAR(1024) NOT NULL,
  FOREIGN KEY (type) REFERENCES OrgTypes(id)
);

CREATE TABLE OrgInstances (
  id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  code VARCHAR(128),
  type INT NOT NULL,
  name VARCHAR(256) NOT NULL,
  UNIQUE(code, type, name),
  FOREIGN KEY (type) REFERENCES OrgTypes(id)
);

CREATE TABLE OrgActivities (
  id INT PRIMARY KEY AUTO_INCREMENT,
  activity_ref INT NOT NULL,
  org_instance_ref INT NOT NULL,
  sector_ref INT NOT NULL,
  country_ref INT NOT NULL,
  org_role_ref INT NOT NULL,
  org_ref INT,
  relationship_index INT,
  UNIQUE(activity_ref, org_instance_ref, sector_ref, country_ref, org_role_ref, relationship_index),
  FOREIGN KEY (activity_ref) REFERENCES Activities(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (org_instance_ref) REFERENCES OrgInstances(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (sector_ref) REFERENCES Sectors(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (country_ref) REFERENCES Countries(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (org_role_ref) REFERENCES OrgRoles(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (org_ref) REFERENCES Orgs(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);


