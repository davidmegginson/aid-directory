""" Demonstrate extracting IATI organisation information from D-Portal

TODO:

- maybe handle regions
- make search country configurable
- maybe switch to IATI Datastore
- extend beyond active activities

"""

import csv, json, sys
from diterator import Iterator


CODELISTS = dict()
""" Global cache of loaded IATI codelists
"""


def get_codelist (name):
    """ Load a codelist the first time it's used, then cache it.
    """
    
    global CODELISTS

    if not name in CODELISTS:
        codelist = dict()
        path = "../inputs/{}.json".format(name)
        with open(path, 'r') as input:
            data = json.load(input)
            for item in data['data']:
                codelist[item['code']] = item['name']
        CODELISTS[name] = codelist

    return CODELISTS[name]


def is_humanitarian (activity):
    """ Test if an IATI activity appears to be humanitarian

    True if any of the following applies:
    
    1. Humanitarian flag is set on the activity
    2. Humanitarian flag is set on any transaction
    3. The humanitarian_scope element is present
    4. A DAC sector code in the 720, 730, or 740 series is present
    5. The DAC sector code 43060 is present
    6. A sector in the vocabulary '10' (Humanitarian Global Clusters) is present
    
    """
    
    if activity.humanitarian or len(activity.humanitarian_scopes) > 0:
        return True
    for transaction in activity.transactions:
        if transaction.humanitarian:
            return True;
    for sector in activity.sectors:
        if sector.vocabulary == '1' and (sector.code.startswith('720') or sector.code.startswith('730') or sector.code.startswith('740') or sector.code == '43060'):
            return True
        elif sector.vocabulary == '10':
            return True
    return False;


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
    """ Write a data row to the CSV output
    """

    # USAID redacts a lot of org info; skip that
    if "USAID redacted" in str(org.name):
        return;

    # Fill in the country name from default codelist if not supplied
    country_name = str(country.narrative)
    if not country_name:
        country_name = get_codelist('Country').get(country.code, '')

    # if the sector vocabulary is DAC, roll up to 3-digit category codes
    sector_code = sector.code
    sector_vocabulary = sector.vocabulary
    if sector_vocabulary == '1':
        sector_vocabulary = '2'
        sector_code = sector_code[:3]

    # fill in the sector name from default codelist if not supplied
    sector_name = str(sector.narrative)
    if not sector_name and sector.vocabulary == '1':
        sector_name = get_codelist('SectorCategory').get(sector_code, '')

    # write a row of CSV data
    output.writerow([
        org.name,
        org.ref,
        get_codelist('OrganisationType').get(org.type) if org.type else '',
        'iati',
        activity.title,
        activity.identifier,
        "1" if is_humanitarian(activity) else "0",
        country_name,
        country.code,
        sector_name,
        sector_code,
        get_codelist('SectorVocabulary').get(sector_vocabulary, ''),
        get_codelist('OrganisationRole').get(org.role, '') if org.role else default_role,
        relationship_index,
    ])


def show_activity (output, activity):
    """ Show all of the org info for an IATI activity
    Includes a separate row for each country/sector/org/role/relationship combo
    """

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

            
def show_activities (activities, file=None):
    """ Display a list of activities (defaults to standard output) """

    if file is None:
        file = sys.stdout

    output = csv.writer(file)
    
    # CSV headers
    output.writerow([
        'org_name',
        'org_id',
        'org_type',
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

    # CSV data rows
    for activity in activities:
        show_activity(output, activity)


# Main entry point

activities = Iterator({
    "country_code": "mg", # Kenya
    "status_code": "2",   # implementation
})
show_activities(activities)
