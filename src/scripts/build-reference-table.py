import csv, sys
from aid_directory.pipeline import Data, read_csv

def get_max (rows, key='_count'):
    """ Get the row with the maximum value for key """
    max = None
    for row in rows:
        if max is None or row[key] > max[key]:
            max = row
    return row
        
name_variants = Data(read_csv('../inputs/all_org_variants_expanded.csv')).cache()

raw_orgs = Data(read_csv('../outputs/orgs.csv')).cache()

raw_org_map = dict()
for org in raw_orgs.count(('org_name', 'org_id', 'org_type', 'org_type_code',)):
    if org['org_name'] and org['org_id'] and org['org_type']:
        raw_org_map.setdefault(org['org_id'], []).append(org)

# reduce to the most-common name for each org
orgs = list()
for rows in raw_org_map.values():
    orgs.append(get_max(rows))

output = csv.DictWriter(sys.stdout, ['org_name', 'org_id', 'org_type', 'org_type_code',], extrasaction='ignore')
output.writeheader()
for org in sorted(orgs, key=lambda a: a['org_name']):
    output.writerow(org)
        
    
