import os

from .pipeline import *

package_directory = os.path.dirname(os.path.abspath(__file__))

org_file = os.path.join(package_directory, '../../outputs/orgs-norm.csv')
relationships_file = os.path.join(package_directory, '../../outputs/relationships.csv')


def get_orgs ():

    return Data(read_csv(org_file)).unique(('org_name', 'org_id', 'org_type', 'org_type_code')).cache()
    

def get_org (org_id):

    org = dict()

    data = Data(read_csv(org_file)).has('org_id', org_id).cache()

    org['id'] = org_id
    org['name'] = next(iter(data)).get('org_name')

    org['types'] = data.unique('org_type_orig')
    org['types'].discard('')

    org['aliases'] = data.unique('org_name_orig')
    org['aliases'].discard('')
    org['aliases'].discard(org['name'])

    org['alternative_ids'] = data.unique('org_id_orig')
    org['alternative_ids'].discard('')
    org['alternative_ids'].discard(org['id'])

    org['receivers'] = Data(read_csv(relationships_file)).has('provider_org_code', org_id).cache()
    org['providers'] = Data(read_csv(relationships_file)).has('receiver_org_code', org_id).cache()

    org['activities'] = data.unique(['activity_title', 'activity_id'])

    # operator.contains is in the wrong order :(
    activity_data = Data(read_csv('../outputs/orgs-norm.csv')).has('activity_id', org['activities'].unique('activity_id'), lambda x, y: x in y).cache()

    org['countries'] = data.unique(('country_name', 'country_code',))

    org['sectors'] = data.unique(['sector_name', 'sector_code', 'sector_type', 'sector_type_code']).cache()
    org['roles'] = data.unique('org_role')
    org['activities'] = activity_data
    org['partners'] = activity_data.has('org_id', org_id, negate=True).unique(('org_name', 'org_id', 'org_type', 'org_role',)).cache()

    return org



def get_sectors ():

    # Fixme add reporting org id for 98 and 99 vocabularies
    return Data(read_csv(org_file)).unique(['sector_name', 'sector_code', 'sector_type', 'sector_type_code']).cache()
    


def get_sector (sector_type_code, sector_code, org_id=None):

    sector = dict()

    # FIXME: wrong. Should always use reporting org id
    if org_id is None:
        data = Data(read_csv(org_file)).has('sector_type_code', sector_type_code).has('sector_code', sector_code).cache()
    else:
        data = Data(read_csv(org_file)).has('sector_type_code', sector_type_code).has('sector_code', sector_code).has('org_id', org_id).cache()

    sector['name'] = next(iter(data)).get('sector_name')
    sector['type'] = next(iter(data)).get('sector_type')
    sector['code'] = sector_code

    sector['aliases'] = data.unique('sector_name');
    sector['orgs'] = data.unique(['org_name', 'org_id', 'org_type', 'org_role']).cache()

    return sector


