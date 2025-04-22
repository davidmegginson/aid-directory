import os

from .pipeline import *

package_directory = os.path.dirname(os.path.abspath(__file__))

org_file = os.path.join(package_directory, '../../outputs/orgs.csv')
relationships_file = os.path.join(package_directory, '../../outputs/relationships.csv')

def get_org (org_id):

    org = dict()

    data = pipe(
        read_csv(org_file),
        lambda x: filter(x, 'org_id', org_id),
        lambda x: list(x),
    )

    org['id'] = org_id
    if len(data) > 0:
        org['name'] = data[0].get('org_name') # fixme: multiple names?
        org['type'] = data[0].get('org_type') # fixme: multiple types?

    org['receivers'] = pipe(
        read_csv(relationships_file),
        lambda x: filter(x, 'provider_org_code', org_id),
        lambda x: list(x),
    )

    org['providers'] = pipe(
        read_csv(relationships_file),
        lambda x: filter(x, 'receiver_org_code', org_id),
        lambda x: list(x),
    )

    org['activities'] = unique(data, ['activity_title', 'activity_id'])
    activity_data = pipe(
        read_csv('../outputs/orgs.csv'),
        lambda x: filter(x, 'activity_id', [activity['activity_id'] for activity in org['activities']]),
        lambda x: list(x),
    )

    org['countries'] = pipe(
        data,
        lambda x: unique(x, ['country_name', 'country_code']),
    )


    org['sectors'] = unique(data, ['sector_name', 'sector_code'])
    org['roles'] = unique(data, 'org_role')
    org['activities'] = activity_data
    org['partners'] = pipe(
        activity_data,
        lambda x: filter(x, 'org_id', org_id, True),
        lambda x: unique(x, ['org_name', 'org_id', 'org_type', 'org_role']),
    )

    return org


def get_orgs ():

    return pipe(
        read_csv(org_file),
        lambda x: unique(x, ('org_name', 'org_id', 'org_type')),
    )
    
