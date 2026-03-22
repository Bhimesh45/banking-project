import oracledb

def get_connection():
    connection = oracledb.connect(
        user="banking_db",
        password="bhimesh",
        dsn="localhost:1521/orclpdb"
    )
    return connection