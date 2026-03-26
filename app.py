import streamlit as st
from core.orchestrator import generate_cart
import os

st.set_page_config(page_title="Meal Moment", layout="wide")

# ---------------- IMAGE MAPPING ----------------
def get_image_path(product_name):
    name = product_name.lower()

    mapping = {
        "onion": "assets/onion.png",
        "tomato": "assets/tomato.png",
        "paneer": "assets/paneer.png",
        "butter": "assets/butter.png",
        "milk": "assets/milk.png",
        "cream": "assets/milk.png",
        "oil": "assets/oil.png",
        "spice": "assets/spices.png",
        "masala": "assets/spices.png",
        "chili": "assets/chili.png",
        "turmeric": "assets/turmeric.png",
        "cashew": "assets/cashew.png",
    }

    for key in mapping:
        if key in name:
            return mapping[key]

    return "assets/default.png"

# ---------------- SAFE IMAGE ----------------
def show_image(path):
    if os.path.exists(path):
        st.image(path, width=80)
    else:
        st.image("https://via.placeholder.com/80", width=80)

# ---------------- HEADER ----------------
st.title("🍳 Meal Moment")
st.caption("Cook smarter. Shop instantly.")

dish = st.text_input("🔍 What do you want to cook?")

if "result" not in st.session_state:
    st.session_state.result = None

if "last_dish" not in st.session_state:
    st.session_state.last_dish = None

if dish and (st.session_state.last_dish != dish or st.button("Generate Cart")):
    st.session_state.last_dish = dish
    st.session_state.result = generate_cart(dish)

# ---------------- MAIN ----------------
if st.session_state.result:

    result = st.session_state.result

    # ---------- INGREDIENTS + STEPS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🥘 Ingredients")
        for item in result["ingredients"]:
            st.write(f"**{item['name']}**")
            st.caption(item["quantity"])
            st.divider()

    with col2:
        st.subheader("👨‍🍳 Cooking Steps")
        for i, step in enumerate(result["steps"], 1):
            st.write(f"**Step {i}**")
            st.write(step)
            st.divider()

    st.divider()

    # ---------- CART ----------
    st.subheader("🛒 Your Cart")

    available = []
    unavailable = []

    for item in result["cart"]:
        if item["product"] != "❌ Not available":
            available.append(item)
        else:
            unavailable.append(item)

    total = 0
    selected_items = []

    # ✅ CLEAN GRID (NO HTML)
    for i in range(0, len(available), 3):
        row = available[i:i+3]
        cols = st.columns(3)

        for j, item in enumerate(row):
            with cols[j]:

                show_image(get_image_path(item["product"]))

                st.write(f"**{item['product']}**")
                st.caption(item["quantity"])
                st.write(f"💰 ₹{item['price']}")

                checked = st.checkbox(
                    "Add",
                    value=True,
                    key=f"cart_{i}_{j}"
                )

                if checked:
                    total += item["price"]
                    selected_items.append(item)

    # ---------- UNAVAILABLE ----------
    if unavailable:
        st.warning("Some items not available")
        for item in unavailable:
            st.write(f"- {item['ingredient']}")

    st.divider()

    # ---------- SUMMARY ----------
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🧾 Selected Items")
        for item in selected_items:
            st.write(f"✔ {item['product']}")

    with col2:
        st.subheader("💳 Total")
        st.success(f"₹ {total}")
