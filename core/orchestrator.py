from agents.recipe_agent import get_recipe_data
from services.snowflake_service import fetch_products


def map_ingredients_to_products(ingredients, products):

    cart = []

    for ing in ingredients:
        ing_name = ing["name"].lower()

        matched = None

        for product in products:
            if ing_name in product["name"]:
                matched = product
                break

        if matched:
            cart.append({
                "product": matched["name"].title(),
                "quantity": ing["quantity"],
                "price": matched["price"]
            })
        else:
            cart.append({
                "product": "❌ Not available",
                "ingredient": ing_name,
                "quantity": ing["quantity"],
                "price": 0
            })

    return cart


def generate_cart(dish):

    recipe = get_recipe_data(dish)

    ingredients = recipe["ingredients"]
    steps = recipe["steps"]

    # 🔥 Fetch from Snowflake
    products = fetch_products()

    cart = map_ingredients_to_products(ingredients, products)

    return {
        "ingredients": ingredients,
        "steps": steps,
        "cart": cart
    }
