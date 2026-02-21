import streamlit as st
from openai import OpenAI

def get_client():
    if "OPENAI_API_KEY" not in st.secrets:
        return None
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def ask_llm(prompt: str, temperature: float = 0.2) -> str:
    client = get_client()

    if client is None:
        return "ERROR: API key not configured"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "ERROR: Failed to generate response"