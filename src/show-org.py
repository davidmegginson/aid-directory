import csv

ORG = 'UNICEF'

def read_csv(path):
    with open(path, 'r') as file:
        input = csv.DictReader(file)
        for row in input:
            yield row


def filter(source, name, values, invert=False):
    if type(values) == type(''):
        values = (values,)
    for row in source:
        if (not invert and row[name] in values):
            yield row
        elif (invert and row[name] not in values):
            yield row


def unique(source, name, include_empty=False):
    result = set()
    for row in source:
        if (include_empty or row[name]):
            result.add(row[name])
    return result


print(ORG, "\n")

data = list(filter(filter(read_csv('../outputs/orgs.csv'), 'org_name', ORG), 'country_name', 'Madagascar'))

receivers = list(filter(read_csv('../outputs/relationships.csv'), 'provider_org_name', ORG))
providers = list(filter(read_csv('../outputs/relationships.csv'), 'receiver_org_name', ORG))

activities = unique(data, 'activity_id')
activity_data = list(filter(read_csv('../outputs/orgs.csv'), 'activity_id', activities))

print("\nCountries:\n- ", "\n- ".join(sorted(unique(data, 'country_name'))))
print("\nSectors:\n- ", "\n- ".join(sorted(unique(data, 'sector_name'))))
print("\nRoles:", ", ".join(sorted(unique(data, 'org_role'))))
print("\nActivities:", ", ".join(sorted(activities)))
print("\nPartners:\n- ", "\n- ".join(sorted(unique(filter(activity_data, 'org_name', ORG, True), 'org_name'))))
print("\nFunding from:", ", ".join(sorted(unique(providers, 'provider_org_name'))))
print("\nFunding to:", ", ".join(sorted(unique(receivers, 'receiver_org_name'))))
