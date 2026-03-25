import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )


def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT NAME, CATEGORY FROM PRODUCTS")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"name": r[0], "category": r[1]} for r in rows]