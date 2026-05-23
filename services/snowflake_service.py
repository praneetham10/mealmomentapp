import snowflake.connector


def get_connection():

    conn = snowflake.connector.connect(
        user="YOUR_SNOWFLAKE_USER",
        account="YOUR_ACCOUNT",
        warehouse="COMPUTE_WH",
        database="MEAL_APPTEST",
        schema="PUBLIC",
        role="ACCOUNTADMIN",
        authenticator="externalbrowser"
    )

    return conn


def fetch_products():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT NAME, PRICE
        FROM PRODUCTS
    """)

    rows = cursor.fetchall()

    products = []

    for row in rows:

        products.append({
            "name": row[0].lower(),
            "price": row[1]
        })

    cursor.close()
    conn.close()

    return products
