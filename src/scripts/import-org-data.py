import csv, json, mysql.connector, os.path, sys

from . import CONFIG

db = mysql.connector.connect (
    database=CONFIG.get('database_name', 'aid-directory'),
    host=CONFIG.get('database_host', 'localhost'),
    user=CONFIG.get('database_user'),
    password=CONFIG.get('database_password'),
    port=CONFIG.get('database_port', '3306'),
)


def get_cached (table_name, select_query, select_params, create_query=None, create_params=None,):
    """ Get a row from database, using a cached version if available """
    cache_key = (table_name,) + select_params
    if not cache_key in get_cached.cache:
        cursor = db.cursor(dictionary=True)
        cursor.execute(select_query, select_params)
        get_cached.cache[cache_key] = cursor.fetchone()
        if (get_cached.cache[cache_key] is None) and (create_query is not None):
            cursor.execute(create_query, create_params)
            cursor.execute("SELECT * FROM {} WHERE id=last_insert_id()".format(table_name))
            get_cached.cache[cache_key] = cursor.fetchone()

    return get_cached.cache[cache_key]

get_cached.cache = dict()


def get_org_type (row):
    # do not create on demand
    return get_cached(
        'OrgTypes',
        'SELECT * FROM OrgTypes WHERE code=%s',
        (row['org_type_code'],),
    )


def get_org_role (row):
    # do not create on demand
    return get_cached(
        'OrgRoles',
        'SELECT * FROM OrgRoles WHERE code=%s',
        (row['org_role_code'],),
    )


def get_country (row):
    # do not create on demand
    return get_cached(
        'Countries',
        'SELECT * FROM Countries WHERE code=%s',
        (row['country_code'],),
    )


def get_source (row):
    return get_cached(
        'Sources',
        'SELECT * FROM Sources where code=%s',
        (row['source'],),
        'INSERT INTO Sources (code, name) VALUES (%s, %s)',
        (row['source'], row['source'],),
    )


def get_activity (row):
    source = get_source(row)
    return get_cached(
        'ActivityView',
        'SELECT * FROM ActivityView WHERE source_ref=%s and code=%s',
        (source['id'], row['activity_id']),
        'INSERT INTO Activities (source_ref, code, name, is_humanitarian) VALUES (%s, %s, %s, %s)',
        (source['id'], row['activity_id'], row['activity_name'], row['is_humanitarian'],)
    )


def get_sector_vocabulary (row):
    # do not create on demand
    return get_cached(
        'SectorVocabularies',
        'SELECT * FROM SectorVocabularies WHERE code=%s',
        (row['sector_type_code'],),
    )


def get_sector (row):
    vocabulary = get_sector_vocabulary(row)
    if row['sector_type_code'] in ('98', '99',):
        return get_cached(
            'SectorView',
            'SELECT * FROM SectorView WHERE vocabulary_ref=%s AND code=%s',
            (vocabulary['id'], row['sector_code'],),
            'INSERT INTO Sectors (vocabulary_ref, code, name) VALUES (%s, %s, %s)',
            (vocabulary['id'], row['sector_code'], row['sector_name'],),
        )
    else:
        return get_cached(
            'SectorView',
            'SELECT * FROM SectorView WHERE vocabulary_ref=%s AND code=%s',
            (vocabulary['id'], row['sector_code'],),
        )
        

def get_org_instance (row):
    org_type = get_org_type(row)
    return get_cached(
        'OrgInstanceView',
        'SELECT * FROM OrgInstanceView WHERE (CODE IS NOT NULL AND CODE=%s) OR (CODE IS NULL AND type=%s AND name=%s)',
        (row['org_id'], org_type['id'], row['org_name'],),
        'INSERT INTO OrgInstances (code, type, name) VALUES (%s, %s, %s)',
        (row['org_id'], org_type['id'], row['org_name'],),
    )


def get_org_activity (row):
    activity = get_activity(row)
    org_instance = get_org_instance(row)
    sector = get_sector(row)
    country = get_country(row)
    org_role = get_org_role(row)
    if row['relationship_index'] == '':
        row['relationship_index'] = None
    return get_cached(
        'OrgActivityView',
        'SELECT * FROM OrgActivityView WHERE activity_ref=%s AND org_instance_ref=%s AND sector_ref=%s AND country_ref=%s AND org_role_ref=%s AND relationship_index=%s',
        (activity['id'], org_instance['id'], sector['id'], country['id'], org_role['id'], row['relationship_index'],),
        'INSERT INTO OrgActivities (activity_ref, org_instance_ref, sector_ref, country_ref, org_role_ref, relationship_index) VALUES (%s, %s, %s, %s, %s, %s)',
        (activity['id'], org_instance['id'], sector['id'], country['id'], org_role['id'], row['relationship_index'],),
    )


def import_data (stream):
    input = csv.DictReader(stream)
    for row in input:
        print(row)
        org_activity = get_org_activity(row)
    db.commit()

if __name__ == '__main__':

    with open('../outputs/orgs.csv', 'r') as stream:
        import_data(stream)
