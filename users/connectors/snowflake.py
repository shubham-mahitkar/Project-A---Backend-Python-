import snowflake.connector
import os


USER = os.getenv('SNOWSQL_USER')
PASSWORD = os.getenv('SNOWSQL_PWD')
ACCOUNT = os.getenv('SNOWSQL_ACCOUNT')

connection = None
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT
    )

connection = conn.cursor()
