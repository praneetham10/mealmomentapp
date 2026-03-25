from services.snowflake_service import get_products
import random


# 💰 Simple pricing (you can later replace with real DB pricing)
def get_price():
    return random.randint(50, 250)


# 🖼️ Local image mapping (NO external URLs = no broken images)
def get_image(product_name):
    name = product_name.lower()

    if "paneer" in name:
        return "assets/paneer.png"
    elif "tomato" in name:
        return "assets/tomato.png"
    elif "onion" in name:
        return "assets/onion.png"
    elif "butter" in name:
        return "assets/butter.png"
    elif "oil" in name:
        return "assets/oil.png"
    elif "cream" in name:
        return "assets/cream.png"
    elif "milk" in name:
        return "assets/milk.png"
    elif "cashew" in name:
        return "assets/cashew.png"
    elif "masala" in name or "spice" in name:
        return "assets/spices.png"
    elif "chili" in name:
        return "assets/chili.png"
    elif "turmeric" in name:
        return "assets/turmeric.png"
    else:
        return "assets/default.png"


def map_ingredients_to_products(ingredients):
    products = get_products()
    mapped = []

    for item in ingredients:
        ingredient_name = item["name"].lower()
        best_match = None

        # 🔍 Matching logic (simple but effective for MVP)
        for product in products:
            category = product["category"].lower()

            if category in ingredient_name or ingredient_name in category:
                best_match = product
                break

        # ✅ If match found
        if best_match:
            mapped.append({
                "ingredient": item["name"],
                "product": best_match["name"],
                "quantity": item["quantity"],
                "price": get_price(),
                "image": get_image(best_match["name"])
            })

        # ❌ If not found
        else:
            mapped.append({
                "ingredient": item["name"],
                "product": "❌ Not available",
                "quantity": item["quantity"],
                "price": 0,
                "image": get_image(item["name"])  # still show relevant icon
            })

    return mapped