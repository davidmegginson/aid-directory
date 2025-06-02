import json, mysql.connector, re, sys

TABLE_NAME_REGEX = r'^[a-zA-Z][a-zA-Z0-9_]+$'

from . import CONFIG

db = mysql.connector.connect (
    database=CONFIG.get('database_name', 'aid-directory'),
    host=CONFIG.get('database_host', 'localhost'),
    user=CONFIG.get('database_user'),
    password=CONFIG.get('database_password'),
    port=CONFIG.get('database_port', '3306'),
)


def load_taxonomy (table_name, data, vocabulary_code=None):
    cursor = db.cursor(dictionary=True)

    if not re.match(TABLE_NAME_REGEX, table_name):
        raise Exception("Invalid table name '%s'", table_name)

    vocabulary_ref = None
    if vocabulary_code:
        cursor.execute("SELECT id FROM SectorVocabularies WHERE code=%s", (vocabulary_code,))
        result = cursor.fetchone()
        vocabulary_ref = result['id']

    for row in data:
        if vocabulary_code is None:
            cursor.execute(
                "INSERT INTO {} (code, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)".format(table_name),
                (row['code'], row['name'],),
            )
        else:
            cursor.execute(
                "INSERT INTO {} (code, name, vocabulary_ref) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)".format(table_name),
                (row['code'], row['name'], vocabulary_ref,),
            )

    db.commit()


if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: {} TABLE_NAME FILE_PATH".format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) == 4:
        (table_name, file_path, vocabulary_code) = sys.argv[1:]
    else:
        (table_name, file_path, vocabulary_code) = sys.argv[1:] + [None,]

    with open(file_path, 'r') as stream:
        package = json.load(stream)
        load_taxonomy(table_name, package['data'], vocabulary_code)

        
