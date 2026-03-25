import json
from services.openai_service import get_completion


def extract_json(response_text):
    try:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        return json.loads(response_text[start:end])
    except Exception as e:
        print("JSON error:", e)
        return {"ingredients": [], "steps": []}


def get_recipe_data(dish):

    prompt = f"""
You are a professional Indian home chef.

Generate a complete cooking plan for "{dish}" for 2 people.

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- No extra text
- Use double quotes
- Use realistic ingredient names

FORMAT:
{{
  "ingredients": [
    {{"name": "", "quantity": ""}}
  ],
  "steps": [
    "step 1",
    "step 2"
  ]
}}
"""

    response = get_completion(prompt)

    print("\n--- RAW LLM RESPONSE ---")
    print(response)

    data = extract_json(response)

    return data