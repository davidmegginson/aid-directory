import csv, json, mysql.connector, os.path, sys

from . import CONFIG

db = mysql.connector.connect (
    database=CONFIG.get('database_name', 'aid-directory'),
    host=CONFIG.get('database_host', 'localhost'),
    user=CONFIG.get('database_user'),
    password=CONFIG.get('database_password'),
    port=CONFIG.get('database_port', '3306'),
)

def get_cached (table_name, select_query, select_params, create_query, create_params):
    """ Get a row from database, using a cached version if available """
    cache_key = (table_name,) + select_params
    if not cache_key in get_cached.cache:
        cursor = db.cursor(dictionary=True)
        cursor.execute(select_query, select_params)
        get_cached.cache[cache_key] = cursor.fetchone()
        if get_cached.cache[cache_key] is None:
            cursor.execute(create_query, create_params)
            cursor.execute("SELECT * FROM {} WHERE id=last_insert_id()".format(table_name))
            get_cached.cache[cache_key] = cursor.fetchone()

    return get_cached.cache[cache_key]

get_cached.cache = dict()


def get_org_type (row):
    return get_cached(
        'OrgTypes',
        'SELECT * FROM OrgTypes WHERE code=%s',
        (row['org_type_code'],),
        'INSERT INTO OrgTypes (code, name) VALUES (%s, %s)',
        (row['org_type_code'], row['org_type']),
    )


def get_org_role (row):
    return get_cached(
        'OrgRoles',
        'SELECT * FROM OrgRoles WHERE code=%s',
        (row['org_role'],),
        'INSERT INTO OrgRoles (code, name) VALUES (%s, %s)',
        (row['org_role'], row['org_role'],)
    )


def get_country (row):
    return get_cached(
        'Countries',
        'SELECT * FROM Countries WHERE code=%s',
        (row['country_code'],),
        'INSERT INTO Countries (code, name) VALUES (%s, %s)',
        (row['country_code'], row['country_name'],)
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
        'Activities',
        'SELECT * FROM Activities WHERE source_ref=%s and code=%s',
        (source['id'], row['activity_id']),
        'INSERT INTO Activities (source_ref, code, name, is_humanitarian) VALUES (%s, %s, %s, %s)',
        (source['id'], row['activity_id'], row['activity_name'], row['is_humanitarian'],)
    )


def get_org_instance (row):
    org_type = get_org_type(row)
    return get_cached(
        'OrgInstances',
        'SELECT * FROM OrgInstances WHERE (CODE IS NOT NULL AND CODE=%s) OR (CODE IS NULL AND type=%s AND name=%s)',
        (row['org_id'], org_type['id'], row['org_name'],),
        'INSERT INTO OrgInstances (code, type, name) VALUES (%s, %s, %s)',
        (row['org_id'], org_type['id'], row['org_name'],),
    )


def import_data (stream):
    input = csv.DictReader(stream)
    for row in input:
        org_instance = get_org_instance(row)

if __name__ == '__main__':
    with open('../outputs/orgs.csv', 'r') as stream:
        import_data(stream)
        db.commit()
