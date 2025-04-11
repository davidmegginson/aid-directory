""" Demonstrate extracting IATI organisation information from D-Portal

TODO:
- fill in missing countries and sector names
- maybe handle regions
- make search country configurable
- maybe switch to IATI Datastore
- extend beyond active activities

"""

import csv, json, sys
from diterator import Iterator

ROLES = {
    '1': 'Funding',
    '2': 'Accountable',
    '3': 'Extending',
    '4': 'Implementing',
}
""" IATI org role codelist """

country_map = None

sector_map = None

def is_humanitarian (activity):
    if activity.humanitarian:
        return True
    for transaction in activity.transactions:
        if transaction.humanitarian:
            return True;
    for sector in activity.sectors:
        if sector.vocabulary == 1 and (sector.code.startswith('720') or sector.code.startswith('730') or sector.code.startswith('740') or sector.code == '43060'):
            return True
    return False;

def load_codelist (path):
    codelist = dict()
    with open(path, 'r') as input:
        data = json.load(input)
        for item in data['data']:
            codelist[item['code']] = item['name']
    return codelist

def get_country_map ():
    global country_map
    if country_map is None:
        country_map = load_codelist("../inputs/Country.json")
    return country_map

def get_sector_map ():
    global sector_map
    if sector_map is None:
        sector_map = load_codelist("../inputs/SectorCategory.json")
    return sector_map

def reduce_transactions (activity):
    """ Reduce an IATI activity's transaction to a list of unique org pairs
    Each pair represents a provider/receiver relationship (1 or more transactions)
    """

    def org2tuple (org):
        if org is None:
            return None
        k1 = str(org.name) if org.name else None
        k2 = str(org.ref) if org.ref else None
        return (k1, k2,)
    
    relationships = dict()

    for transaction in activity.transactions:
        provider = transaction.provider_org
        receiver = transaction.receiver_org
        if provider or receiver:
            relationships[(org2tuple(provider), org2tuple(receiver),)] = [provider, receiver]

    return relationships.values()
        

def show_org (output, org, activity, country, sector, default_role='', relationship_index=''):

    if "USAID redacted" in str(org.name):
        return;

    country_name = str(country.narrative)
    if not country_name:
        country_name = get_country_map().get(country.code, '')

    sector_code = sector.code
    if sector.vocabulary == '1':
        sector_code = sector_code[:3]

    sector_name = str(sector.narrative)
    if not sector_name and sector.vocabulary == '1':
        sector_name = get_sector_map().get(sector_code, '')

    humanitarian = "1" if is_humanitarian(activity) else "0"
    
    output.writerow([
        org.name,
        org.ref,
        'iati',
        activity.title,
        activity.identifier,
        humanitarian,
        country_name,
        country.code,
        sector_name,
        sector_code,
        sector.vocabulary,
        ROLES.get(org.role) if org.role else default_role,
        relationship_index,
    ])


def show_activity (output, activity):

    for country in activity.recipient_countries:

        for sector in activity.sectors:
    
            """ Display an activity to standard output """
            show_org(output, activity.reporting_org, activity, country, sector, 'Reporting')

            for org in activity.participating_orgs:
                show_org(output, org, activity, country, sector)

            relationships = reduce_transactions(activity)
            for (n, relationship) in enumerate(relationships):
                if relationship[0]:
                    show_org(output, relationship[0], activity, country, sector, 'Provider', n)
                if relationship[1]:
                    show_org(output, relationship[1], activity, country, sector, 'Receiver', n)

            
def show_activities (activities):
    """ Display a list of activities to standard output """
    output = csv.writer(sys.stdout)
    output.writerow([
        'org_name',
        'org_id',
        'source',
        'activity_name',
        'activity_id',
        'is_humanitarian',
        'country_name',
        'country_code',
        'sector_name',
        'sector_code',
        'sector_type',
        'org_role',
        'relationship_index',
    ])
    for activity in activities:
        show_activity(output, activity)


# Main entry point

activities = Iterator({
    "country_code": "mg", # Kenya
    "status_code": "2",   # implementation
})
show_activities(activities)
