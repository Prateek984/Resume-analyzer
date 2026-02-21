import json
import re
from core.llm_client import ask_llm


def load_prompt():
    with open("prompts/parse_resume.txt", "r", encoding="utf-8") as f:
        return f.read()


def extract_json(text: str) -> str:
    """Remove markdown and extract valid JSON"""

    # remove ```json ``` wrappers
    text = re.sub(r"```json|```", "", text).strip()

    # find first { to last }
    start = text.find("{")
    end = text.rfind("}") + 1

    if start != -1 and end != -1:
        return text[start:end]

    return text


def parse_resume(resume_text: str) -> dict:
    prompt = load_prompt().format(resume=resume_text[:10000])

    response = ask_llm(prompt)

    try:
        clean = extract_json(response)
        data = json.loads(clean)
        return data

    except Exception as e:
        print("Failed to parse JSON. Raw response:", response)
        print("Error:", e)
        return {}