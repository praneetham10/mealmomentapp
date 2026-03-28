import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        account="YOUR_ACCOUNT_IDENTIFIER",  # e.g. abc-xy12345
        warehouse="COMPUTE_WH",
        database="MEAL_APPTEST",
        schema="PUBLIC"
    )


def fetch_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT NAME, PRICE FROM PRODUCTS")

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
