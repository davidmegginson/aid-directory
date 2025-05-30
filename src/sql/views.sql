DROP VIEW IF EXISTS ActivityView;
DROP VIEW IF EXISTS SectorView;
DROP VIEW IF EXISTS OrgInstanceView;
DROP VIEW IF EXISTS OrgActivityView;

CREATE VIEW ActivityView AS
SELECT A.*, SR.code AS source_code, SR.name AS source_name
FROM Activities A
JOIN Sources SR ON A.source_ref=SR.id;

CREATE VIEW SectorView AS
SELECT S.*, V.code as vocabulary_code, V.name AS vocabulary_name
FROM Sectors S
JOIN SectorVocabularies V ON S.vocabulary_ref=V.id;

CREATE VIEW OrgInstanceView AS
SELECT OI.*, OT.code AS vocabulary_code, OT.name AS vocabulary_name
FROM OrgInstances OI
JOIN OrgTypes OT ON OI.type=OT.id;

CREATE VIEW OrgActivityView AS
SELECT OA.*,
  OI.code AS org_code, OI.name AS org_name,
  OT.id AS org_type_ref, OT.code AS org_type_code, OT.name AS org_type_name,
  A.code AS activity_code, A.name AS activity_name, A.is_humanitarian AS is_humanitarian,
  A.source_ref AS source_ref, SR.code AS source_code, SR.name AS source_name,
  S.code AS sector_code, S.name AS sector_name, S.vocabulary_ref AS sector_vocabulary_ref,
  V.code AS sector_vocabulary_code, V.name AS sector_vocabulary_name,
  ORL.code AS org_role_code, ORL.name AS org_role_name,
  ORG.code AS norm_org_code, ORG.name AS norm_org_name, ORG.type AS norm_org_type_code, ORGT.name AS norm_org_type_name
FROM OrgActivities OA
JOIN Activities A ON OA.activity_ref=A.id
JOIN OrgInstances OI ON OA.org_instance_ref=OI.id
JOIN Sources SR ON A.source_ref=SR.id
JOIN Sectors S ON OA.sector_ref=S.id
JOIN SectorVocabularies V ON S.vocabulary_ref=V.id
JOIN OrgRoles ORL ON OA.org_role_ref=ORL.id
LEFT JOIN OrgTypes OT ON OI.type=OT.id
LEFT JOIN Orgs ORG ON OA.org_ref=ORG.id
LEFT JOIN OrgTypes ORGT on ORG.type=ORGT.id;

