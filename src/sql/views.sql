DROP VIEW IF EXISTS ActivityView;
DROP VIEW IF EXISTS SectorView;

CREATE VIEW ActivityView AS
SELECT A.*, SR.code AS source_code, SR.name AS source_name
FROM Activities A
JOIN Sources SR ON A.source_ref=SR.id;

CREATE VIEW SectorView AS
SELECT S.*, V.code as vocabulary_code, V.name AS vocabulary_name
FROM Sectors S
JOIN SectorVocabularies V ON S.vocabulary_ref=V.id;
