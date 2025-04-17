import csv, sys


def read_relationships (input):
    """ Reconstruct provider/receiver relationships from the raw org data
    """
    
    relationships = {}
    
    for org in input:

        activity_key = (org['country_code'], org['sector_code'], org['sector_type'], org['activity_id'],)

        relationship_index = org['relationship_index']

        if relationship_index == '':
            continue

        if not activity_key in relationships:
            relationships[activity_key] = {}

        if not relationship_index in relationships[activity_key]:
            relationships[activity_key][relationship_index] = {}

        relationships[activity_key][relationship_index][org['org_role']] = org

    return relationships


def write_relationships (output, relationships):
    """ Write the relationships with a single row for each one
    """

    output.writerow([
        'provider_org_name',
        'provider_org_code',
        'receiver_org_name',
        'receiver_org_code',
        'activity_name',
        'activity_id',
        'is_humanitarian',
        'country_name',
        'country_code',
        'sector_name',
        'sector_code',
        'sector_type',
    ])

    for activity in relationships.values():
        for relationship in activity.values():
            provider = relationship.get('Provider')
            receiver = relationship.get('Receiver')
            if provider and receiver:
                output.writerow([
                    provider['org_name'],
                    provider['org_id'],
                    receiver['org_name'],
                    receiver['org_id'],
                    provider['activity_name'],
                    provider['activity_id'],
                    provider['is_humanitarian'],
                    provider['country_name'],
                    provider['country_code'],
                    provider['sector_name'],
                    provider['sector_code'],
                    provider['sector_type'],
                ])
                

#
# Called from command line
#
if __name__ == '__main__':
    input = csv.DictReader(sys.stdin)
    output = csv.writer(sys.stdout)

    write_relationships(output, read_relationships(input))
