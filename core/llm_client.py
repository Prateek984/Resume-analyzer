import os
from dotenv import load_dotenv
from openai import OpenAI

import streamlit as st
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

MODEL_NAME = "gpt-4o-mini"


def ask_llm(prompt: str, temperature: float = 0.2) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "ERROR: Failed to generate response"