import csv, sys
from aid_directory import Data, read_csv

orgs_ref = Data(read_csv('../outputs/orgs-ref.csv')).cache()

orgs_variants = Data(read_csv('../outputs/orgs-variants.csv')).cache()

org_ref_map = dict()
for org in orgs_ref:
    org_ref_map[org['org_id']] = org

org_name_map = dict()
for org in orgs_variants:
    if org['org_name']:
        org_name_map.setdefault(org['org_name'].lower(), org['new_org_id'])

org_id_map = dict()
for org in orgs_variants:
    if org['org_id']:
        org_id_map.setdefault(org['org_id'].lower(), org['new_org_id'])

output = csv.DictWriter(sys.stdout, [
    'org_name',
    'org_id',
    'org_type',
    'org_type_code',
    'org_name',
    'org_id',
    'org_type',
    'org_type_code',
    'source',
    'activity_name',
    'activity_id',
    'is_humanitarian',
    'country_name',
    'country_code',
    'sector_name',
    'sector_code',
    'sector_type',
    'sector_type_code',
    'org_role',
    'relationship_index',
    'org_name_orig',
    'org_id_orig',
    'org_type_orig',
    'org_type_code_orig',
])

output.writeheader()

for org in Data(read_csv('../outputs/orgs.csv')):

    for attribute in ('org_name', 'org_id', 'org_type', 'org_type_code',):
        org[attribute + "_orig"] = org[attribute]
    
    # Fill in missing ids
    if not org['org_id'] and org['org_name'].lower() in org_name_map:
        org['org_id'] = org_name_map[org['org_name'].lower()]

    # Map variant ids
    key = org['org_id'].lower()
    if org['org_id'] and org['org_id'].lower() in org_id_map:
        org['org_id_orig'] = org['org_id']
        org['org_id'] = org_id_map[org['org_id'].lower()]
        
    # Normalise names
    ref = org_ref_map.get(org['org_id'], None)
    for attribute in ('org_name', 'org_id', 'org_type', 'org_type_code',):
        if ref is not None:
            org[attribute] = ref[attribute]

    output.writerow(org)
