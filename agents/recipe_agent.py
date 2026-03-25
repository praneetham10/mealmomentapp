from services.openai_service import get_completion
import json

def get_recipe_data(dish):
    prompt = f"""
    Give ingredients with quantities and steps for {dish}.
    
    Return JSON in this format:
    {{
        "ingredients": [{{"name": "", "quantity": ""}}],
        "steps": ["", ""]
    }}
    """

    response = get_completion(prompt)

    try:
        data = json.loads(response)
    except:
        data = {
            "ingredients": [{"name": "Unknown", "quantity": ""}],
            "steps": ["Could not parse recipe"]
        }

    return data
