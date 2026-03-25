from agents.recipe_agent import get_recipe_data

def generate_cart(dish):
    recipe_data = get_recipe_data(dish)

    ingredients = recipe_data.get("ingredients", [])
    steps = recipe_data.get("steps", [])

    # SIMPLE CART LOGIC (no mapper needed)
    cart = []

    for item in ingredients:
        cart.append({
            "ingredient": item.get("name", ""),
            "product": item.get("name", ""),  # basic mapping
            "price": 50,  # dummy price
            "quantity": item.get("quantity", "")
        })

    return {
        "ingredients": ingredients,
        "steps": steps,
        "cart": cart
    }
