import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a cooking assistant.
Always respond ONLY in valid JSON format.

Format:
{
  "ingredients": [{"name": "", "quantity": ""}],
  "steps": ["step1", "step2"]
}
"""
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
