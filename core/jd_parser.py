import json
import re
from core.llm_client import ask_llm


def load_prompt():
    with open("prompts/parse_jd.txt", "r", encoding="utf-8") as f:
        return f.read()


def extract_json(text: str) -> str:
    text = re.sub(r"```json|```", "", text).strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]


def parse_jd(jd_text: str) -> dict:
    prompt = load_prompt().format(jd=jd_text[:10000])

    response = ask_llm(prompt)

    try:
        clean = extract_json(response)
        return json.loads(clean)
    except Exception as e:
        print("JD parse failed:", response)
        print("Error:", e)
        return {}