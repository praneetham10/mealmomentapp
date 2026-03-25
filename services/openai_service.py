import os
from openai import OpenAI

# Get API key from environment (Streamlit Secrets)
api_key = os.getenv("OPENAI_API_KEY")

# Optional safety check
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please add it in Streamlit Secrets.")

client = OpenAI(api_key=api_key)

def get_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful cooking assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
