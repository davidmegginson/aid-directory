import csv

ORG = 'Netherlands Ministry of Foreign Affairs'


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


def unique(source, name):
    result = set()
    for row in source:
        result.add(row[name])
    return result


print(ORG, "\n")


data = list(filter(filter(read_csv('../outputs/orgs.csv'), 'org_name', ORG), 'country_name', 'Madagascar'))

activities = unique(data, 'activity_id')
activity_data = list(filter(read_csv('../outputs/orgs.csv'), 'activity_id', activities))

print("Countries:", ", ".join(sorted(unique(data, 'country_name'))))
print("Sectors:", ", ".join(sorted(unique(data, 'sector_name'))))
print("Roles:", ", ".join(sorted(unique(data, 'org_role'))))
print("Activities:", ", ".join(sorted(activities)))
print("Partners:", ", ".join(sorted(unique(filter(activity_data, 'org_name', ORG, True), 'org_name'))))
