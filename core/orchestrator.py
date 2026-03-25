from agents.recipe_agent import get_recipe_data
from agents.mapping_agent import map_ingredients_to_products
from agents.cart_agent import build_cart


def generate_cart(dish):

    recipe = get_recipe_data(dish)

    ingredients = recipe.get("ingredients", [])
    steps = recipe.get("steps", [])

    mapped = map_ingredients_to_products(ingredients)
    cart = build_cart(mapped)

    return {
        "ingredients": ingredients,
        "cart": cart,
        "steps": steps
    }