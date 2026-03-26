import json
from services.openai_service import get_completion

def get_recipe_data(dish):
    prompt = f"Give ingredients and steps for {dish}"

    response = get_completion(prompt)

    try:
        data = json.loads(response)
        return data
    except:
        return {
            "ingredients": [{"name": "Unknown", "quantity": ""}],
            "steps": ["Could not parse recipe"]
        }
