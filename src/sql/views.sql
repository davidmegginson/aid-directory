DROP VIEW IF EXISTS SectorView;

CREATE VIEW SectorView AS
SELECT S.*, V.code as vocabulary_code, V.name AS vocabulary_name
FROM Sectors S
JOIN SectorVocabularies V ON S.vocabulary_ref=V.id;
