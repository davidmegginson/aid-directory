""" Import the latest canonical name for each reporting org
Give authority to what the orgs called themselves most recently.

"""

import csv, sys

def import_canonical_orgs (input):

    data = dict()
    
    data_in = csv.DictReader(input)
    for row in data_in:
        if row['org_role'] == 'Reporting':
            data[row['org_id']] = (row['org_name'], row['org_type_code'])

    for id in data:
        print(id, data[id])


if __name__ == '__main__':
    data_file = sys.argv[1]
    with open(data_file, 'r') as input:
        import_canonical_orgs(input)
