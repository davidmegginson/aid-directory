import os

from .pipeline import *

package_directory = os.path.dirname(os.path.abspath(__file__))

org_file = os.path.join(package_directory, '../../outputs/orgs.csv')
relationships_file = os.path.join(package_directory, '../../outputs/relationships.csv')

def get_org (org_id):

    org = dict()

    data = Data(read_csv(org_file)).has('org_id', org_id).cache()

    org['id'] = org_id
    org['name'] = next(iter(data)).get('org_name')

    org['types'] = data.unique('org_type')

    org['aliases'] = data.unique('org_name')

    org['receivers'] = Data(read_csv(relationships_file)).has('provider_org_code', org_id).cache()
    org['providers'] = Data(read_csv(relationships_file)).has('receiver_org_code', org_id).cache()

    org['activities'] = data.unique(['activity_title', 'activity_id'])

    # operator.contains is in the wrong order :(
    activity_data = Data(read_csv('../outputs/orgs.csv')).has('activity_id', org['activities'].unique('activity_id'), lambda x, y: x in y).cache()

    org['countries'] = data.unique(('country_name', 'country_code',))

    org['sectors'] = data.unique(['sector_name', 'sector_code'])
    org['roles'] = data.unique('org_role')
    org['activities'] = activity_data
    org['partners'] = activity_data.has('org_id', org_id, negate=True).unique(('org_name', 'org_id', 'org_type', 'org_role',))

    return org


def get_orgs ():

    return Data(read_csv(org_file)).unique(('org_name', 'org_id', 'org_type'))
    
