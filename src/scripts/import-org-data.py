import csv, json, mysql.connector, os.path, sys

from . import CONFIG

db = mysql.connector.connect (
    database=CONFIG.get('database_name', 'aid-directory'),
    host=CONFIG.get('database_host', 'localhost'),
    user=CONFIG.get('database_user'),
    password=CONFIG.get('database_password'),
    port=CONFIG.get('database_port', '3306'),
)

CODE_TABLES = (
    'OrgTypes',
    'Countries',
    'Roles',
    'SectorVocabularies',
)

def get_coded (table, code, name):
    """ Look up a coded metadata item, creating it if necessary """

    # security check
    if not table in CODE_TABLES:
        raise Exception("Unknown code table {}".format(table))

    # cache key
    key = (table, code,)

    # database lookup if not in cache
    if not key in get_coded.cache:
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM {} WHERE code=%s".format(table),
            (code,)
        )
        get_coded.cache[key] = cursor.fetchone()

        # create if not in database
        if get_coded.cache[key] is None:
            cursor.execute(
                "INSERT INTO {} (code, name) VALUES (%s, %s)".format(table),
                (code, name),
            )
            cursor.execute(
                "SELECT * FROM {} WHERE id=last_insert_id()".format(table)
            )
            get_coded.cache[key] = cursor.fetchone()

    return get_coded.cache[key]


get_coded.cache = dict()


def get_sector (sector_code, sector_name, sector_type_code, sector_type):

    key = (sector_code, str(sector_type_code),)

    if not key in get_sector.cache:

        # make sure we have the vocabulary
        sector_vocabulary = get_coded('SectorVocabularies', sector_type_code, sector_type)
        print(sector_vocabulary)
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM Sectors WHERE code=%s and vocabulary_ref=%s",
            (sector_code, sector_vocabulary['id'],)
        )
        get_sector.cache[key] = cursor.fetchone()
        if get_sector.cache[key] is None:
            cursor.execute(
                "INSERT INTO Sectors (code, name, vocabulary_ref) VALUES (%s, %s, %s)",
                (sector_code, sector_name, sector_vocabulary['id'],)
            )
            cursor.execute(
                "SELECT * FROM Sectors WHERE id=last_insert_id()"
            )
            get_sector.cache[key] = cursor.fetchone()

    return get_sector.cache[key]


get_sector.cache = dict()


def import_data (stream):
    input = csv.DictReader(stream)
    for row in input:
        org_type = get_coded('OrgTypes', row['org_type_code'], row['org_type'])
        country = get_coded('Countries', row['country_code'], row['country_name'])
        role = get_coded('Roles', row['org_role'], row['org_role'])
        sector = get_sector(row['sector_code'], row['sector_name'], row['sector_type_code'], row['sector_type'])
        print(org_type, country, role, sector)

if __name__ == '__main__':
    with open('../outputs/orgs.csv', 'r') as stream:
        import_data(stream)
        db.commit()
