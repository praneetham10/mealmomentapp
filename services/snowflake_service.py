import streamlit as st
import snowflake.connector


def get_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["SNOWFLAKE_USER"],
        account=st.secrets["SNOWFLAKE_ACCOUNT"],
        warehouse=st.secrets["SNOWFLAKE_WAREHOUSE"],
        database=st.secrets["SNOWFLAKE_DATABASE"],
        schema=st.secrets["SNOWFLAKE_SCHEMA"],
        role=st.secrets["SNOWFLAKE_ROLE"],
        authenticator="externalbrowser"
    )

        return conn

    except Exception as e:
        st.error(f"Snowflake connection failed: {str(e)}")
        raise


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
