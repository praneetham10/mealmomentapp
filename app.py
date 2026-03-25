import streamlit as st
from core.orchestrator import generate_cart

st.set_page_config(page_title="Meal Moment", layout="wide")

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

# Trigger
if dish and (
    st.session_state.last_dish != dish
    or st.button("Generate Cart")
):
    st.session_state.last_dish = dish
    st.session_state.result = generate_cart(dish)

# ---------------- MAIN RESULT ----------------
if st.session_state.result:

    result = st.session_state.result

    # -------- INGREDIENTS + RECIPE SIDE BY SIDE --------
    left_col, right_col = st.columns([1, 1.5])

    # -------- INGREDIENTS --------
    with left_col:
        st.markdown("## 🥘 Ingredients")

        cols = st.columns(2)
        for i, item in enumerate(result["ingredients"]):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="padding:10px; border-radius:10px; background:#f5f5f5; text-align:center;">
                    <b>{item['name']}</b><br>
                    <span style="color:grey;">{item['quantity']}</span>
                </div>
                """, unsafe_allow_html=True)

    # -------- RECIPE --------
    with right_col:
        st.markdown("## 👨‍🍳 Cooking Steps")

        for i, step in enumerate(result["steps"], 1):
            st.markdown(f"""
            <div style="padding:12px; border-radius:10px; background:#f9f9f9; margin-bottom:10px;">
                <b>Step {i}</b><br>
                {step}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- CART ----------------
    st.markdown("## 🛒 Your Cart")

    available = []
    unavailable = []

    for item in result["cart"]:
        if item["product"] != "❌ Not available":
            available.append(item)
        else:
            unavailable.append(item)

    total = 0
    selected_items = []

    cols = st.columns(3)

    for i, item in enumerate(available):
        with cols[i % 3]:

            st.markdown("""
            <div style="padding:15px; border-radius:15px; background:#ffffff; box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
            """, unsafe_allow_html=True)

            st.image(item["image"], width=80)

            st.markdown(f"**{item['product']}**")
            st.caption(item["quantity"])
            st.markdown(f"💰 ₹{item['price']}")

            checked = st.checkbox(
                "Add",
                value=True,
                key=f"cart_{i}"
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

    st.markdown("---")