from services.openai_service import get_completion
import json


def get_recipe_data(dish):

    prompt = f"""
    Give a recipe for {dish} in JSON format only.

    Format:
    {{
        "ingredients": [
            {{
                "name": "ingredient name",
                "quantity": "quantity"
            }}
        ],
        "steps": [
            "step 1",
            "step 2"
        ]
    }}

    Return ONLY valid JSON.
    """

    try:

        response = get_completion(prompt)

        print("OPENAI RESPONSE:")
        print(response)

        recipe = json.loads(response)

        return recipe

    except Exception as e:

        print("ERROR:")
        print(str(e))

        return {
            "ingredients": [
                {
                    "name": "Unknown",
                    "quantity": ""
                }
            ],
            "steps": [
                f"ERROR: {str(e)}"
            ]
        }
