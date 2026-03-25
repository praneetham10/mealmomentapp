from services.openai_service import get_completion

response = get_completion("List ingredients for dosa for 2 people in JSON format")

print(response)