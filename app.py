import streamlit as st
import time
from core.orchestrator import generate_cart

st.set_page_config(page_title="Meal Moment", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center;'>🍳 Meal Moment</h1>
<p style='text-align: center; color: grey;'>Cook smarter. Shop instantly.</p>
""", unsafe_allow_html=True)

dish = st.text_input("🔍 What do you want to cook?")

# ---------------- PROTECTION ----------------
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

if "last_used" not in st.session_state:
    st.session_state.last_used = 0

# ---------------- BUTTON ----------------
if st.button("Generate Cart"):

    # LIMIT REQUESTS
    if st.session_state.usage_count >= 5:
        st.warning("⚠️ Limit reached. Please try later.")
        st.stop()

    # COOLDOWN
    if time.time() - st.session_state.last_used < 5:
        st.warning("⏳ Please wait a few seconds before trying again.")
        st.stop()

    st.session_state.last_used = time.time()
    st.session_state.usage_count += 1

    if dish:
        result = generate_cart(dish)

        # ---------------- INGREDIENTS + RECIPE ----------------
        left_col, right_col = st.columns([1, 1.5])

        with left_col:
            st.markdown("## 🥘 Ingredients")
            cols = st.columns(2)

            for i, item in enumerate(result["ingredients"]):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div style="padding:10px; border-radius:10px; background:#f5f5f5;">
                        <b>{item['name']}</b><br>
                        <span style="color:grey;">{item['quantity']}</span>
                    </div>
                    """, unsafe_allow_html=True)

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

        total = 0

        for item in result["cart"]:
            if item["product"] != "❌ Not available":
                st.write(f"✔ {item['product']} - ₹{item['price']}")
                total += item["price"]
            else:
                st.write(f"❌ {item['ingredient']} not available")

        st.markdown(f"### 💳 Total: ₹{total}")
