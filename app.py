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
        "rice": "assets/default.png",
        "chicken": "assets/default.png",
        "yogurt": "assets/default.png"
    }

    for key in mapping:
        if key in name:
            return mapping[key]

    return "assets/default.png"


# ---------------- SAFE IMAGE ----------------
def show_image(path):
    if os.path.exists(path):
        st.image(path, width=70)
    else:
        st.image("https://via.placeholder.com/70", width=70)


# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center;'>🍳 Meal Moment</h1>
<p style='text-align: center; color: grey;'>Cook smarter. Shop instantly.</p>
""", unsafe_allow_html=True)

dish = st.text_input("🔍 What do you want to cook?", key="dish_input")

if "result" not in st.session_state:
    st.session_state.result = None

if "last_dish" not in st.session_state:
    st.session_state.last_dish = None

if dish and (
    st.session_state.last_dish != dish
    or st.button("Generate Cart")
):
    st.session_state.last_dish = dish
    st.session_state.result = generate_cart(dish)


# ---------------- MAIN ----------------
if st.session_state.result:

    result = st.session_state.result

    # ---------------- INGREDIENTS + STEPS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🥘 Ingredients")
        for item in result["ingredients"]:
            st.container()
            st.markdown(f"""
            <div style="padding:10px; border-radius:8px; background:#f5f5f5; margin-bottom:8px;">
                <b>{item['name']}</b><br>
                <span style="color:grey;">{item['quantity']}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("## 👨‍🍳 Cooking Steps")
        for i, step in enumerate(result["steps"], 1):
            st.markdown(f"""
            <div style="padding:10px; border-radius:8px; background:#f9f9f9; margin-bottom:8px;">
                <b>Step {i}</b><br>{step}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- CART ----------------
    st.markdown("## 🛒 Your Cart")

    available = [i for i in result["cart"] if i["product"] != "❌ Not available"]
    unavailable = [i for i in result["cart"] if i["product"] == "❌ Not available"]

    total = 0
    selected_items = []

    # ✅ PERFECT GRID (CONSISTENT)
    for i in range(0, len(available), 3):
        row = available[i:i+3]
        cols = st.columns(3)

        for j, item in enumerate(row):
            with cols[j]:

                with st.container():

                    st.markdown(
                        """
                        <div style="padding:12px; border-radius:12px; background:#f5f5f5;">
                        """,
                        unsafe_allow_html=True
                    )

                    show_image(get_image_path(item["product"]))

                    st.markdown(f"**{item['product']}**")
                    st.caption(item["quantity"])
                    st.markdown(f"💰 ₹{item['price']}")

                    checked = st.checkbox(
                        "Add",
                        value=True,
                        key=f"cart_{i}_{j}"
                    )

                    if checked:
                        total += item["price"]
                        selected_items.append(item)

                    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- UNAVAILABLE ----------------
    if unavailable:
        st.markdown("### ⚠️ Not Available")
        for item in unavailable:
            st.write(f"- {item['ingredient']}")

    st.markdown("---")

    # ---------------- SUMMARY ----------------
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🧾 Selected Items")
        for item in selected_items:
            st.write(f"✔ {item['product']}")

    with col2:
        st.markdown("### 💳 Total")
        st.markdown(f"<h2 style='color:green;'>₹ {total}</h2>", unsafe_allow_html=True)
