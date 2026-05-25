from services.openai_service import get_completion
import json
import re


def get_recipe_data(dish):

    prompt = f"""
    Give a recipe for {dish}.

    Return ONLY valid JSON in this format:

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

    Do not include markdown.
    Do not include explanation.
    Only return raw JSON.
    """

    try:

        response = get_completion(prompt)

        # 🔥 REMOVE ```json blocks if present
        response = response.strip()

        response = re.sub(r"^```json", "", response)
        response = re.sub(r"```$", "", response)

        response = response.strip()

        recipe = json.loads(response)

        return recipe

    except Exception as e:

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
