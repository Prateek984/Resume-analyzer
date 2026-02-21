import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Create single reusable client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_llm(prompt: str, temperature: float = 0.2) -> str:
    """
    Sends a prompt to OpenAI and returns text response.
    Central function used across project.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # cheap + good
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "ERROR: Failed to generate response"