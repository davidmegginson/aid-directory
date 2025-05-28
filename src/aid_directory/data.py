from . import app

import mysql.connector, os

from .pipeline import *

package_directory = os.path.dirname(os.path.abspath(__file__))

org_file = os.path.join(package_directory, '../../outputs/orgs-norm.csv')
relationships_file = os.path.join(package_directory, '../../outputs/relationships.csv')

def get_db ():
    if get_db.db is None:
        get_db.db = mysql.connector.connect(
            database='aid_directory',
            host='aid-directory-db',
            port='3306',
            user='root',
            password='dyhtt',
        )
    return get_db.db;

get_db.db = None

def get_cursor ():
    if get_cursor.cursor is None:
        get_cursor.cursor = get_db().cursor(dictionary=True)
    return get_cursor.cursor

get_cursor.cursor = None

def get_orgs ():
    get_cursor().execute("SELECT DISTINCT org_name, org_code, org_type_name, org_type_code FROM OrgActivityView")
    return Data(get_cursor().fetchall());
    
def get_org (org_code):

    org = dict()

    get_cursor().execute("SELECT * FROM OrgActivityView WHERE org_code=%s", (org_code,))
    data = Data(get_cursor().fetchall());

    org['code'] = org_code
    org['name'] = next(iter(data)).get('org_name')

    org['types'] = data.unique('org_type_name')
    org['types'].discard('')

    org['aliases'] = data.unique('org_name')
    org['aliases'].discard('')
    org['aliases'].discard(org['name'])

    org['activities'] = data.unique(['activity_title', 'activity_code'])

    # operator.contains is in the wrong order :(
    get_cursor().execute(
        "SELECT * FROM OrgActivityView WHERE activity_code IN (SELECT activity_code FROM OrgActivityView WHERE org_code=%s)",
        (org_code,)
    )
    activity_data = Data(get_cursor().fetchall())

    org['countries'] = data.unique(('country_name', 'country_code',))

    org['sectors'] = data.unique(['sector_name', 'sector_code', 'sector_vocabulary_name', 'sector_vocabulary_code']).cache()
    org['roles'] = data.unique('org_role_name')
    org['activities'] = activity_data
    org['partners'] = activity_data.has('org_code', org_code, negate=True).unique(('org_name', 'org_id', 'org_type', 'org_role',)).cache()

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


